import json
import os
import util.tools as ut
import threading
import local.task as tsk
import tempfile
import net.client_request as req
import net.listener as lsn
import local.task_queue as tq
import database.db_op as dbo
from multiprocessing import Process

db_op = dbo.DB_operation(ut.GetTempPath()+'/'+ut.GetMyDeviceID()+".db")

def f(name):
    print('hello', name)

def start_server():
    lsn.LOCAL_SERVER.serve_forever()


def loadhelp():
    return """
    get put mkdir pwd del ls cd exit
    """

# threading.Thread(target=start_server,)
p=threading.Thread(target=start_server,)
t=threading.Thread(target=tq.task_exe,)
p.start()
t.start()

global IDFS_root

server_ip = ut.GetServerIP()
server_id = ''


tp = tempfile.gettempdir().replace('\\', '/')

ut.IS_SERVER = False


def get_child_item(db_op):
    db_op.commit()
    child_dir = db_op.lsdir(current_path)
    child_file = db_op.lsfile(current_path)
    return child_dir, child_file

# 192.168.71.1
# 192.168.71.2


if __name__ == "__main__":



    IDFS_root = ut.GetIDFSRoot()
    server_ip = ut.GetServerIP()

    ut.MY_IP = input("input intranet IP address!\n:")

    print("Hello!\nYour server address: %s\nIDFS root: %s\n" %
          (server_ip, IDFS_root))

    print("My name: %s\nMy id: %s\n" % (ut.GetMyDevName(), ut.GetMyDeviceID()))
    print("Database path: %s\n" % (db_op.db_location))

    task_reg = tsk.task_reg(ut.GetMyDeviceID(), ut.GetMyDeviceID(
    ), "available", ut.GetMyDevName(), ut.GetMyIP())

    req.SendTask(task_reg, server_ip)

    current_path = '/'

    while True:
        child_dir, child_file = get_child_item(db_op)
        print("~>", end=" ")
        op = input()
        cmd = ""
        if len(op.split()) > 0:
            cmd = op.split()[0]

        if cmd == "help" or cmd == "?":
            print(loadhelp())

        elif cmd=="ping":
            req.SendTask(tsk.task_null(ut.GetMyDeviceID()),"192.168.71.2")

        elif cmd == "put":
            file_path = op.split()[1]
            file_hash = ut.GetFileContentHash(file_path)
            print(file_hash)

            if ut.GetMyOS() == 'Windows':
                file_path = file_path.replace('\\', '/')

            
            tq.MY_TASK_QUEUE.put(tsk.task_sql_insert_file(ut.GetMyDeviceID(),ut.GetFileName(file_path),file_hash,os.path.getmtime(
                file_path),current_path))

            tq.MY_TASK_QUEUE.put(tsk.task_sql_insert_log(ut.GetMyDeviceID(),file_hash,ut.GetMyDeviceID(),ut.GetIntTimeStamp()))

            print("Put file %s\nHash:%s" % (file_path, file_hash))

        elif cmd == "get":
            file_name_path = op.split()[1]
            print("Get file OK")

        elif cmd == "ls":
            print("dir:")
            print(child_dir)
            print("file:")
            print(child_file)

        elif cmd == "mkdir":
            dir_name = op.split()[1]
            tq.MY_TASK_QUEUE.put(tsk.task_sql_update_path(ut.GetMyDeviceID(),ut.ConflatePath('/', dir_name)))

        elif cmd == "pwd":
            print(current_path)

        elif cmd == "cd":
            target_dir = op.split()[1]

            if target_dir in child_dir:
                current_path = ut.ConflatePath(current_path, target_dir)

            elif target_dir == '..':
                current_path = ut.GetBasePath(current_path)
            else:
                print("Directory not exist!")

        elif cmd == "del":
            del_obj = op.split()[1]

        elif cmd == "exit":
            break
        else:
            print("command not found")
