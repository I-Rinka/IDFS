import time
import hashlib
import socket

import datetime


def GetIntTimeStamp():
    return int(time.time())

def GetFileHash(file_name: str, file_path: str, file_timestamp: int):
    return hashlib.md5(file_name+file_path+file_timestamp)

def GetHostName():
    return socket.gethostname()