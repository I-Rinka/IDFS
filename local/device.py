import hashlib
import util.tools as ut
import local.task as tsk
import net.http_request as rq


def GetDeviceID(device_name: str, device_type: str, device_os: str):
    return hashlib.md5(
        (device_name+device_type+device_os).encode('utf8')).hexdigest()


device_phone = "phone"
device_server = "server"
device_laptop = "laptop"


class Device():
    """parent object for all device"""

    def __init__(self, device_name: str, device_type: str, device_os: str, device_ip: str):
        self.device_name = device_name
        self.device_type = device_type
        self.device_os = device_os
        self.device_ip = device_ip
        self.device_id = GetDeviceID(device_name, device_type, device_os)
        self.device_last_login_time = ut.GetIntTimeStamp()

    def submit_task(self, task: tsk.base_task):
        return rq.SendTask(task, self.device_ip)

    def upload_file(self, os_path: str):
        return rq.UploadFile(os_path, self.device_ip)

    def download_file(self, idfs_path: str):
        pass


def DvObj2Json(obj):
    return{
        "device_name": obj.device_name,
        "device_type": obj.device_type,
        "device_os": obj.device_os,
        "device_ip": obj.device_ip,
        "device_id": GetDeviceID(obj.device_name, obj.device_type, obj.device_os),
        "device_last_login_time": obj.device_last_login_time
    }
