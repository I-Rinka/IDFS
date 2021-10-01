import time
import client.config as conf
import requests
import util as ut
import os

def back_thread():
    while True:
        time.sleep(1)
        header = {"Content-Type": "file", "Authorization": "{}".format(
            ut.GetMyID()), "Operation": "{}".format("null")}
        rq = requests.get("http://"+conf.server_ip+":" +
                          str(conf.IDFS_port), timeout=(1, None), headers=header)
        file_list = rq.content.decode("utf8").split("\n")
        
        for file in file_list:
            file_path=os.path.join(conf.IDFS_root,file)
            if os.path.exists(file_path):
                files={'file':open(file_path,'rb')}
            requests.post("http://"+conf.server_ip+":" +
                          str(conf.IDFS_port), timeout=(1, None), headers=header,files=files)
