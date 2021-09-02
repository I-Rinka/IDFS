import local.device as dvc
import util.tools as ut
import threading
import queue
import json

task_null = "task_null"
task_device_reg = "task_dev_reg"
task_upload_file = "task_upload"
task_download_file = "task_download"


CLOG_LIST = {}
TASK_QUEUE = queue.Queue(maxsize=-1)


class base_task(object):
    """docstring for base_task."""

    def __init__(self, task_type, requester_id: str):
        super(base_task, self).__init__()
        self.task_type = task_type
        self.requester_id = requester_id

    def do(self,arg):
        pass

    def toJson(self):
        return json.dumps(TaskObj2Json(self))


class task_null(base_task):
    """heart beat, do nothing"""

    def __init__(self, requester_id: str):
        super(task_null, self).__init__("task_null", requester_id)


class task_dev_reg(base_task):
    """online device information, update it into device list"""

    def __init__(self, requester_id: str, reg_device: dvc.Device):
        super(task_dev_reg, self).__init__("task_dev_reg", requester_id)
        self.target_device = dvc.Device

    def do(self):
        pass
        # device_list.find_device(self.reg_device)


class task_upload(base_task):
    """upload file to target"""

    def __init__(self, requester_id: str, target_dev: dvc.Device, file_path: str):
        super(task_upload, self).__init__("task_upload")
        self.target_dev=target_dev
        self.file_path=file_path
        if requester_id == target_dev.device_id:
            # target_dev.upload
            # device 插入数据
            return
        # if target_dev in device_list.available:
            # target_dev.upload
            pass
            # if wrong, direct_dev.upload
            # if wrong, server_dev.upload


class task_download(base_task):
    """download file from target"""

    def __init__(self, requester_id: str, target_dev: dvc.Device, file_path: str):
        super(task_download, self).__init__("task_download")
        self.target_dev=target_dev
        self.file_path=file_path
        if requester_id == target_dev.device_id:
            # target_dev.download(Get)
            return


def TaskJs2Obj(js):
    tt = js['task_type']
    if tt == 'task_null':
        return task_null()
    elif tt == 'task_upload':
        return task_upload(dvc.Device(js['target_dev']['device_name'], js['target_dev']['device_type'], js['target_dev']['device_os'], js['target_dev']['device_ip']), js['file_path'])
    return task_null()


def TaskObj2Json(task):
    basic_task = {
        "task_type": task.task_type,
        "device": dvc.DvObj2Json(task.device),
        "requester_id": task.requester_id
    }
    if task.task_type == 'task_null':
        pass
    elif task.task_type == 'task_dev_reg' or task.task_type == 'task_upload' or task.task_type == 'task_download':
        basic_task["target_dev"] = dvc.DvObj2Json(task.reg_device)
    elif task.task_type == 'task_upload' or task.task_type == 'task_download':
        basic_task["file_path"] = dvc.DvObj2Json(task.file_path)
    return basic_task
