import requests
import client.config as conf
import time
# big file
ip="192.168.91.8"

t1=time.time_ns()

for i in range(2):
    def get_file(file_name:str):
        rq = requests.get("http://"+ip+":"+str(conf.IDFS_port) +
                        "/"+file_name)
        if rq.status_code == 200:
            f = open("bigfile"+'/'+file_name, 'wb+')
            f.write(rq.content)
            f.close()

    for i in range(4):
        file_name="bf"+str(i+1)
        get_file(file_name)

    # medium file
    for i in range(20):
        file_name="mf"+str(i+1)
        get_file(file_name)
        

    # small file
    for i in range(200):
        file_name="sf"+str(i+1)
        get_file(file_name)

    print("ns:"+str(time.time_ns()-t1))