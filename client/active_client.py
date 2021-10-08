from _typeshed import Self
import os
import client.db as dbo
import client.UI as UI
import client.http_handler as http_server
import util as ut
import client.config as conf
import shutil
import requests
import json
import time
import client.get_file as get


class active_client(object):
    """docstring for active_client."""

    def __init__(self, server_ip: conf.server_ip):
        super(active_client, self).__init__()
        self.db = None
        self.current_path = '/'
        self.server_ip = server_ip

    def __init__(self, my_ip: str, server_ip: conf.server_ip):
        super(active_client, self).__init__()
        conf.my_ip = my_ip
        self.current_path = '/'
        self.server_ip = server_ip
        self.db = None

    def start_db(self):
        rqlite = dbo.rqdb(conf.my_ip)
        rqlite.start_db()
        rqlite.connect_db(conf.my_ip, conf.rqlite_port)
        # time.sleep(1)
        while True:
            try:
                rqlite.create_tables()
            except:
                print("not connect, connecting...")
                time.sleep(0.5)
            else:
                break

        rqlite.add_device(ut.GetMyID())
        self.db = rqlite

    def join_db(self, target_ip: str):
        IP = target_ip
        header = {"Content-Type": "file", "Authorization": "{}".format(
            ut.GetMyID()), "Operation": "{}".format("null")}
        rq = requests.get("http://"+IP+':'+str(conf.IDFS_port),
                          timeout=(1, None), headers=header)
        js = rq.content.decode("utf8")
        dic = json.loads(js)
        raft_port = dic["raft_port"]
        rqlite_port = dic["http_port"]

        rqlite = dbo.rqdb(conf.my_ip)
        rqlite.join_db(IP, rqlite_port)
        rqlite.connect_db(conf.my_ip, conf.rqlite_port)
        while True:
            try:
                rqlite.add_device(ut.GetMyID())
            except:
                print("connecting..")
                time.sleep(1)
            else:
                break
        self.db = rqlite

    def put(self, file_path: str, current_path="/"):
        if os.path.isfile(file_path):
            file_name = os.path.basename(file_path)
            content_hash = ut.GetFileContentHash(file_path)
            self.db.upload_file(file_name, self.current_path, os.stat(
                file_path).st_mtime, content_hash)
            shutil.copy(file_path, os.path.join(
                current_path, content_hash))
            # not using path hash any more, just using content hash
            print("commit file {filehash}".format(
                filehash=content_hash))

        else:
            print("file not exist!")

    def get(self, file: str, prob_hash: str):
        if get.get_local(self.db, file) == False:
            while get.get_remote(self.server_ip, prob_hash) == False:
                time.sleep(0.5)
                pass
