from http.server import HTTPServer, BaseHTTPRequestHandler
from socketserver import ThreadingMixIn
import os
import hashlib
import threading
import queue
import time
import random
import json
import urllib
import cgi
import re
import tempfile
import logging
import util as ut
import client.get_file as get
import client.db as dbo
import client.config as conf

logging.basicConfig(level=logging.WARN)

server_instance = None


def task_null_handler(device_id: str):
    # select device from database
    print("task_null:"+device_id)


def task_getfile_handler(IDFS_path: str):
    print("task_getfile:"+IDFS_path)
    print("idfs_addr:"+os.path.join("IDFS", ut.GetFileHash(IDFS_path)))


def task_postfile_handler(IDFS_path: str):
    print("task_postfile:"+IDFS_path)


def task_stop_handler():
    print("stop")
    if server_instance is not None:
        server_instance.server_close()


class Resquest(BaseHTTPRequestHandler):
    def do_GET(self):
        file_path = urllib.parse.unquote(self.path)  # url path
        print(file_path)

        auth = self.headers['Authorization']

        if auth is not None:
            task_null_handler(auth)

        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write("获取到了文件！".encode("utf8"))


class ThreadedHTTPServer(ThreadingMixIn, HTTPServer):
    """Handle requests in a separate thread."""


if __name__ == "__main__":
    server = ThreadedHTTPServer(('0.0.0.0', conf.IDFS_port), Resquest)
    
    # db=dbo.rqdb(conf.my_ip)
    # db.start_db(conf.raft_port,conf.rqlite_port)
    # db.connect_db(conf.my_ip,conf.rqlite_port)

    threading.Thread(target=server.serve_forever,).start()
    # server.serve_forever()

    for i in range(3):
        get.get_local(None,["1233"],["127.0.0.1"],["哈哈哈啊"],"/nihao/haixing.jpg")
        

