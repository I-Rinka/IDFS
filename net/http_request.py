import requests
import util.tools as ut
import oop.device.device as dv
import json


class Request(object):
    """docstring for Request."""

    def __init__(self, initial_connect_target: str):
        super(Request, self).__init__()
        self.protocal = "http://"
        self.next_connection_dest = initial_connect_target+':'+str(ut.GetServerPort())
        self.url = self.protocal+self.next_connection_dest

    def ChgConnectTarget(self, target_ip: str):
        self.next_connection_dest = target_ip

    def SendNullReq(self):
        header = {"Authorization": "{}".format(
            ut.GetMyDeviceID()), "Operation": "{}".format("null")}
        r = requests.get(self.url, headers=header)
        return r.text

    def SendRegReq(self, device):
        header = {"Authorization": "{}".format(
            ut.GetMyDeviceID()), "Operation": "{}".format("register")}
        payload = json.dumps(device, default=dv.DvObj2Json)
        r = requests.post(self.url,
                          headers=header, data=payload)
        # print(r.content)
        return r.text

    def UploadFile(self, file_path: str):
        header = {"Content-Type": "file", "Authorization": "{}".format(
            ut.GetMyDeviceID()), "Operation": "{}".format("upload")}

        IDFS_path = ut.GetIDFSPath(file_path)
        path_base = ut.GetBasePath(IDFS_path)

        if path_base == '/':
            path_base = ''
        # up_file = {ut.GetFileName(file_path.replace(
        #     '\\', '/')): open(file_path, 'rb')}

        # print(self.url+path_base)
        r = requests.post(self.url+IDFS_path,
                          headers=header,data=open(file_path, 'rb').read())
        print(r.headers)
        return r.text

    
    def GetFile(self, IDFS_path: str):
        header = {"Content-Type": "file", "Authorization": "{}".format(
            ut.GetMyDeviceID()), "Operation": "{}".format("getfile")}

        r = requests.get(self.url+IDFS_path,
                          headers=header)
        print(r.headers)
        return r.text
