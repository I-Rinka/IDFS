import oop.device.device as devc
import threading
import queue

task_null = "null"
task_device_reg = "dev_register"
task_upload_file = "upload"
task_download_file = "download"


class base_task(object):
    """docstring for base_task."""

    def __init__(self, task_type):
        super(base_task, self).__init__()
        self.task_type = task_type

    def do(self):
        pass


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
