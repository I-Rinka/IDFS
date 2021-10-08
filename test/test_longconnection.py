from re import L
import threading
import server.server as ss
import requests
import time
import server.config as conf



def th0():
    header = {"Content-Type": "file", "Authorization": "{}".format(
    123123123), "Operation": "{}".format("get_task")}
    rq=requests.get("http://127.0.0.1:"+str(conf.IDFS_port),headers=header)

    print("th0 getting task!")
    print(rq.headers)
    print(rq.content)

def th1():
    header = {"Content-Type": "file", "Authorization": "{}".format(
    123123123), "Operation": "{}".format("get_file")}
    rq=requests.get("http://127.0.0.1:"+str(conf.IDFS_port)+"/"+"12345",headers=header)
    print(rq.status_code)

if __name__ == "__main__":
    threading.Thread(target=ss.IDFS_server().server_start,).start()
    for i in range(10):
        print("th0!")
        threading.Thread(target=th0,).start()

    time.sleep(10)
    print("th1 getting file!")
    th1()
    # threading.Thread(target=th1,).start()
