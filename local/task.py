import util.tools as ut
import threading
import queue
import json

task_null = "task_null"
task_reg = "task_reg"
task_upload_file = "task_upload"
task_sql = "task_sql"


sql_file_update = "sql_file_update"
sql_device_update = "sql_device_update"
sql_file_insert = "sql_file_insert"
sql_log_insert = "sql_log_insert"
sql_path_update = "sql_path_update"


class base_task(object):
    """docstring for base_task."""

    def __init__(self, task_type, requester_id: str):
        super(base_task, self).__init__()
        self.task_type = task_type
        self.requester_id = requester_id

    def toJson(self):
        return json.loads(TaskObj2Json(self))


class task_null(base_task):
    """heart beat, do nothing"""

    def __init__(self, requester_id: str):
        super(task_null, self).__init__("task_null", requester_id)


class task_reg(base_task):
    """docstring for task_reg."""

    def __init__(self, requester_id: str, reg_dev_id: str, dev_status: str, dev_name: str, dev_ip: str):
        super(task_reg, self).__init__(task_reg, requester_id)
        self.requester_id = requester_id
        self.reg_dev_id = reg_dev_id
        self.dev_status = dev_status
        self.dev_name = dev_name
        self.dev_ip = dev_ip


class task_upload(base_task):
    """upload file to target"""

    def __init__(self, requester_id: str, target_dev: dvc.Device, file_path: str):
        super(task_upload, self).__init__("task_upload")
        self.target_dev = target_dev
        self.file_path = file_path


class task_sql(base_task):
    """docstring for task_sql."""

    def __init__(self, requester_id: str, sql_type: str):
        super(task_sql, self).__init__(task_sql)
        self.sql_type = sql_type


class task_sql_insert_file(task_sql):
    """docstring for sql_insert_file."""

    def __init__(self, requester_id: str, file_name: str, file_hash: str, file_time: int, file_path: str):
        super(task_sql_insert_file, self).__init__(
            requester_id, sql_file_insert)
        self.file_name = file_name
        self.file_path = file_path
        self.file_time = file_time
        self.file_hash = file_hash


class task_sql_insert_log(task_sql):
    """docstring for task_sql_insert_log."""

    def __init__(self,  requester_id: str, file_hash: str, device_id: str, log_time: int):
        super(task_sql_insert_log, self).__init__(
            requester_id, sql_file_insert)
        self.file_hash = file_hash
        self.device_id = device_id
        self.log_time = log_time


class task_sql_update_path(task_sql):
    """docstring for task_sql_insert_log."""

    def __init__(self, requester_id: str, base_path: str):
        super(task_sql_insert_log, self).__init__(
            requester_id, sql_file_insert)
        self.base_path = base_path


class sql_device_update(task_sql):
    """docstring for sql_device_update."""

    def __init__(self, requester_id: str,  device_id: str, status: str, ip: str):
        super(sql_device_update, self).__init__(
            (requester_id, sql_file_update))
        self.status = status
        self.device_id = device_id
        self.ip = ip

    # def do(self, sql_op):
    #     sql_op.exe("update Device set device_status='%s',device_ip='%s' where device_id='%s'" % (
    #         self.status, self.ip, self.device_id))
    #     sql_op.commit()


def TaskJs2Obj(js):
    tt = js['task_type']
    if tt == 'task_null':
        return task_null()
    elif tt == 'task_upload':
        return task_upload(js['requester_id'], dvc.Device(js['target_dev']['device_name'], js['target_dev']['device_type'], js['target_dev']['device_os'], js['target_dev']['device_ip']), js['file_path'])
    elif tt == task_sql:
        sql = js["sql_type"]
        if sql == sql_device_update:
            return sql_file_update(js["requester_id"], js["device_id"], js["status"], js["ip"])
        elif sql == sql_file_update:
            return sql_file_update(js["requester_id"], js["file_name"], js["file_path"], js["file_hash"], js["file_time"], js["device_id"], js["time_stamp"])

    return task_null()


def TaskObj2Json(task):
    return task.__dict__
    # basic_task = {
    #     "task_type": task.task_type,
    #     "requester_id": task.requester_id
    # }
    # if task.task_type == 'task_null':
    #     pass

    # elif task.task_type == task_reg:
    #     base_task["requester_id"] = task.requester_id
    #     base_task["reg_dev_id"] = task.reg_dev_id
    #     base_task["dev_status"] = task.dev_status
    #     base_task["dev_name"] = task.dev_name
    #     base_task["dev_ip"] = task.dev_ip

    # elif task.task_type == task_upload:
    #     base_task["target_dev"] = task.target_dev
    #     base_task["file_path"] = task.file_path

    # elif task.task_type == task_sql:
    #     basic_task["sql_type"] = task.sql_type
    #     if task.sql_type == sql_file_update:
    #         base_task["file_name"] = task.file_name
    #         base_task["file_path"] = task.file_path
    #         base_task["file_time"] = task.file_time
    #         base_task["file_hash"] = task.file_hash
    #         base_task["device_id"] = task.device_id
    #         base_task["time_stamp"] = task.time_stamp

    #     elif task.sql_type == sql_device_update:
    #         base_task["status"] = task.status
    #         base_task["device_id"] = task.device_id
    #         base_task["ip"] = task.ip

    # return basic_task
