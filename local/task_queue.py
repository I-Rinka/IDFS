import queue
import threading
import local.task as tsk
import util.tools as ut
import database.db_op as dbo


MY_TASK_QUEUE = queue.Queue(maxsize=-1)

db = dbo.DB_operation(ut.GetTempPath()+'/'+ut.GetMyDeviceID()+".db")
db.create_table()

db.addDevice("d5a466a038841ad4b4d849d40454be3c",
                'available', 'Y7000P-Octo-Rinka', '192.168.71.1')
db.addDevice("eb0858f16e80bea04bca908e080f2454",
                    'available', 'ubuntu-server', '192.168.71.2')

def task_exe():
    while True:
        task = MY_TASK_QUEUE.get()
        print("我从网络上拿到了一个任务！:")
        print(task)
        if isinstance(task, tsk.task_reg):
            if not tsk.reg_dev_id == ut.GetMyDeviceID():
                db.addDevice(tsk.reg_dev_id, tsk.dev_status,
                                tsk.dev_name, tsk.dev_ip)
            print("reg")

        elif isinstance(task, tsk.task_sql):
            print("sql")
            if isinstance(task, tsk.task_sql_insert_file):
                print("file")
                db.commitFile(task.file_name, task.file_path,
                                task.file_time, task.file_hash,True)
            elif isinstance(task, tsk.task_sql_insert_log):
                print("log")
                db.commitFileLog(task.file_hash, task.device_id,
                                    task.log_time,True)
            elif isinstance(task, tsk.task_sql_update_path):
                print("path")
                db.commitPath(task.base_path)
        print("task done")
