import client.db as dbo
import threading
import requests
import util as ut
import client.config as conf
import os


def request_cloud():
    print("remote access")


def get_thread(db, file_path: str):
    id_list, ip_list, file_list = db.get_available_device(
        os.path.basename(file_path), os.path.dirname(file_path))
    print(id_list)
    print(ip_list)
    print(file_list)

    # myfile=os.path.join(conf.IDFS_root.replace('\\','/'),file_path)
    # print(myfile)
    # if os.path.isfile(myfile):
    #     return True

    header = {"Content-Type": "file", "Authorization": "{}".format(
        ut.GetMyID()), "Operation": "{}".format("get_file")}
    if len(id_list) == 0:
        request_cloud()
    else:
        have_get = False
        for i in range(len(id_list)):
            if have_get:
                break
            ip = ip_list[i]
            dv_id = id_list[i]
            file_hash = file_list[i]
            if os.path.isfile(os.path.join(conf.IDFS_root.replace('\\', '/'+'/'), file_hash)):
                print("File {file} exists!".format(file=file_path))
                have_get = True
                continue
            if ip == conf.my_ip:
                continue
            try:
                rq = requests.get("http://"+ip+":"+str(conf.IDFS_port) +
                                  "/"+file_hash, timeout=(1, None), headers=header)
                if rq.status_code == 200:
                    f = open(conf.IDFS_root+'/'+file_hash, 'wb+')
                    f.write(rq.content)
                    print("receive file:{path}".format(path=file_path))
                    f.close()
                    have_get = True
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
