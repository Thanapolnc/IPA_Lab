from netmiko import ConnectHandler
from pathlib import Path
import time
import re

username = 'admin'

devices_ip = ["172.31.114.3", "172.31.114.4", "172.31.114.5"]

pattern = r'^(\S+)\s+.*\s+up\s+up\s*$'

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

DEVICE_PARAMS = {'device_type': 'cisco_ios',
                 'username': username,
                 'use_keys': True,
                 'disabled_algorithms': disabled,
                 'key_file': str(Path.home() / ".ssh" / "id_rsa"),
                 'allow_agent': False             
}

for ip in devices_ip:
  device_params = DEVICE_PARAMS.copy()
  device_params["ip"] = ip

  with ConnectHandler(**device_params) as ssh:
      ssh.enable()
      print(f"Connected to {ip}")
      output = ssh.send_command('sh ip int br')

      up_int = []

      for line in output.splitlines():
         match = re.search(pattern, line)
         if match:
            up_int.append(match.group(1))

      print(f" {ip} UP/UP Interface is: ", up_int or "None")
      time.sleep(2)

      