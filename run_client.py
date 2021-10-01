from os import path
import client.db as dbo
import client.UI as UI
import client.http_handler as http_server
import client.back_thread as back
import util as ut
import client.config as conf
import requests
import json
import time
import client.back_thread as back_thread
import threading

connect_type = input("connect server | client | none ?\n")
# connect server means not runing database

has_database = True

if connect_type == "none":
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
    # IP=conf.my_ip
elif connect_type == "server":
    has_database = False
else:
    IP = input("input IP:\n")
    header = {"Content-Type": "file", "Authorization": "{}".format(
        ut.GetMyID()), "Operation": "{}".format("null")}
    if connect_type == "client":
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
        # join db

if has_database:
    server = http_server.http_server(rqlite)
    server.start_server()

    CLI = UI.client_CLI(rqlite, conf.IDFS_root, conf.my_ip)
    CLI.start_cli()
    # threading.Thread(target=back_thread.back_thread,).start()
    
else:
    back_thread.back_thread()