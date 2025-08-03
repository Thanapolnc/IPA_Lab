import os
from netmiko import ConnectHandler
from pathlib import Path

current_dir = Path(__file__).parent
templates_path = current_dir / "ntc-templates" / "ntc_templates" / "templates"
os.environ['NET_TEXTFSM'] = str(templates_path)

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
                 'allow_agent': False,          
}

def connect_device(name):
  "for connect device"
  device_params = DEVICE_PARAMS.copy()
  device_params.update({'host': devices[name]})
  return ConnectHandler(**device_params)


def set_description(conn, intf, description):
  "set description to interface"

  commands = [
    f'int {intf}',
    f'description {description}',
    'end'
  ]

  return conn.send_config_set(commands)

def get_description(conn, intf):
  "get interface description"

  results =conn.send_command("show interfaces description", use_textfsm=True)

  for result in results:
     
    if(result.get("port", "").lower()) == intf.lower():
        return result.get("description", "")
  return 

def get_cdp(conn):
  "get neighbors of device"

  return conn.send_command("show cdp neighbors", use_textfsm=True)


def autoset_description(conn):
  "automatically generate description"

  print("Getting CDP neighbors...")
  neighbors = get_cdp(conn)
  
  # if not neighbors:
  #   print("No CDP neighbors found!")
  #   return
  
  # print(f"Found {len(neighbors)} neighbors:")
  # for i, entry in enumerate(neighbors):
  #   print(f"Entry {i}: {entry}")
  
  for entry in neighbors:
    # Use correct field names from ntc-templates
    local = entry.get("local_interface")
    nbr = entry.get("neighbor_name") 
    nbr_intf = entry.get("neighbor_interface")

    if not all([local, nbr, nbr_intf]):
       continue

    desc = f"Connect to {nbr_intf} of {nbr}"
    print(f"Setting on {local}: {desc}")
    set_description(conn, local, desc)

if __name__ == "__main__":
    conn = connect_device("S1")
    autoset_description(conn)

    for intf in ["Gi0/0", "Gi0/1", "Gi1/1"]:
        print(f"{intf} → {get_description(conn, intf)}")

    conn.disconnect()




