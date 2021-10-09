import client.active_client as ac
import socket
import client.config as conf

my_ip = "192.168.91.10"
fst_client = ac.active_client(my_ip,"192.168.91.8")
print(my_ip)
conf.my_ip=my_ip
fst_client.join_db("192.168.91.9")
import client.http_handler as ss
ss.http_server(fst_client.db).start_server()
fst_client.put("bigfile/bf2")

for j in range(3):
    for i in range(6,11):
        print("bigfile/mf"+str(i))
        fst_client.put("bigfile/mf"+str(i))
    for i in range(51,101):
        print("bigfile/sf"+str(i))
        fst_client.put("bigfile/sf"+str(i))