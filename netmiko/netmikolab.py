from netmiko import ConnectHandler
from pathlib import Path
import time

username = 'admin'

devices = {
    "S1": "172.31.114.3",
    "R1": "172.31.114.4",
    "R2": "172.31.114.5"
}

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
  "exit",
  "int vlan 101",
  "no shut",
  "exit",
  "int range gi0/1, gi1/1",
  "switchport mode access",
  "switchport access vlan 101"

]

R1_CONFIG = [
  "int gi0/2",
  "no sh",
  "ip vrf forwarding Control-Data",
  "ip add 172.31.114.6 255.255.255.240",
  "int gi0/1",
  "no sh",
  "ip vrf forwarding Control-Data",
  "ip add 192.168.114.1 255.255.255.128",
  "int lo0",
  "no sh",
  "ip vrf forwarding Control-Data",
  "ip add 1.1.1.1 255.255.255.255",
  "router ospf 1 vrf Control-Data",
  "network 172.31.114.0 0.0.0.255 area 0",
  "network 192.168.114.0 0.0.0.127 area 0",
  "network 1.1.1.1 0.0.0.0 area 0",
  "exit",
  "ip domain-lookup",
  "ip name-server vrf Control-Data 192.168.114.2"
]

R2_CONFIG = [
  "int gi0/1",
  "no sh",
  "ip vrf forwarding Control-Data",
  "ip add 172.31.114.7 255.255.255.240",
  "int gi0/2",
  "no sh",
  "ip vrf forwarding Control-Data",
  "ip add 192.168.114.129 255.255.255.128",
  "int lo0",
  "no sh",
  "ip vrf forwarding Control-Data",
  "ip add 2.2.2.2 255.255.255.255",
  "int gi0/3",
  "no sh",
  "ip vrf forwarding Control-Data",
  "ip address dhcp",
  "exit",
  "ip route vrf Control-Data 0.0.0.0 0.0.0.0 192.168.122.1",
  "router ospf 1 vrf Control-Data",
  "network 172.31.114.0 0.0.0.255 area 0",
  "network 192.168.114.128 0.0.0.127 area 0",
  "network 2.2.2.2 0.0.0.0 area 0",
  "default-information originate always",
  "exit"
]

PAT_CONFIG = [
  "int gi0/3",
  "ip nat outside",
  "int range gi0/1-2",
  "ip nat inside",  
  "exit",
  "ip nat inside source list 1 interface gigabitEthernet 0/3 vrf Control-Data overload",
  "access-list 1 permit 172.31.114.0 0.0.0.255",
  "access-list 1 permit 192.168.114.0 0.0.0.255",
  "ip name-server 8.8.8.8"
]

ALL_COMMAND  = {
  "S1": S1_CONFIG,
  "R1": R1_CONFIG,
  "R2": R2_CONFIG
}

for device, ip in devices.items():
  device_params = DEVICE_PARAMS.copy()
  device_params["ip"] = ip

  commands = ALL_COMMAND[device]
  
  with ConnectHandler(**device_params) as ssh:
      ssh.enable()
      print(f"Connected to {ip}")
      result = ssh.send_config_set(commands)
      print(f"Configuration result for {ip}:\n{result}")
      time.sleep(2)

      if device == "R2":
        print("OSPF config complete Continue PAT config")
        commands = PAT_CONFIG
        ssh.enable()
        result = ssh.send_config_set(commands)
        print(f"Configuration result for {ip}:\n{result}")
        time.sleep(2)
      