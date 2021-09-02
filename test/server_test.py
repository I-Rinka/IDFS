import requests
import util.tools as ut
import net.http_request as hr
import local.device as dv
import socket
import local.task as tsk

rq = hr.Request("localhost")
while True:
    inpt = input("输入:")
    if inpt == "exit":
        break

    elif inpt == '1':
        txt = rq.SendNullReq()
        task = tsk.TaskJs2Obj(txt)
        # if task.task_type != tsk.task_null:
            

    elif inpt == '2':
        print(rq.SendRegReq(dv.Device(ut.GetHostName(), ut.GetMyDeviceType(
        ), ut.GetMyOS(), socket.gethostbyname(socket.gethostname()))))
    elif inpt == '3':
        inpt = input("输入路径:")
        print(rq.UploadFile(inpt))
    elif inpt == '4':
        inpt = input("输入IDFS路径:")
        print(rq.GetFile(inpt))
    # else:

        # print(ut.GetIDFSPath(input()))
