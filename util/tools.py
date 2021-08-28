import time
import hashlib
import socket

import datetime


def GetIntTimeStamp():
    return int(time.time())


def GetFileHash(file_name: str, file_path: str, file_timestamp: int):
    hash_val = hashlib.md5(
        (file_name+file_path+str(file_timestamp)).encode('utf8')).hexdigest()
    return hash_val


def GetHostName():
    return socket.gethostname()


def ConflatePath(parent_path: str, new_dir: str):
    if parent_path == '/':
        return parent_path+new_dir
    else:
        return parent_path+'/'+new_dir

def GetParentPath(path:str):
    current_path = path[0:path.rfind('/')]
    if current_path=='':
        current_path='/'
    return current_path