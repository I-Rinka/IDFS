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

import task as tsk
import util as ut

logging.basicConfig(level=logging.WARN)

server_instance=None

def task_null_handler(device_id: str):
    # select device from database
    print("task_null:"+device_id)


def task_getfile_handler(IDFS_path: str):
    print("task_getfile:"+IDFS_path)
    print("idfs_addr:"+os.path.join("IDFS",ut.GetFileHash(IDFS_path)))


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
        file_hash=ut.GetFileHash(file_path)

        auth = self.headers['Authorization']

        if auth is not None:
            task_null_handler(auth)

        if os.path.isfile(os.path.join("IDFS",file_hash)):
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write("有！".encode("utf8"))
        else:
            self.send_response(404)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write("not found".encode("utf8"))

        
 

    def do_POST(self):
        self.send_response(200)
        datas = self.rfile.read(int(self.headers['content-length']))
        task_type = None

        file_path = urllib.parse.unquote(self.path)

        try:
            task_type = self.headers['task_type']
            assert (task_type in tsk.local_task_type), "task not in type"
        except:
            logging.WARN("task request error")
        else:
            if task_type == "post_file":
                task_postfile_handler(file_path)
            elif task_type == "stop":
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                task_stop_handler()

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


# LOCAL_SERVER = ThreadedHTTPServer(('0.0.0.0', ut.GetServerPort()), Resquest)
# print('Starting server, use <Ctrl-C> to stop host:%s port:%s' %
#       ('0.0.0.0', ut.GetServerPort()))
# server.serve_forever()
