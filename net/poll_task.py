import net.http_request as req
import util.tools as ut
import local.task as tsk
import local.task_driver as td
import time

def fetch_task():
    # 后续可以从各种设备里面拿数据
    req = req.Request(ut.GetServerIP())
    while True:
        txt = req.SendNullReq()
        task = tsk.TaskJs2Obj(txt)
        if task.task_type != tsk.task_null:
            td.TASK_QUEUE.put(task)
        time.sleep(1)

