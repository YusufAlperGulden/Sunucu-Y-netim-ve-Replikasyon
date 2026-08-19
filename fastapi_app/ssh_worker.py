import paramiko
import io

class SSHManager:
    def __init__(self, host, port, username, credential_string):
        self.host = host
        self.port = port
        self.username = username
        self.credential_string = credential_string
        self.client = paramiko.SSHClient()
        self.client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    def connect(self):
        # Determine if credential is a PEM key
        is_key = False
        if self.credential_string and "-----BEGIN" in self.credential_string:
            is_key = True
            
        if is_key:
            try:
                # Try RSA first
                pkey = paramiko.RSAKey.from_private_key(io.StringIO(self.credential_string))
            except Exception:
                try:
                    # Try Ed25519
                    pkey = paramiko.Ed25519Key.from_private_key(io.StringIO(self.credential_string))
                except Exception:
                    # Fallback to ECDSA
                    pkey = paramiko.ECDSAKey.from_private_key(io.StringIO(self.credential_string))
            
            self.client.connect(hostname=self.host, port=self.port, username=self.username, pkey=pkey, timeout=10)
        else:
            self.client.connect(hostname=self.host, port=self.port, username=self.username, password=self.credential_string, timeout=10)

    def execute_command(self, command):
        stdin, stdout, stderr = self.client.exec_command(command)
        return stdout.read().decode('utf-8', errors='ignore'), stderr.read().decode('utf-8', errors='ignore'), stdout.channel.recv_exit_status()

    def read_file(self, file_path):
        sftp = self.client.open_sftp()
        try:
            with sftp.file(file_path, 'r') as f:
                content = f.read().decode('utf-8')
            return content
        finally:
            sftp.close()

    def write_file(self, file_path, content):
        sftp = self.client.open_sftp()
        try:
            with sftp.file(file_path, 'w') as f:
                f.write(content)
        finally:
            sftp.close()

    def disconnect(self):
        self.client.close()

    def __enter__(self):
        self.connect()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.disconnect()
