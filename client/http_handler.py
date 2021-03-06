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
import requests
import client.config as conf
import client.db as abo

logging.basicConfig(level=logging.WARN)

db_op:abo.rqdb = None

def task_null_handler(device_id: str):
    # select device from database
    print("task_null:"+device_id)


def task_getfile_handler(IDFS_path: str):
    print("task_getfile:"+IDFS_path)
    print("idfs_addr:"+os.path.join("IDFS", ut.GetFileHash(IDFS_path)))


def task_postfile_handler(IDFS_path: str):
    print("task_postfile:"+IDFS_path)


class Resquest(BaseHTTPRequestHandler):
    def do_GET(self):
        file_path = urllib.parse.unquote(self.path)  # url path
        print(file_path)
        # file_hash = ut.GetFileHash(file_path)

        auth = self.headers['Authorization']

        if auth is not None:
            if db_op is not None:
                db_op.add_device(auth)
            else:
                print("database not exist!")

        if self.headers['Operation']=="get_file":
            my_file_path=os.path.join(conf.IDFS_root.replace('\\','/')+'/', file_path[1:])
            print("upload file {myfile}".format(myfile=my_file_path))

            if os.path.isfile(my_file_path): # file exists and return file
                self.send_response(200)
                self.send_header('Content-type', 'application/json')
                fd=open(my_file_path,'rb')
                self.end_headers()
                # print(fd.read())
                self.wfile.write(fd.read())
                print("file transfered end")
            else: # file not found
                self.send_response(404)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
            
        elif self.headers['Operation']=='null': # register
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            return_str=json.dumps({
                "raft_port":conf.raft_port,
                "http_port":conf.rqlite_port
            })
            self.wfile.write(return_str.encode("utf8"))

        else:
            self.send_response(404)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write("file not found".encode("utf8"))


    def do_POST(self):
        self.send_response(200)
        datas = self.rfile.read(int(self.headers['content-length']))
        task_type = None

        file_path = urllib.parse.unquote(self.path)

        try:
            task_type = self.headers['task_type']
        except:
            logging.WARN("task request error")
        else:
            if task_type == "post_file":
                task_postfile_handler(file_path)
            elif task_type == "stop":
                self.send_header('Content-type', 'application/json')
                self.end_headers()

        try:
            auth = self.headers['Authorization']
        except:
            print("no auth")
        else:
            task_null_handler(auth)

        self.send_header('Content-type', 'application/json')
        self.end_headers()


class ThreadedHTTPServer(ThreadingMixIn, HTTPServer):
    """Handle requests in a separate thread."""


class http_server(object):
    """docstring for http_server."""

    def __init__(self, db):
        super(http_server, self).__init__()
        self.server_instance = ThreadedHTTPServer(
            ('0.0.0.0', conf.IDFS_port), Resquest)
        self.server_thread:threading.Thread=None
        global db_op
        db_op=db

    def start_server(self):
        self.server_thread=threading.Thread(target=self.server_instance.serve_forever,)
        self.server_thread.start()
    
    def stop_server(self):
        if self.server_instance is not None:
            self.server_instance.server_close()
        if self.server_thread is not None:
            self.server_thread._stop()