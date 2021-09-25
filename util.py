import hashlib
import platform
import getpass

def GetFileHash(file_path_name: str):
    hash_val = hashlib.md5(
        (file_path_name).encode('utf8')).hexdigest()
    return hash_val

def GetMyID():
    return hashlib.md5(
    (platform.uname().system+platform.uname().node+getpass.getuser()).encode('utf8')).hexdigest()

