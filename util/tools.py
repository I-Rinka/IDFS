import time
import hashlib
import socket

import datetime


def GetIntTimeStamp():
    return int(time.time())

def GetFileHash(file_name: str, file_path: str, file_timestamp: int):
    hash_val=hashlib.md5((file_name+file_path+str(file_timestamp)).encode('utf8')).hexdigest()

def GetHostName():
    return socket.gethostname()