"""
deploy_worker.py -- PostgreSQL Streaming Replication Deployment Automation
"""
import ast
import datetime
import time

from models import SessionLocal, DeployJob
from ssh_worker import SSHManager
from vault import decrypt


def _ts():
    return datetime.datetime.utcnow().strftime("[%H:%M:%S]")


def _append_log(job_id, line):
    db = SessionLocal()
    try:
        job = db.query(DeployJob).filter(DeployJob.id == job_id).first()
        if not job:
            return
        job.log_output = (job.log_output or "") + f"{_ts()} {line}\n"
        job.updated_at = datetime.datetime.utcnow()
        db.commit()
    except Exception:
        db.rollback()
    finally:
        db.close()


def _set_status(job_id, status, step, error_msg=None):
    db = SessionLocal()
    try:
        job = db.query(DeployJob).filter(DeployJob.id == job_id).first()
        if not job:
            return
        job.status = status
        job.step = step
        if error_msg is not None:
            job.error_msg = error_msg[:950]
        job.updated_at = datetime.datetime.utcnow()
        db.commit()
    except Exception:
        db.rollback()
    finally:
        db.close()


def _log_and_status(job_id, status, step, msg, error=None):
    _append_log(job_id, msg)
    _set_status(job_id, status, step, error)


def _run(ssh, cmd, job_id, desc=None, sudo="sudo"):
    _append_log(job_id, "$ " + cmd[:120])
    stdout, stderr, rc = ssh.execute_command(cmd)
    for line in stdout.strip().splitlines()[:10]:
        _append_log(job_id, "  " + line)
    if rc != 0 and stderr.strip():
        for line in stderr.strip().splitlines()[:5]:
            _append_log(job_id, "  WARNING: " + line)
    return stdout, stderr, rc


def _detect_os(ssh, job_id):
    out, _, _ = ssh.execute_command("cat /etc/os-release 2>/dev/null || echo unknown")
    out_l = out.lower()
    first_line = out.strip().splitlines()[0] if out.strip() else "unknown"
    _append_log(job_id, "OS: " + first_line)
    if any(x in out_l for x in ("ubuntu", "debian", "mint")):
        return "debian"
    if any(x in out_l for x in ("rhel", "centos", "almalinux", "rocky", "fedora", "oracle")):
        return "rhel"
    raise RuntimeError("Desteklenmeyen OS: " + out.strip()[:200])


def _install_postgresql_debian(ssh, version, sudo, job_id):
    major = version.split(".")[0]
    _append_log(job_id, "Ubuntu/Debian: PostgreSQL " + major + " kuruluyor...")
    cmds = [
        sudo + " apt-get update -qq",
        sudo + " apt-get install -y curl ca-certificates gnupg lsb-release",
        "curl -fsSL https://www.postgresql.org/media/keys/ACCC4CF8.asc | " + sudo + " gpg --dearmor -o /usr/share/keyrings/postgresql-keyring.gpg 2>/dev/null || true",
        "echo \"deb [signed-by=/usr/share/keyrings/postgresql-keyring.gpg] https://apt.postgresql.org/pub/repos/apt $(lsb_release -cs)-pgdg main\" | " + sudo + " tee /etc/apt/sources.list.d/pgdg.list",
        sudo + " apt-get update -qq",
        sudo + " apt-get install -y postgresql-" + major + " postgresql-client-" + major,
    ]
    for cmd in cmds:
        _, stderr, rc = _run(ssh, cmd, job_id, sudo=sudo)
        if rc != 0 and "already installed" not in stderr.lower():
            if "update" in cmd:
                continue
            raise RuntimeError("Kurulum basarisiz: " + stderr[:300])
    _append_log(job_id, "PostgreSQL " + major + " kuruldu (Debian)")


