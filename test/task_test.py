import local.task as tsk
import local.device as dv
import json


upl=tsk.task_upload(dv.Device("sam","phone","windows","127.0.0.1"),"/new_dir/new file.txt")
jstr=json.dumps(upl,default=tsk.TaskObj2Json)
print(jstr)
task=tsk.TaskJs2Obj(json.loads(jstr))
print(task.target_dev.device_type)
