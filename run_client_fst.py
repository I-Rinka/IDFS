import client.active_client as ac
import socket

my_ip = socket.gethostbyname(socket.gethostname())
fst_client = ac.active_client(my_ip)
fst_client.start_db()
fst_client.put("util.py")