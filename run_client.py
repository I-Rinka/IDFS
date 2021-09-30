import client.db as dbo
import client.UI as UI
import client.http_handler as http_server
import client.back_thread as back
import util as ut
import client.config as conf
import requests
import json

connect_type = input("connect server | client | no ?\n")

if connect_type=="no":
    rqlite=dbo.rqdb(conf.my_ip)
    rqlite.start_db()
    rqlite.connect_db(conf.my_ip,conf.rqlite_port)
    rqlite.create_tables()
    rqlite.add_device(ut.GetMyID())
    # IP=conf.my_ip
else:
    IP=input("input IP:\n")
    header = {"Content-Type": "file", "Authorization": "{}".format(
    ut.GetMyID()), "Operation": "{}".format("get_file")}
    if connect_type=="client":
        rq=requests.get("http://"+IP+':'+str(conf.IDFS_port),timeout=(1,None),headers=header)
        js=rq.content.decode("utf8")
        dic=json.loads(js)
        raft_port=dic["raft_port"]
        rqlite_port=dic["http_port"]

        rqlite=dbo.rqdb(conf.my_ip)
        rqlite.join_db(IP,rqlite_port)
        rqlite.connect_db(conf.my_ip,conf.rqlite_port)
        print(raft_port)
        print(rqlite_port)
        # join db

server=http_server.http_server(rqlite)
server.start_server()

CLI=UI.client_CLI(rqlite,conf.IDFS_root,conf.my_ip)
CLI.start_cli()