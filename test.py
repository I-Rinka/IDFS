import requests
import util.tools as ut
import net.http_request as hr
import oop.device.device as dv
import socket

if __name__ == "__main__":
    rq = hr.Request("localhost")
    while True:
        inpt = input("输入:")
        if inpt == "exit":
            break
         
        elif inpt == '1':
            print(rq.SendNullReq())
        elif inpt == '2':
            print(rq.SendRegReq(dv.Device(ut.GetHostName(), ut.GetMyDeviceType(
            ), ut.GetMyOS(), socket.gethostbyname(socket.gethostname()))))
        elif inpt == '3':
            inpt=input("输入路径:")
            print(rq.UploadFile(inpt))
        else:
            print(rq.GetFile(inpt))

            # print(ut.GetIDFSPath(input()))