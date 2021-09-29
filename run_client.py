my_ip="172.26.96.1"
server_ip=""
raft_port=17777
rqlite_port=17778
IDFS_port=12996

import client.db as dbo
import client.UI as UI
import client.http_handler as http_server
import client.back_thread as back
import util as ut

rqlite=dbo.rqdb(my_ip)
rqlite.start_db(raft_port,rqlite_port)
rqlite.connect_db(my_ip,rqlite_port)
rqlite.create_tables()
rqlite.add_device(ut.GetMyID())

CLI=UI.client_CLI(rqlite,"files",my_ip)
CLI.start_cli()