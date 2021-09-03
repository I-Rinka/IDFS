import json
import os
import util.tools as ut
import threading
import local.task as tsk
import tempfile
import net.client_request as req
import net.listener as lsn

from multiprocessing import Process

def f(name):
    print('hello', name)

def start_server():
    lsn.LOCAL_SERVER.serve_forever()


def loadhelp():
    return """
    get put mkdir pwd del ls cd exit
    """

# threading.Thread(target=start_server,)
p=Process(target=start_server,)
p.start()

global IDFS_root

server_ip = ut.GetServerIP()
server_id = ''


tp = tempfile.gettempdir().replace('\\', '/')

db_op = lsn.db

ut.IS_SERVER = False


def get_child_item(db_op):
    db_op.commit()
    child_dir = db_op.lsdir(current_path)
    child_file = db_op.lsfile(current_path)
    return child_dir, child_file

# 192.168.71.1
# 192.168.71.2


if __name__ == "__main__":

    db_op.addDevice("d5a466a038841ad4b4d849d40454be3c",
                    'available', 'Y7000P-Octo-Rinka', '192.168.71.1')
    db_op.addDevice("eb0858f16e80bea04bca908e080f2454",
                    'available', 'ubuntu-server', '192.168.71.2')

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

            db_op.commitFile(ut.GetFileName(file_path), file_hash, os.path.getmtime(
                file_path), current_path, True)
            db_op.commitFileLog(file_hash, ut.GetMyDeviceID(),
                                ut.GetIntTimeStamp(), True)

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
            db_op.commitPath(ut.ConflatePath('/', dir_name), True)

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
