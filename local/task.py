import local.device as dvc
import util.tools as ut
import threading
import queue
import json
import database.db_op as dbo

task_null = "task_null"
task_device_reg = "task_dev_reg"
task_upload_file = "task_upload"
task_download_file = "task_download"
task_sql = "task_sql"


sql_file_update = "sql_file_update"
sql_device_update = "sql_device_update"

CLOG_LIST = {}
TASK_QUEUE = queue.Queue(maxsize=-1)


class base_task(object):
    """docstring for base_task."""

    def __init__(self, task_type, requester_id: str):
        super(base_task, self).__init__()
        self.task_type = task_type
        self.requester_id = requester_id

    def do(self, arg):
        pass

    def toJson(self):
        return json.dumps(TaskObj2Json(self))


class task_null(base_task):
    """heart beat, do nothing"""

    def __init__(self, requester_id: str):
        super(task_null, self).__init__("task_null", requester_id)


# class task_dev_reg(base_task):
#     """online device information, update it into device list"""

#     def __init__(self, requester_id: str, reg_device: dvc.Device):
#         super(task_dev_reg, self).__init__("task_dev_reg", requester_id)
#         self.target_device = dvc.Device

#     def do(self):
#         pass
        # device_list.find_device(self.reg_device)


# class task_upload(base_task):
#     """upload file to target"""

#     def __init__(self, requester_id: str, target_dev: dvc.Device, file_path: str):
#         super(task_upload, self).__init__("task_upload")
#         self.target_dev = target_dev
#         self.file_path = file_path
#         if requester_id == target_dev.device_id:
#             # target_dev.upload
#             # device 插入数据
#             return
#         # if target_dev in device_list.available:
#             # target_dev.upload
#             pass
#             # if wrong, direct_dev.upload
#             # if wrong, server_dev.upload


# class task_download(base_task):
#     """download file from target"""

#     def __init__(self, requester_id: str, target_dev: dvc.Device, file_path: str):
#         super(task_download, self).__init__("task_download")
#         self.target_dev = target_dev
#         self.file_path = file_path
#         if requester_id == target_dev.device_id:
#             # target_dev.download(Get)
#             return


class task_sql(base_task):
    """docstring for task_sql."""

    def __init__(self, requester_id: str, sql_type: str):
        super(task_download, self).__init__(task_sql)
        self.sql_type = sql_type

    def do(self, sql_op):
        pass


class sql_file_update(task_sql):
    """docstring for sql_file_update."""

    def __init__(self, requester_id: str, file_name: str, file_path: str, file_hash: str, file_time: int, device_id: str, time_stamp: str):
        super(sql_file_update, self).__init__(requester_id, sql_file_update)
        self.file_name = file_name
        self.file_path = file_path
        self.file_time = file_time
        self.file_hash = file_hash
        self.device_id = device_id
        self.time_stamp = time_stamp

    def do(self, sql_op):
        sql_op.exe("insert into File values('%s','%s',%s,'%s')" % (
            self.file_name, self.file_hash, str(self.file_time), self.file_path))
        sql_op.exe("insert into Path values('%s','%s')" %
                   (self.file_path, ut.GetBasePath(self.file_path)))
        sql_op.exe("insert into Log values('%s','%s','%s')" %
                   (self.file_hash, self.device_id, self.time_stamp))
        sql_op.commit()


class sql_device_update(task_sql):
    """docstring for sql_device_update."""

    def __init__(self, requester_id: str,  device_id: str, status: str, ip: str):
        super(sql_device_update, self).__init__(
            (requester_id, sql_file_update))
        self.status = status
        self.device_id = device_id
        self.ip = ip

    def do(self, sql_op):
        sql_op.exe("update Device set device_status='%s',device_ip='%s' where device_id='%s'" % (
            self.status, self.ip, self.device_id))
        sql_op.commit()


def TaskJs2Obj(js):
    tt = js['task_type']
    if tt == 'task_null':
        return task_null()
    elif tt == 'task_upload':
        return task_upload(dvc.Device(js['target_dev']['device_name'], js['target_dev']['device_type'], js['target_dev']['device_os'], js['target_dev']['device_ip']), js['file_path'])
    elif tt == task_sql:
        sql = js["sql_type"]
        if sql == sql_device_update:
            return sql_file_update(js["requester_id"], js["device_id"], js["status"], js["ip"])
        elif sql == sql_file_update:
            return sql_file_update(js["requester_id"], js["file_name"], js["file_path"], js["file_hash"], js["file_time"], js["device_id"], js["time_stamp"])

    return task_null()


def TaskObj2Json(task):
    basic_task = {
        "task_type": task.task_type,
        "requester_id": task.requester_id
    }
    if task.task_type == 'task_null':
        pass
    elif task.task_type == 'task_dev_reg' or task.task_type == 'task_upload' or task.task_type == 'task_download':
        basic_task["target_dev"] = dvc.DvObj2Json(task.reg_device)
    elif task.task_type == 'task_upload' or task.task_type == 'task_download':
        basic_task["file_path"] = dvc.DvObj2Json(task.file_path)
    elif task.task_type == task_sql:
        basic_task["sql_type"] = task.sql_type
        if task.sql_type == sql_file_update:
            base_task["file_name"]=task.file_name
            base_task["file_path"]=task.file_path
            base_task["file_time"]=task.file_time
            base_task["file_hash"]=task.file_hash
            base_task["device_id"]=task.device_id
            base_task["time_stamp"]=task.time_stamp

        elif task.sql_type == sql_device_update:
            base_task["status"]=task.status
            base_task["device_id"]=task.device_id
            base_task["ip"]=task.ip
        
    return basic_task
