import client.db as dbo
import threading
import requests
import util as ut
import client.config as conf

def request_cloud():
    print("remote access")


def get_thread(db,id_list:list, ip_list:list, file_list:list, file_path:str):
    header = {"Content-Type": "file", "Authorization": "{}".format(
    ut.GetMyID()), "Operation": "{}".format("get_file")}
    if len(id_list) == 0:
        request_cloud()
    else:
        have_get=False
        for i in range(len(id_list)):
            if have_get:
                break
            ip = ip_list[i]
            dv_id = id_list[i]
            file_hash = file_list[i]
            try:
                rq = requests.get("http://"+ip+":"+str(conf.IDFS_port) +
                                  "/"+file_hash, timeout=(1, None),headers=header)
                if rq.status_code==200:
                    f=open(conf.IDFS_root+'/'+file_hash,'wb+')
                    f.write(rq.content)
                    print("receive file:{path}".format(path=file_path))
                    have_get=True
                else:
                    print("in future, this log will delete")
                    
            except Exception as e:
                print(e)
                if isinstance(db, dbo.rqdb):
                    db.offline_device(dv_id)
                else:
                    print("offline")
            else:
                pass
        if not have_get:
            request_cloud()
