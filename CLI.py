import json
import os
import database.db_init
import database.db_operation
import util.tools as ut
import threading
import local.task as tsk
import tempfile
import shutil
import client
import net.http_request as req

clt=client

def loadhelp():
    return """
    get put mkdir pwd del ls cd exit
    """

global IDFS_root

threading.Thread()

tp = tempfile.gettempdir().replace('\\', '/')

def get_child_item(db_op: database.db_operation.DB_operation):
    db_op.commit()
    child_dir = db_op.lsdir(current_path)
    child_file = db_op.lsfile(current_path)
    return child_dir, child_file


if __name__ == "__main__":

    IDFS_root = ut.GetIDFSRoot()
    server_ip = ut.GetServerIP()

    print("Hello!\nYour server address: %s\nIDFS root: %s\n" %
          (server_ip, IDFS_root))

    current_path = '/'

    db_op = database.db_operation.DB_operation(
        server_ip, "rinka", "bltEX_01", "IDFS")


    while True:
        child_dir, child_file = get_child_item(db_op)
        print("~>", end=" ")
        op = input()
        cmd = op.split()[0]

        req.SendTask(tsk.task_null(ut.GetMyDeviceID()),ut.GetServerIP())

        if cmd == "help" or cmd == "?":
            print(loadhelp())
        elif cmd == "get":
            file_name_path = op.split()[1]
            fh = ut.GetFileHash(file_name_path)
            if os.path.exists(tp+'/'+fh):
                pass
            else:
                sema=threading.Semaphore(0)
                tsk.CLOG_LIST[fh]=sema
                sema.acquire()
            print("Get file OK")

        elif cmd == "put":
            file_name = op.split()[1]
            print("Put file %s" % file_name)
            db_op.put(file_name, current_path, 100, ut.GetHostName())

            
        elif cmd == "ls":
            print("dir:")
            print(child_dir)
            print("file:")
            print(child_file)


        elif cmd == "mkdir":
            dir_name = op.split()[1]
            db_op.mkdir(dir_name, current_path)
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
            if del_obj in child_dir:
                db_op.deldir(del_obj, current_path)
            elif del_obj in child_file:
                db_op.delfile(del_obj, current_path)
        # elif cmd == "init":
        #     database.db_init.init(db_location)
        elif cmd == "exit":
            break
        else:
            print("command not found")
