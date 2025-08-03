import pytest
from textfsmlab import connect_device, set_description, get_description, get_cdp, autoset_description

def test_s1():
  "test switch 1"
  conn = connect_device("S1")

  
  autoset_description(conn)

  assert get_description(conn, "Gi0/0") == "Connect to Gi0/3 of Switch0"
  assert get_description(conn, "Gi0/1") == "Connect to Gi0/2 of Router2"
  assert get_description(conn, "Gi1/1") == "Connect to PC"


