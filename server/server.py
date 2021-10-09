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

client_queue=[]

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

                # write request to waiting clients
                for client in client_queue:
                    print("update request"+file)
                    client[0].send_header('Content-type', 'application/json')
                    client[0].send_header('Operation', 'upload_file')
                    client[0].end_headers()
                    client[0].wfile.write(file.encode('utf-8'))
                    client[1].release()
                    client_queue.remove(client)

            
        elif self.headers['Operation']=='get_task': # register
            self.send_response(200)
            # self.send_header('Content-type', 'application/json')
            # self.end_headers()
            cl=threading.Lock()
            client_queue.append([self,cl])
            cl.acquire() # need double aquire to lock this thread
            cl.acquire()
            # print("server OK")


        elif self.headers['Operation']=='null': # register
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            # self.wfile.write("\n".join(files_requests)) # this is the request list to string

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
            content_length = int(self.headers['Content-Length']) # <--- Gets the size of data

            post_data = self.rfile.read(content_length) 
            fd.write(post_data)
            print("upload file OK")
            fd.close()
            self.wfile.write("POST request for {}".format(self.path).encode('utf-8'))
        

class ThreadedHTTPServer(ThreadingMixIn, HTTPServer):
    """Handle requests in a separate thread."""

class IDFS_server(object):
    """docstring for IDFS_server."""
    def __init__(self):
        super(IDFS_server, self).__init__()
        self.server_instance = ThreadedHTTPServer(
            ('0.0.0.0', conf.IDFS_port), Resquest)

    def server_start(self):
        self.server_instance.serve_forever()