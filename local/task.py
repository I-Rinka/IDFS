import util.tools as ut
import threading
import queue
import json

ttype_null = "task_null"
ttype_reg = "task_reg"
ttype_upload_file = "task_upload"
ttype_sql = "task_sql"


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

class task_null(base_task):
    """heart beat, do nothing"""

    def __init__(self, requester_id: str):
        super(task_null, self).__init__("task_null", requester_id)


class task_reg(base_task):
    """docstring for task_reg."""

    def __init__(self, requester_id: str, reg_dev_id: str, dev_status: str, dev_name: str, dev_ip: str):
        super(task_reg, self).__init__(ttype_reg, requester_id)
        self.requester_id = requester_id
        self.reg_dev_id = reg_dev_id
        self.dev_status = dev_status
        self.dev_name = dev_name
        self.dev_ip = dev_ip


class task_upload(base_task):
    """upload file to target"""

    def __init__(self, requester_id: str, file_path: str):
        super(task_upload, self).__init__(ttype_upload_file,requester_id)
        self.file_path = file_path


class task_sql(base_task):
    """docstring for task_sql."""

    def __init__(self, requester_id: str, sql_type: str):
        super(task_sql, self).__init__(ttype_sql,requester_id)
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
        super(task_sql_update_path, self).__init__(
            requester_id, sql_path_update)
        self.base_path = base_path


class task_sql_device_update(task_sql):
    """docstring for task_sql_device_update."""

    def __init__(self, requester_id: str,  device_id: str, status: str, ip: str):
        super(task_sql_device_update, self).__init__(
            (requester_id, sql_file_update))
        self.status = status
        self.device_id = device_id
        self.ip = ip
    

def TaskJs2Obj(js):
    tt = js['task_type']
       
    # elif tt == 'task_upload':
        # return task_upload(js['requester_id'], dvc.Device(js['target_dev']['device_name'], js['target_dev']['device_type'], js['target_dev']['device_os'], js['target_dev']['device_ip']), js['file_path'])
    if tt==ttype_reg:
        reg=task_reg(None,None,None,None,None)
        return reg.__dict__.update(js)
    elif tt==ttype_upload_file:
        reg=task_upload(None,None)
        return reg.__dict__.update(js)

    elif tt == ttype_sql:
        if js['sql_type']==sql_device_update:
            task=sql_device_update(None,None,None,None)
        elif js['sql_type']==sql_file_insert:
            task=task_sql_insert_file(None,None,None,None,None)
        elif js['sql_type']==sql_log_insert:
            task=task_sql_insert_log(None,None,None,None)
        elif js['sql_type']==sql_path_update:
            task=task_sql_update_path(None,None)
        task.__dict__.update(js)
            
        return task
    else:
        return task_null(js['requester_id'])
            