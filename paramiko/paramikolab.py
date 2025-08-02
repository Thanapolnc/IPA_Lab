import time
import paramiko
from pathlib import Path

USERNAME = 'admin'

devices_ip = ["172.31.114.1", "172.31.114.2", "172.31.114.3", "172.31.114.4", "172.31.114.5"]

disabled = {
    'kex': [
        'diffie-hellman-group1-sha1',
        'diffie-hellman-group-exchange-sha256',
        'ecdh-sha2-nistp256', 'ecdh-sha2-nistp384', 'ecdh-sha2-nistp521'
    ],
    'pubkeys': [
        'rsa-sha2-256', 'rsa-sha2-512',
    ],
    'mac': [
        'hmac-sha2-256', 'hmac-sha2-512',
    ]
}

for ip in devices_ip:
  client = paramiko.SSHClient()
  client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
  client.connect(hostname=ip, 
                 username=USERNAME,
                 disabled_algorithms=disabled,
                 key_filename=str(Path.home() / ".ssh" / "id_rsa"),
                 look_for_keys=False,
                 allow_agent=False)
  with client.invoke_shell() as ssh:
    print("Connected to {}".format(ip))

    ssh.send("terminal length 0\n")
    time.sleep(1)
    result = ssh.recv(1000).decode('ascii')
    print(result)

    ssh.send("en\n")
    time.sleep(1)
    result = ssh.recv(1000).decode('ascii')
    print(result)

    ssh.send("sh ip int br\n")
    time.sleep(3)
    result = ssh.recv(3000).decode('ascii')
    print(result)
  
  client.close()