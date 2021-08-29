import local.device as devc
import threading
import queue
import json

task_null = "task_null"
task_device_reg = "task_dev_reg"
task_upload_file = "task_upload"
task_download_file = "task_download"


class base_task(object):
    """docstring for base_task."""

    def __init__(self, task_type):
        super(base_task, self).__init__()
        self.task_type = task_type

    def do(self):
        pass

    def toJson(self):
        return json.dumps(TaskObj2Json(self))


class task_null(base_task):
    """heart beat, do nothing"""

    def __init__(self):
        super(task_null, self).__init__("task_null")


class task_dev_reg(base_task):
    """online device information, update it into device list"""

    def __init__(self, device: devc.Device):
        super(task_dev_reg, self).__init__("task_dev_reg")
        self.device = device


class task_upload(base_task):
    """upload file to target"""

    def __init__(self, target_dev: devc.Device, file_path: str):
        super(task_upload, self).__init__("task_upload")
        self.target_dev = target_dev
        self.file_path = file_path


class task_download(base_task):
    """download file from target"""

    def __init__(self, target_dev: devc.Device, file_path: str):
        super(task_download, self).__init__("task_download")
        self.task_download = task_download
        self.file_path = file_path
        self.target_dev = target_dev


def TaskJs2Obj(js):
    tt = js['task_type']
    if tt == 'task_null':
        return task_null()
    elif tt == 'task_upload':
        return task_upload(devc.Device(js['target_dev']['device_name'], js['target_dev']['device_type'], js['target_dev']['device_os'], js['target_dev']['device_ip']), js['file_path'])
    return task_null()


def TaskObj2Json(tsk):
    if tsk.task_type == 'task_null':
        return {"task_type": 'task_null'}
    elif tsk.task_type == 'task_upload':
        return {
            "task_type": 'task_upload',
            "target_dev": devc.DvObj2Json(tsk.target_dev),
            "file_path": tsk.file_path
        }
    return {"task_type": 'task_null'}
