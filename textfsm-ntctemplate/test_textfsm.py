import pytest
from textfsmlab import connect_device, set_description, get_description, get_cdp, autoset_description

def test_s1():
  "test switch 1"
  conn = connect_device("S1")

  autoset_description(conn)

  assert get_description(conn, "Gi0/0") == "Connect to Gi0/3 of Switch0"
  assert get_description(conn, "Gi0/1") == "Connect to Gi0/2 of Router2"
  assert get_description(conn, "Gi1/1") == "Connect to PC"

def test_R1():
  "test router 1"
  conn = connect_device("R1")

  autoset_description(conn)

  assert get_description(conn, "Gi0/0") == "Connect to Gi0/1 of Switch0"
  assert get_description(conn, "Gi0/1") == "Connect to PC"
  assert get_description(conn, "Gi0/2") == "Connect to Gi0/1 of Router2"

def test_R2():
  "test router 2"
  conn = connect_device("R2")

  autoset_description(conn)

  assert get_description(conn, "Gi0/0") == "Connect to Gi0/2 of Switch0"
  assert get_description(conn, "Gi0/1") == "Connect to Gi0/2 of Router1"
  assert get_description(conn, "Gi0/2") == "Connect to Gi0/1 of Switch1"
  assert get_description(conn, "Gi0/3") == "Connect to WAN"




