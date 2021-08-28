import json
import os
import database.db_init
import database.db_operation
import util.tools as ut


def loadhelp():
    return """
    get put del ls cd exit
    """


global IDFS_root

if __name__ == "__main__":
    file_object = open("../config/profile.json")
    file_json = file_object.read()
    profile_data = json.loads(file_json)
    print("Hello!\nYour server address: %s\nIDFS root: %s\n" %
          (profile_data["server_address"], profile_data["IDFS_local_root"]))
    IDFS_root = profile_data["IDFS_local_root"]

    db_location = profile_data["database_file_location"]

    current_path = '/'

    db_op = database.db_operation.DB_operation(db_location)

    child_dir = db_op.lsdir(current_path)
    child_file = db_op.lsfile(current_path)

    while True:
        print("~>", end=" ")
        op = input()
        cmd = op.split()[0]
        if cmd == "help" or cmd == "?":
            print(loadhelp())
        elif cmd == "get":
            print("get")
        elif cmd == "put":
            file_name = op.split[1]
            print("Put file %d", file_name)
            db_op.put(file_name, current_path, 100, ut.GetHostName())
        elif cmd == "ls":
            print("dir:")
            print(child_dir)
            print("file:")
            print(child_file)
        elif cmd == "cd":
            target_dir = op.split[1]
            if target_dir in child_dir:
                if current_path == '/':
                    current_path = current_path+target_dir
                else:
                    current_path = current_path+'/'+target_dir
                    child_dir = db_op.lsdir(current_path)
                    child_file = db_op.lsfile(current_path)
            elif target_dir == '..':
                current_path = current_path[0:current_path.rfind('/')]
                child_dir = db_op.lsdir(current_path)
                child_file = db_op.lsfile(current_path)
        elif cmd == "del":
            del_obj=op.split[1]
            if del_obj in child_dir:
                db_op.deldir(del_obj,current_path)
            elif del_obj in child_file:
                db_op.delfile(del_obj,current_path)
        elif cmd == "init":
            database.db_init.init(db_location)
        elif cmd == "exit":
            break
        else:
            print("command not found")
