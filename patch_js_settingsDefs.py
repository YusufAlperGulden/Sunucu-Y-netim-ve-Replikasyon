import re
import json

js_path = 'fastapi_app/static/main.js'
with open(js_path, 'r', encoding='utf-8') as f:
    content = f.read()

# I will replace the settingsDefs array
old_settings = r"const settingsDefs = \[\s*\{ key: 'backup_cloud_retention'.*?\}\s*\];"

new_settings = """const settingsDefs = [
        // Backup
        { category: 'Backup', key: 'backup_cloud_retention', desc: 'Setting of how many days to keep the backups uploaded to a cloud. Backups matching retention period are removed.' },
        { category: 'Backup', key: 'backup_create_checksum', desc: 'Configures cmon if it has to calculate checksum (md5sum) on the created backup files and verify them.' },
        { category: 'Backup', key: 'backup_delete_all_job_max_reattempts', desc: 'Max number of attempts on DELETE_ALL_BACKUPS jobs it can be triggered on cluster drop operation.' },
        { category: 'Backup', key: 'backup_delete_all_job_min_delay_on_reattempts', desc: 'Delay between attempts on DELETE_ALL_BACKUPS jobs it can be triggered on cluster drop operation.' },
        { category: 'Backup', key: 'backup_encryption_key', desc: 'The AES encryption key to encrypt backups. The format of the string is base64 encoded.' },
        { category: 'Backup', key: 'backup_n_safety_copies', desc: 'Setting of how many completed full backups will be kept regardless of their retention status.' },
        { category: 'Backup', key: 'backup_post_script', desc: 'This script is executed after the backup happens, but after a candidate has been elected.' },
        { category: 'Backup', key: 'backup_pre_script', desc: 'This script is executed before the backup happens, but after a candidate has been elected.' },
        { category: 'Backup', key: 'backup_retention', desc: 'Setting of how many days to keep the backups. Backups matching retention period are removed.' },
        { category: 'Backup', key: 'backup_subdir', desc: 'Set the name of the backup subdirectory. This string may hold standard %X field separators.' },
        { category: 'Backup', key: 'backup_user', desc: 'The username of the database account used for managing backups.' },
        { category: 'Backup', key: 'backup_user_password', desc: 'The database password for backup user.' },
        { category: 'Backup', key: 'backupdir', desc: 'The default backup directory, to be pre-filled in Frontend.' },
        { category: 'Backup', key: 'pgbackrest_cipher_pass', desc: 'The AES key to be used to encrypt backup repository of PgBackRest.' },
        { category: 'Backup', key: 'pgbackrest_cipher_type', desc: 'Cipher to be used to encrypt backup repository of PgBackRest.' },
        { category: 'Backup', key: 'pgbackrest_repo_hostname', desc: 'The name of the repository host where to save backup data of PgBackRest.' },
        { category: 'Backup', key: 'pgbackrest_repo_path', desc: 'The path of the repository directory where to save backup data of PgBackRest.' },
        { category: 'Backup', key: 'pgbackrest_stanza_name', desc: 'The name of the stanza to be used to save and restore backups of the cluster.' },
        
        // Cluster
        { category: 'Cluster', key: 'cluster_auto_recovery', desc: 'Enable or disable automatic cluster recovery on primary failure.' },
        { category: 'Cluster', key: 'node_auto_recovery', desc: 'Enable or disable automatic node recovery on individual node failure.' },
        
        // Long Query
        { category: 'Long Query', key: 'log_min_duration_statement', desc: 'PostgreSQL parameter: Logs statements that run longer than this many milliseconds. Set to -1 to disable.' },
        { category: 'Long Query', key: 'long_query_time', desc: 'Threshold in seconds for capturing slow queries in the dashboard.' },
        
        // Replication
        { category: 'Replication', key: 'wal_level', desc: 'PostgreSQL parameter: Set to logical for logical replication, or replica for streaming.' },
        { category: 'Replication', key: 'max_replication_slots', desc: 'PostgreSQL parameter: Maximum number of replication slots.' },
        { category: 'Replication', key: 'max_wal_senders', desc: 'PostgreSQL parameter: Maximum number of simultaneous WAL sender processes.' },
        
        // Retention
        { category: 'Retention', key: 'pitr_retention_hours', desc: 'Retention hours to erase old WAL archive logs for Point-In-Time-Recovery.' },
        { category: 'Retention', key: 'metric_retention_days', desc: 'Number of days to keep historical performance metrics in the local database.' },
        
        // Sampling
        { category: 'Sampling', key: 'metrics_sampling_interval', desc: 'Interval in seconds between metric collection polls.' },
        { category: 'Sampling', key: 'ping_interval', desc: 'Interval in seconds between node health checks.' },
        
        // Swapping
        { category: 'Swapping', key: 'swap_alert_threshold_percent', desc: 'Trigger an alarm if OS swap usage exceeds this percentage.' },
        
        // System
        { category: 'System', key: 'shared_buffers', desc: 'PostgreSQL parameter: Amount of memory the database server uses for shared memory buffers.' },
        { category: 'System', key: 'work_mem', desc: 'PostgreSQL parameter: Amount of memory to be used by internal sort operations and hash tables.' },
        { category: 'System', key: 'max_connections', desc: 'PostgreSQL parameter: Maximum number of concurrent connections to the database server.' },
        
        // Threshold
        { category: 'Threshold', key: 'cpu_alarm_threshold', desc: 'Trigger a critical alarm if CPU usage exceeds this percentage.' },
        { category: 'Threshold', key: 'ram_alarm_threshold', desc: 'Trigger a critical alarm if RAM usage exceeds this percentage.' },
        { category: 'Threshold', key: 'disk_alarm_threshold', desc: 'Trigger a critical alarm if Disk usage exceeds this percentage.' }
    ];"""

content = re.sub(old_settings, new_settings, content, flags=re.DOTALL)

with open(js_path, 'w', encoding='utf-8') as f:
    f.write(content)
print("Updated settingsDefs")
