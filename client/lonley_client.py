import client.config as conf
import util as ut
import requests
import os
import time

class lonley_client(object):
    """docstring for lonley_client."""
    def __init__(self, my_ip:str):
        super(lonley_client, self).__init__()
        conf.my_ip=my_ip
    def __init__(self):
        super(lonley_client, self).__init__()

    def start(self, connect_server:str):
        while True:
            header = {"Content-Type": "file", "Authorization": "{}".format(
            ut.GetMyID()), "Operation": "{}".format("get_task")}
            rq= requests.get("http://"+connect_server+":" +
                          str(conf.IDFS_port), timeout=(1, None), headers=header)
            
            file=rq.content.decode("utf8")
            if rq.headers['Operation']=="upload_file":
                file_path=os.path.join(conf.IDFS_root,file)
                if os.path.exists(file_path):
                    files={'file':open(file_path,'rb')}
                requests.post("http://"+connect_server+":" +
                            str(conf.IDFS_port), timeout=(1, None), headers=header,files=files)
            else:
                time.sleep(1)
