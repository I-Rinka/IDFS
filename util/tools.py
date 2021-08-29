import time
import hashlib
import socket
import datetime
import json
import platform

file_object = open("config/profile.json")
file_json = file_object.read()
profile_data = json.loads(file_json)


def GetServerIP():
    return profile_data["server_address"]

def GetServerPort():
    return int(profile_data["server_port"])

def GetIDFSRoot():
    return profile_data["IDFS_local_root"]

def GetMyDeviceType():
    return profile_data["device_type"]


def GetMyOS():
    return platform.system()


def GetMyDevName():
    return socket.gethostname()


my_device_id = hashlib.md5(
    (GetMyDevName()+GetMyDeviceType()+GetMyOS()).encode('utf8')).hexdigest()


def GetMyDeviceID():
    return my_device_id


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


def GetBasePath(path: str):
    current_path = path[0:path.rfind('/')]
    if current_path == '':
        current_path = '/'
    return current_path

def GetFileName(path: str):
    file_name = path[path.rfind('/')+1:]
    if file_name == '':
        file_name = '/'
    return file_name

def GetIDFSPath(local_obsolute_path:str):
    local_path=GetIDFSRoot()
    IDFS_path=local_obsolute_path[len(local_path):]
    if IDFS_path=='':
        return '/'
    if platform.system()=='Windows':
        IDFS_path=IDFS_path.replace('\\','/')
    return IDFS_path