def _install_postgresql_rhel(ssh, version, sudo, job_id):
    major = version.split(".")[0]
    _append_log(job_id, "RHEL/CentOS: PostgreSQL " + major + " kuruluyor...")
    _, _, dnf_rc = ssh.execute_command("which dnf 2>/dev/null")
    pkg = "dnf" if dnf_rc == 0 else "yum"
    cmds = [
        sudo + " " + pkg + " install -y https://download.postgresql.org/pub/repos/yum/reporpms/EL-$(rpm -E %{rhel})-x86_64/pgdg-redhat-repo-latest.noarch.rpm 2>/dev/null || true",
        sudo + " " + pkg + " module disable -y postgresql 2>/dev/null || true",
        sudo + " " + pkg + " install -y postgresql" + major + "-server postgresql" + major,
        sudo + " /usr/pgsql-" + major + "/bin/postgresql-" + major + "-setup initdb 2>/dev/null || true",
    ]
    for cmd in cmds:
        _, stderr, rc = _run(ssh, cmd, job_id, sudo=sudo)
        if rc != 0 and "already installed" not in stderr.lower():
            if "module disable" in cmd or "pgdg-redhat" in cmd:
                continue
            raise RuntimeError("RHEL kurulum basarisiz: " + stderr[:300])
    _append_log(job_id, "PostgreSQL " + major + " kuruldu (RHEL)")


def _get_pg_service_name(version, os_family):
    major = version.split(".")[0]
    if os_family == "rhel":
        return "postgresql-" + major
    return "postgresql"


def _get_data_dir(data_dir, version, os_family):
    major = version.split(".")[0]
    if data_dir and data_dir.strip():
        return data_dir.strip()
    if os_family == "rhel":
        return "/var/lib/pgsql/" + major + "/data"
    return "/var/lib/postgresql/" + major + "/main"


def _get_conf_dir(ssh, data_dir, os_family):
    if os_family == "debian":
        out, _, _ = ssh.execute_command("ls /etc/postgresql/ 2>/dev/null | sort -V | tail -1")
        ver = out.strip()
        if ver:
            return "/etc/postgresql/" + ver + "/main"
    return data_dir


def _disable_firewall(ssh, sudo, db_port, job_id):
    _append_log(job_id, "Guvenlik duvari devre disi birakiliyor...")
    _, _, rc = ssh.execute_command("which ufw 2>/dev/null")
    if rc == 0:
        ssh.execute_command(sudo + " ufw disable 2>/dev/null || true")
    else:
        ssh.execute_command(sudo + " systemctl stop firewalld 2>/dev/null || true")
        ssh.execute_command(sudo + " systemctl disable firewalld 2>/dev/null || true")
        ssh.execute_command(sudo + " iptables -I INPUT -p tcp --dport " + str(db_port) + " -j ACCEPT 2>/dev/null || true")
    _append_log(job_id, "  guvenlik duvari devre disi")


def _disable_selinux(ssh, sudo, job_id):
    _append_log(job_id, "SELinux devre disi birakiliyor...")
    ssh.execute_command(sudo + " setenforce 0 2>/dev/null || true")
    ssh.execute_command(sudo + " sed -i 's/^SELINUX=enforcing/SELINUX=permissive/' /etc/selinux/config 2>/dev/null || true")
    _append_log(job_id, "  SELinux permissive moda alindi")


