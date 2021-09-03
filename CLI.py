import json
import os
import util.tools as ut
import threading
import local.task as tsk
import tempfile
import net.client_request as req


def loadhelp():
    return """
    get put mkdir pwd del ls cd exit
    """


global IDFS_root

server_ip = ut.GetServerIP()

threading.Thread()

tp = tempfile.gettempdir().replace('\\', '/')

# def get_child_item(db_op):
#     db_op.commit()
#     child_dir = db_op.lsdir(current_path)
#     child_file = db_op.lsfile(current_path)
#     return child_dir, child_file


if __name__ == "__main__":

    IDFS_root = ut.GetIDFSRoot()
    server_ip = ut.GetServerIP()

    print("Hello!\nYour server address: %s\nIDFS root: %s\n" %
          (server_ip, IDFS_root))

    print("My name: %s\nMy id: %s\n" % (ut.GetMyDevName(), ut.GetMyDeviceID()))

    current_path = '/'

    while True:
        # child_dir, child_file = get_child_item(db_op)
        print("~>", end=" ")
        op = input()
        cmd = op.split()[0]

        if cmd == "help" or cmd == "?":
            print(loadhelp())

        elif cmd == "reg":
            task_reg = tsk.task_reg(ut.GetMyDeviceID(), ut.GetMyDeviceID(
            ), "available", ut.GetMyDevName(), "192.168.71.1")
            req.SendTask(task_reg,server_ip)

        elif cmd == "put":
            file_name = op.split()[1]
            print("Put file %s" % file_name)

            # db_op.put(file_name, current_path, 100, ut.GetHostName())

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
