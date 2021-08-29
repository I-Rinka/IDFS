from http.server import HTTPServer, BaseHTTPRequestHandler
import json
import urllib
import util.tools as ut
import cgi
import re

data = {'result': 'this is a test'}
host = ('localhost', int(ut.GetServerPort()))


class Resquest(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps(data).encode())
        print(self.headers)
        # print("auth:"+self.headers["Authorization"])

    def do_POST(self):
        self.send_response(200)
        # self.send_header('Content-type', 'application/json')
        self.send_header('Content-type', 'text')
        self.end_headers()
        print(self.headers)

        print("地址：")
        st_ed = re.findall('\s.*\s', self.requestline, flags=0)
        addr=st_ed[0][1:]
        addr=urllib.parse.unquote(addr)
        print(addr)
        # addr=self.requestline[st_ed[0],st_ed[1]-1]
        # print(addr)

        datas = self.rfile.read(int(self.headers['content-length']))
        if self.headers['Operation'] == 'register':
            print(datas)
            self.wfile.write(datas)

        elif self.headers['Operation'] == 'upload':
            open("%s" % "收到的文件", "wb+").write(datas)


if __name__ == '__main__':
    server = HTTPServer(host, Resquest)
    print("Starting server, listen at: %s:%s" % host)
    server.serve_forever()