def _configure_primary(ssh, sudo, conf_dir, data_dir, db_port, replica_ips, db_user, db_pass, service_name, job_id):
    _append_log(job_id, "Primary yapilandirmasi basliyor...")
    major_port = str(db_port)
    pg_settings = {
        "listen_addresses": "'*'",
        "wal_level": "replica",
        "max_wal_senders": "10",
        "wal_keep_size": "1024",
        "hot_standby": "on",
        "port": major_port,
    }
    for key, val in pg_settings.items():
        cmd = (
            sudo + " bash -c \"grep -q '^" + key + "' " + conf_dir + "/postgresql.conf "
            "&& sed -i 's|^" + key + ".*|" + key + " = " + val + "|' " + conf_dir + "/postgresql.conf "
            "|| echo '" + key + " = " + val + "' >> " + conf_dir + "/postgresql.conf\""
        )
        _run(ssh, cmd, job_id)
    _append_log(job_id, "  postgresql.conf guncellendi")

    hba_path = conf_dir + "/pg_hba.conf"
    for rip in replica_ips:
        line = "host replication replicator " + rip + "/32 md5"
        cmd = sudo + " bash -c \"grep -qF 'replication replicator " + rip + "' " + hba_path + " || echo '" + line + "' >> " + hba_path + "\""
        _run(ssh, cmd, job_id)
    cmd = sudo + " bash -c \"grep -qF 'host all all 0.0.0.0/0' " + hba_path + " || echo 'host all all 0.0.0.0/0 md5' >> " + hba_path + "\""
    _run(ssh, cmd, job_id)
    _append_log(job_id, "  pg_hba.conf guncellendi")

    _run(ssh, sudo + " systemctl restart " + service_name, job_id, "PostgreSQL yeniden baslatiliyor")
    time.sleep(4)

    repl_pass = "Repl_" + (db_pass[:8].replace("'", "X") if db_pass else "Pass123")
    create_sql = "DO $$ BEGIN IF NOT EXISTS (SELECT FROM pg_catalog.pg_roles WHERE rolname='replicator') THEN CREATE USER replicator REPLICATION LOGIN ENCRYPTED PASSWORD '" + repl_pass + "'; END IF; END $$;"
    out, err, rc = _run(ssh, sudo + " -u postgres psql -c \"" + create_sql + "\"", job_id, "Replikasyon kullanicisi olusturuluyor")
    if rc != 0:
        raise RuntimeError("Replication user olusturulamadi: " + err[:300])
    _append_log(job_id, "  'replicator' kullanicisi olusturuldu")

    if db_user and db_user.lower() != "postgres":
        admin_sql = "DO $$ BEGIN IF NOT EXISTS (SELECT FROM pg_catalog.pg_roles WHERE rolname='" + db_user + "') THEN CREATE USER \"" + db_user + "\" WITH SUPERUSER ENCRYPTED PASSWORD '" + db_pass + "'; END IF; END $$;"
        _run(ssh, sudo + " -u postgres psql -c \"" + admin_sql + "\"", job_id, "Admin kullanicisi olusturuluyor")

    _append_log(job_id, "Primary yapilandirmasi tamamlandi")
    return repl_pass


def _configure_replica(ssh, sudo, primary_ip, primary_port, data_dir, db_user, repl_pass, service_name, version, job_id):
    _append_log(job_id, "Replica yapilandirmasi basliyor (primary: " + primary_ip + ")...")
    _run(ssh, sudo + " systemctl stop " + service_name + " 2>/dev/null || true", job_id, "PostgreSQL durduruluyor")
    _run(ssh, sudo + " rm -rf " + data_dir, job_id, "Data dizini temizleniyor")
    _run(ssh, sudo + " mkdir -p " + data_dir, job_id)
    _run(ssh, sudo + " chown postgres:postgres " + data_dir, job_id)
    _run(ssh, sudo + " chmod 700 " + data_dir, job_id)

    pgpass_line = primary_ip + ":" + str(primary_port) + ":replication:replicator:" + repl_pass
    _run(ssh, sudo + " bash -c \"echo '" + pgpass_line + "' > /var/lib/postgresql/.pgpass && chmod 600 /var/lib/postgresql/.pgpass && chown postgres:postgres /var/lib/postgresql/.pgpass\"", job_id)

    _append_log(job_id, "pg_basebackup calistiriliyor (birkas dakika surebilir)...")
    pb_cmd = (
        sudo + " -u postgres pg_basebackup "
        "-h " + primary_ip + " -p " + str(primary_port) + " -U replicator "
        "-D " + data_dir + " -Fp -Xs -P -R --no-password"
    )
    out, err, rc = _run(ssh, pb_cmd, job_id, "pg_basebackup")
    if rc != 0:
        raise RuntimeError("pg_basebackup basarisiz: " + err[:400])
    _append_log(job_id, "pg_basebackup tamamlandi")

    _run(ssh, sudo + " -u postgres touch " + data_dir + "/standby.signal", job_id)

    auto_conf = data_dir + "/postgresql.auto.conf"
    conninfo = "host=" + primary_ip + " port=" + str(primary_port) + " user=replicator password=" + repl_pass + " application_name=replica"
    cmd = sudo + " bash -c \"grep -qF primary_conninfo " + auto_conf + " && sed -i \\\"s|primary_conninfo.*|primary_conninfo = \\'" + conninfo + "\\'|\\\" " + auto_conf + " || echo \\\"primary_conninfo = \\'" + conninfo + "\\'\\\" >> " + auto_conf + "\""
    _run(ssh, cmd, job_id, "primary_conninfo ayarlaniyor")

    _run(ssh, sudo + " chown -R postgres:postgres " + data_dir, job_id)
    _run(ssh, sudo + " systemctl enable " + service_name + " 2>/dev/null || true", job_id)
    _run(ssh, sudo + " systemctl start " + service_name, job_id, "PostgreSQL baslatiliyor")
    time.sleep(5)
    _append_log(job_id, "Replica servisi baslatildi")


