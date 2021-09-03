import requests
import util.tools as ut
import json
import local.task as tsk


protocal = "http://"
port = str(ut.GetServerPort())


def SendTask(task: tsk.base_task, ip: str):
    print("Send task\n%s\nto %s" % (task.__dict__, protocal+ip+':'+port))

    if ip == ut.GetMyIP():
        pass
        return ""
    else:
        header = {"Authorization": "{}".format(
            ut.GetMyDeviceID()), "Operation": "{}".format("task")}
        print(task.__dict__)
        payload = json.dumps(task.__dict__)
        r = requests.post(protocal+ip+':'+port,
                          headers=header, data=payload, timeout=5)
        print(r.content)
        print(r.status_code)
        return r.text


def UploadFile(file_path: str, ip: str):
    header = {"Content-Type": "file", "Authorization": "{}".format(
        ut.GetMyDeviceID()), "Operation": "{}".format("upfile")}

    IDFS_path = ut.GetIDFSPath(file_path)
    path_base = ut.GetBasePath(IDFS_path)

    if path_base == '/':
        path_base = ''

    r = requests.post(protocal+ip+':'+port+IDFS_path,
                      headers=header, data=open(file_path, 'rb').read())
    # print(r.headers)
    return r.text


def GetFile(IDFS_path: str, ip: str):
    header = {"Content-Type": "file", "Authorization": "{}".format(
        ut.GetMyDeviceID()), "Operation": "{}".format("getfile")}

    r = requests.get(protocal+ip+':'+port+IDFS_path,
                     headers=header)

    # print(r.headers)
    return r.text
