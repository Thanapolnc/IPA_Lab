from netmiko import ConnectHandler
from pathlib import Path

username = 'admin'
# password = 'cisco'

devices_ip = ["172.31.114.3", "172.31.114.4", "172.31.114.5"]

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

S1_CONFIG = [
  "vlan 101",
  "name control-data",
  "int vlan 101",
  "no shut",
  "#int range gi0/1-2",
  "#switchport mode access"
  "switchport access vlan 101"

]

R1_CONFIG = [
  ""
]

for ip in devices_ip:
  device_params = DEVICE_PARAMS.copy()
  device_params["ip"] = ip

  with ConnectHandler(**device_params) as ssh:
    result = ssh.send_command('sh ip int br')
    print(result)