import client.active_client as ac
import socket

my_ip = socket.gethostbyname(socket.gethostname())
fst_client = ac.active_client(my_ip,"192.168.91.8")
fst_client.join_db("192.168.91.9")
fst_client.get("util.py")