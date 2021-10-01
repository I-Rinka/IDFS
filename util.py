import hashlib
import platform
import getpass
import client.config as conf

def GetFileHash(file_path_name: str):
    hash_val = hashlib.md5(
        (file_path_name).encode('utf8')).hexdigest()
    return hash_val

def GetMyID():
    # return hashlib.md5(
    # (platform.uname().system+platform.uname().node+getpass.getuser()).encode('utf8')).hexdigest()
    # return hashlib.md5(
    # ("ubuntu20").encode('utf8')).hexdigest()
    return hashlib.md5(
    (conf.my_ip).encode('utf8')).hexdigest()

def GetFileContentHash(file_path):
    md5_hash = hashlib.md5()
    with open(file_path,"rb") as f:
        # Read and update hash in chunks of 4K
        for byte_block in iter(lambda: f.read(4096),b""):
            md5_hash.update(byte_block)
        return md5_hash.hexdigest()