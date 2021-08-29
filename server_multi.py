from http.server import HTTPServer, BaseHTTPRequestHandler
from socketserver import ThreadingMixIn
import hashlib
import threading
import queue
import time
import random
import json
import urllib
import util.tools as ut
import cgi
import re


data = {'result': 'this is a test'}
host = ('localhost', int(ut.GetServerPort()))

IO_dic={}

def GetFileHashPF(path):
    return hashlib.md5(
        (path).encode('utf8')).hexdigest()

class Resquest(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)

        self.send_header('Content-type', 'application/json')
        self.end_headers()

        print(self.headers)

        if self.headers['Operation'] == 'getfile':
            file_hash=GetFileHashPF(urllib.parse.unquote(self.path))
            print(file_hash)
            print(urllib.parse.unquote(self.path))

            IO_dic[file_hash]=self.wfile
            sema=threading.Semaphore(0)
            IO_dic[file_hash+"_sema"]=sema
            sema.acquire()
        else:
            print("null")
            self.wfile.write("null operation")
        
        # self.wfile.write(json.dumps(data).encode())
        # print(self.headers)
        # print("auth:"+self.headers["Authorization"])

    def do_POST(self):
        self.send_response(200)
        # self.send_header('Content-type', 'application/json')
        self.send_header('Content-type', 'text')
        self.end_headers()

        addr = urllib.parse.unquote(self.path)
        print(addr)
        # addr=self.requestline[st_ed[0],st_ed[1]-1]
        # print(addr)

        datas = self.rfile.read(int(self.headers['content-length']))
        if self.headers['Operation'] == 'register':
            print(datas)
            self.wfile.write(datas)

        elif self.headers['Operation'] == 'upload':
            file_hash=GetFileHashPF(urllib.parse.unquote(self.path))

            print(file_hash)
            print(urllib.parse.unquote(self.path))
            
            if file_hash in IO_dic:
                IO_dic[file_hash].write(datas)
                IO_dic[file_hash+"_sema"].release()
                del IO_dic[file_hash]
                IO_dic[file_hash+"_sema"]


class ThreadedHTTPServer(ThreadingMixIn, HTTPServer):
    """Handle requests in a separate thread."""


if __name__ == '__main__':
    server = ThreadedHTTPServer(('localhost', ut.GetServerPort()), Resquest)
    print('Starting server, use <Ctrl-C> to stop')
    server.serve_forever()
