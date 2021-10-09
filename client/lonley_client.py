import client.config as conf
import util as ut
import requests
import os
import time


class lonley_client(object):
    """docstring for lonley_client."""

    def __init__(self, my_ip: str):
        super(lonley_client, self).__init__()
        conf.my_ip = my_ip

    def __init__(self):
        super(lonley_client, self).__init__()

    def start(self, connect_server:str):
        while True:
            header = {"Content-Type": "file", "Authorization": "{}".format(
            ut.GetMyID()), "Operation": "{}".format("get_task")}
            rq= requests.get("http://"+connect_server+":" +
                          str(conf.IDFS_port), timeout=(1, None), headers=header)
            file_name=rq.content.decode("utf8")
            if rq.headers['Operation']=="upload_file":
                file_path=os.path.join(conf.IDFS_root,file_name)
                header = {"Content-Type": "file", "Authorization": "{}".format(
                     ut.GetMyID()), "Operation": "{}".format("post_file")}
                if os.path.exists(file_path):
                    try:
                        print("transferring {}",file_path)
                        f=open(file_path,'rb')
                        print("addr:"+"http://"+connect_server+":" +
                                    str(conf.IDFS_port)+'/'+file_name)
                        rq= requests.post("http://"+connect_server+":" +
                                    str(conf.IDFS_port)+'/'+file_name, headers=header,data=f.read())
                        print(rq.status_code)
                    except:
                        print("upload error")
                else:
                    print("no!")
            else:
                time.sleep(1)

