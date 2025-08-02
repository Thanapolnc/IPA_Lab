from netmiko import ConnectHandler
from pathlib import Path
import time
import yaml
from jinja2 import Environment, FileSystemLoader

username = 'admin'

devices = {
    "s1": "172.31.114.3",
    "r1": "172.31.114.4",
    "r2": "172.31.114.5"
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

for device, ip in devices.items():
  device_params = DEVICE_PARAMS.copy()
  device_params["ip"] = ip

  with open('device_data/{}.yaml'.format(device)) as f:
    device_vars = yaml.safe_load(f)

  env = Environment(loader=FileSystemLoader('templatej2'))
  template = env.get_template('{}.j2'.format(device))

  commands = template.render(device_vars['{}'.format(device)]).splitlines()
  
  with ConnectHandler(**device_params) as ssh:
      ssh.enable()
      print(f"Connected to {ip}")
      result = ssh.send_config_set(commands)
      print(f"Configuration result for {ip}:\n{result}")
      time.sleep(2)

      if device == "r2":
        print("OSPF config complete Continue PAT config")
        with open('device_data/R2_PAT.yaml') as f:
          device_vars = yaml.safe_load(f)

        env = Environment(loader=FileSystemLoader('templatej2'))
        template = env.get_template('r2_pat.j2')

        commands = template.render(device_vars["r2_pat"]).splitlines()
        
        ssh.enable()
        result = ssh.send_config_set(commands)
        print(f"Configuration result for {ip}:\n{result}")
        time.sleep(2)