def _verify_replication(ssh, sudo, job_id):
    out, _, rc = ssh.execute_command(sudo + " -u postgres psql -c \"SELECT client_addr, state, sync_state FROM pg_stat_replication;\" 2>/dev/null")
    _append_log(job_id, "Replikasyon durumu:")
    for line in out.strip().splitlines():
        _append_log(job_id, "  " + line)
    return rc == 0


def run_deploy_job(job_id):
    """Main entry point — called as FastAPI BackgroundTask."""
    db = SessionLocal()
    try:
        job = db.query(DeployJob).filter(DeployJob.id == job_id).first()
        if not job:
            return
        j_ssh_host    = job.ssh_host
        j_ssh_port    = job.ssh_port or 22
        j_ssh_user    = job.ssh_user
        j_ssh_cred    = decrypt(job.encrypted_ssh_cred) if job.encrypted_ssh_cred else ""
        j_sudo        = job.sudo_method or "sudo"
        j_disable_fw  = job.disable_fw
        j_disable_sel = job.disable_selinux
        j_install_sw  = job.install_software
        j_db_version  = job.db_version or "17"
        j_db_port     = job.db_port or 5432
        j_db_user     = job.db_admin_user or "postgres"
        j_db_pass     = decrypt(job.encrypted_db_pass) if job.encrypted_db_pass else ""
        j_db_dir      = job.db_data_dir or ""
        try:
            nodes = ast.literal_eval(job.nodes_json or "[]")
        except Exception:
            nodes = []
    finally:
        db.close()

    primary_nodes = [n for n in nodes if n.get("role") == "primary"]
    replica_nodes = [n for n in nodes if n.get("role") != "primary"]

    if not primary_nodes:
        _set_status(job_id, "FAILED", "no_primary", "Hic primary node tanimlanmamis.")
        return

    primary_ip  = primary_nodes[0].get("ip", "").strip()
    replica_ips = [n.get("ip", "").strip() for n in replica_nodes if n.get("ip", "").strip()]

    # Step 1: Connect to primary
    _log_and_status(job_id, "CONNECTING", "connecting_primary",
                    "Primary SSH: " + j_ssh_user + "@" + primary_ip + ":" + str(j_ssh_port))
    try:
        primary_ssh = SSHManager(primary_ip, j_ssh_port, j_ssh_user, j_ssh_cred)
        primary_ssh.connect()
    except Exception as e:
        err = str(e)
        _log_and_status(job_id, "FAILED", "connection_failed", "SSH hatasi: " + err, err)
        return

    try:
        # Step 2: Detect OS
        _log_and_status(job_id, "SSH_OK", "detecting_os", "Baglanti basarili, OS tespit ediliyor...")
        os_family = _detect_os(primary_ssh, job_id)
        _append_log(job_id, "OS ailesi: " + os_family)

        data_dir    = _get_data_dir(j_db_dir, j_db_version, os_family)
        conf_dir    = _get_conf_dir(primary_ssh, data_dir, os_family)
        svc_name    = _get_pg_service_name(j_db_version, os_family)

        # Step 3: Security
        if j_disable_fw:
            _disable_firewall(primary_ssh, j_sudo, j_db_port, job_id)
        if j_disable_sel:
            _disable_selinux(primary_ssh, j_sudo, job_id)

        # Step 4: Install
        if j_install_sw:
            _log_and_status(job_id, "INSTALLING", "installing_primary",
                            "PostgreSQL " + j_db_version + " primary'e kuruluyor...")
            if os_family == "debian":
                _install_postgresql_debian(primary_ssh, j_db_version, j_sudo, job_id)
            else:
                _install_postgresql_rhel(primary_ssh, j_db_version, j_sudo, job_id)

        # Step 5: Configure primary
        _log_and_status(job_id, "CONFIGURING_PRIMARY", "configuring_primary",
                        "Primary yapilandiriliyor...")
        repl_pass = _configure_primary(
            primary_ssh, j_sudo, conf_dir, data_dir,
            j_db_port, replica_ips, j_db_user, j_db_pass,
            svc_name, job_id
        )
        _log_and_status(job_id, "STARTING_PRIMARY", "primary_ready",
                        "Primary node hazir ve calisiyor.")

    except Exception as e:
        err = str(e)
        _log_and_status(job_id, "FAILED", "primary_error", "Primary hatasi: " + err, err)
        primary_ssh.disconnect()
        return

    primary_ssh.disconnect()

    # Step 6: Configure replicas
    for i, replica_ip in enumerate(replica_ips):
        _log_and_status(job_id, "CONFIGURING_REPLICA", "replica_" + str(i+1) + "_connecting",
                        "Replica " + str(i+1) + ": " + j_ssh_user + "@" + replica_ip)
        try:
            replica_ssh = SSHManager(replica_ip, j_ssh_port, j_ssh_user, j_ssh_cred)
            replica_ssh.connect()
        except Exception as e:
            err = str(e)
            _log_and_status(job_id, "FAILED", "replica_connect_failed", "Replica SSH hatasi: " + err, err)
            return

        try:
            replica_os      = _detect_os(replica_ssh, job_id)
            replica_data    = _get_data_dir(j_db_dir, j_db_version, replica_os)
            replica_svc     = _get_pg_service_name(j_db_version, replica_os)

            if j_disable_fw:
                _disable_firewall(replica_ssh, j_sudo, j_db_port, job_id)
            if j_disable_sel:
                _disable_selinux(replica_ssh, j_sudo, job_id)
            if j_install_sw:
                if replica_os == "debian":
                    _install_postgresql_debian(replica_ssh, j_db_version, j_sudo, job_id)
                else:
                    _install_postgresql_rhel(replica_ssh, j_db_version, j_sudo, job_id)

            _configure_replica(
                replica_ssh, j_sudo,
                primary_ip, j_db_port,
                replica_data, j_db_user, repl_pass,
                replica_svc, j_db_version, job_id
            )
            _append_log(job_id, "Replica " + str(i+1) + " (" + replica_ip + ") tamamlandi.")

        except Exception as e:
            err = str(e)
            _log_and_status(job_id, "FAILED", "replica_error", "Replica hatasi: " + err, err)
            try:
                replica_ssh.disconnect()
            except Exception:
                pass
            return
        finally:
            try:
                replica_ssh.disconnect()
            except Exception:
                pass

    # Step 7: Verify
    _log_and_status(job_id, "VERIFYING", "verifying", "Replikasyon dogrulanıyor...")
    try:
        verify_ssh = SSHManager(primary_ip, j_ssh_port, j_ssh_user, j_ssh_cred)
        verify_ssh.connect()
        _verify_replication(verify_ssh, j_sudo, job_id)
        verify_ssh.disconnect()
    except Exception as e:
        _append_log(job_id, "Dogrulama uyarisi (kurulum tamamlandi): " + str(e))

    _log_and_status(job_id, "SUCCESS", "done",
                    "Deployment tamamlandi! Primary: " + primary_ip + ":" + str(j_db_port))
    _append_log(job_id, "=" * 50)
    _append_log(job_id, "Primary : " + primary_ip + ":" + str(j_db_port))
    for ip in replica_ips:
        _append_log(job_id, "Replica : " + ip + ":" + str(j_db_port))
    _append_log(job_id, "Replikasyon kullanicisi: replicator")
