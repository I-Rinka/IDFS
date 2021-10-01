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
import server.config as conf
import client.db as abo

files_requests=[]

class Resquest(BaseHTTPRequestHandler):
    def do_GET(self):
        file_path = urllib.parse.unquote(self.path)  # url path
        print(file_path)
        auth = self.headers['Authorization']

        if self.headers['Operation']=="get_file":
            my_file_path=os.path.join(conf.IDFS_root.replace('\\','/')+'/', file_path[1:])
            print("deliver {myfile}".format(myfile=my_file_path))

            if os.path.isfile(my_file_path): # file exists and return file
                self.send_response(200)
                self.send_header('Content-type', 'application/json')
                fd=open(my_file_path,'rb')
                self.end_headers()
                self.wfile.write(fd.read())
                print("file transfered end")
                # 直接用os.state来判断时间戳是否应该删去那个文件

            else: # file not found
                self.send_response(404)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                file=file_path[1:]
                if file not in files_requests:
                    files_requests.append(file)

            
        elif self.headers['Operation']=='null': # register
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write("\n".join(files_requests)) # this is the request list to string

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
        file_hash=file_path[1:]
        self.send_header('Content-type', 'application/json')
        self.end_headers()

        if self.headers['post_file']:
            fd=open(os.path.join(conf.IDFS_root,file_hash),"wb+")
            datas = self.rfile.read(int(self.headers['content-length']))
            fd.write(datas)
            if file_hash in files_requests:
                files_requests.remove(file_hash)

        self.wfile.write("\n".join(files_requests))
        

class ThreadedHTTPServer(ThreadingMixIn, HTTPServer):
    """Handle requests in a separate thread."""

server_instance = ThreadedHTTPServer(
    ('0.0.0.0', conf.IDFS_port), Resquest)
server_instance.serve_forever()