from http.server import HTTPServer, BaseHTTPRequestHandler
from socketserver import ThreadingMixIn
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
import util.tools as ut
import local.task as tsk
import local.task_queue as tq


tp = ut.GetTempPath()


class Resquest(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.headers['Operation'] == 'getfile':
            file_path = urllib.parse.unquote(self.path)

            # if db.isFileExist(file_path):
            #     self.send_response(200)
            #     auth = self.headers['Authorization']
            #     self.send_header('Content-type', 'application/json')
            #     self.end_headers()

            #     if ut.isServer():
            #         device_list = db.selectFileDevice(file_path)  # 还没实现
            #         for dev_id in device_list:
            #             tq.DEVICE_TASK[dev_id].put(
            #                 tsk.task_upload(ut.GetMyDeviceID(), file_path))

            #         sema = threading.Semaphore(0)
            #         tsk.CLOG_LIST[name_hash] = sema
            #         sema.acquire()

            #         db.commitFileLog(db.selectNewestFileHash(
            #             file_path), auth, ut.GetIntTimeStamp(), True)

            #     name_hash = ut.GetFileHash(file_path)

            #     fd = open(tp+'/'+name_hash)

            #     self.wfile.write(fd.read().encode("utf8"))

        else:
            self.send_response(200)
            auth = self.headers['Authorization']
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write("操了".encode("utf8"))
            # self.send_response(404)

    def do_POST(self):

        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()

        datas = self.rfile.read(int(self.headers['content-length']))
        # print("post:%s"%datas.decode("utf8"))

        auth = self.headers['Authorization']

        if self.headers['Operation'] == 'upfile':
            idfs_path = urllib.parse.unquote(self.path)
            print(idfs_path)
            file_hash = ut.GetFileHash(urllib.parse.unquote(self.path))
            fd = open(tp+'/'+file_hash, 'wb+')
            fd.write(datas)

            if ut.isServer():
                tsk.CLOG_LIST[file_hash].release()

        elif self.headers['Operation'] == 'task':
            js = json.loads(datas.decode("utf8"))

            task = tsk.TaskJs2Obj(js)
            tq.MY_TASK_QUEUE.put(task)
            print("net task:%s"%task.__dict__)

        if ut.isServer():
            if auth not in tq.DEVICE_TASK.keys() or tq.DEVICE_TASK[auth].empty():
                self.wfile.write(
                    str(tsk.task_null(ut.GetMyDeviceID()).__dict__).encode("utf8"))
            else:
                self.wfile.write(
                    str(tq.DEVICE_TASK[auth].get().__dict__).encode("utf8"))
        else:
            self.wfile.write(
                str(tsk.task_null(ut.GetMyDeviceID()).__dict__).encode("utf8"))


class ThreadedHTTPServer(ThreadingMixIn, HTTPServer):
    """Handle requests in a separate thread."""


LOCAL_SERVER = ThreadedHTTPServer(('0.0.0.0', ut.GetServerPort()), Resquest)
print('Starting server, use <Ctrl-C> to stop host:%s port:%s' %
      ('0.0.0.0', ut.GetServerPort()))
# server.serve_forever()
