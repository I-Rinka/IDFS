import client.db as db
import socket
import requests
import subprocess
import util
import sys

print(socket.gethostname())

db=db.rqdb(socket.gethostname())
db.start_db(11112,11113)
db.connect_db(socket.gethostname(),11113)

db.add_device(util.GetMyID())
# db.add_device('5687c2afc8b234501bf19ccab6ed0c0bc')

# db.upload_file('hello.txt','/',123,'123123')
print(db.get_available_device('hello.txt','/'))

db.offline_device(util.GetMyID())
print(db.get_available_device('hello.txt','/'))
