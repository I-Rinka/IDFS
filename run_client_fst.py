import client.active_client as ac
import socket
import time

my_ip = socket.gethostbyname(socket.gethostname())
fst_client = ac.active_client("192.168.91.9","192.168.91.8")
fst_client.start_db()
import client.http_handler as ss
ss.http_server(fst_client.db).start_server()
fst_client.put("bigfile/bf1")
for i in range(5):
    fst_client.put("bigfile/mf"+str(i+1))
for i in range(50):
    fst_client.put("bigfile/sf"+str(i+1))

time.sleep(50)

print("start")
t=time.time_ns()

for i in range(4):
    print("bf"+str(i+1))
    fst_client.get("/bf"+str(i+1),"bf"+str(i+1))
for i in range(20):
    print("mf"+str(i+1))
    fst_client.get("/mf"+str(i+1),"mf"+str(i+1))
for i in range(200):
    print("sf"+str(i+1))
    fst_client.get("/sf"+str(i+1),"sf"+str(i+1))
print("ns:"+str(time.time_ns()-t))
