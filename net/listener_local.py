from http.server import HTTPServer, BaseHTTPRequestHandler
from socketserver import ThreadingMixIn
import local.task as tsk
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
import tempfile

tp = tempfile.gettempdir().replace('\\', '/')

data = {'result': 'this is a test'}
host = ('localhost', int(ut.GetServerPort()))

class Resquest(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)

        auth = self.headers['Authorization']

        self.send_header('Content-type', 'application/json')
        self.end_headers()

        if self.headers['Operation'] == 'getfile':
            file_path = urllib.parse.unquote(self.path)
            fh = ut.GetFileHash(file_path)
            fd = open(tp+'/'+fh)
            self.wfile.write(fd.read().encode("utf8"))

    def do_POST(self):
        self.send_response(200)

        self.send_header('Content-type', 'application/json')
        self.end_headers()

        datas = self.rfile.read(int(self.headers['content-length']))

        if self.headers['Operation'] == 'upload':
            idfs_path = urllib.parse.unquote(self.path)
            print(idfs_path)
            file_hash = ut.GetFileHash(urllib.parse.unquote(self.path))
            fd = open(tp+'/'+file_hash, 'wb+')
            fd.write(datas)

        elif self.headers['Operation'] == 'task':
            # js=data.
            print(datas)
            # tsk.TASK_QUEUE.put()


class ThreadedHTTPServer(ThreadingMixIn, HTTPServer):
    """Handle requests in a separate thread."""



LOCAL_SERVER = ThreadedHTTPServer(('localhost', ut.GetServerPort()), Resquest)
print('Starting server, use <Ctrl-C> to stop')
# server.serve_forever()
