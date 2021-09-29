import socket
import client.db
import os


class client_CLI(object):
    """docstring for client_UI."""

    def __init__(self, db: client.db.rqdb, IDFS_root="files", my_IP=None):
        super(client_CLI, self).__init__()
        if my_IP is None:
            my_IP = socket.gethostbyname(socket.gethostname())
# current path和本机路径合体的时候注意，要把current path的'/'去掉，用current_path[1:]
# os.path.join('C:\\Users\\I_Rin\\Desktop\\IDFS\\files\\'.replace('\\','/'),'haha/xing')]
    def start_cli(self):
        current_path = '/'

        while True:
            print("~>", end=" ")
            op = input()
            cmd = ""
            if len(op.split()) > 0:
                cmd = op.split()[0]

            if cmd == "help" or cmd == "?":
                pass

            elif cmd == "put":
                pass

            elif cmd == "get":
                pass

            elif cmd == "pwd":
                print(current_path)

            elif cmd == "cd":
                target_dir = op.split()[1]

                if target_dir == '..':
                    current_path = os.path.dirname(current_path).replace('\\','/')
                elif target_dir == '.':
                    pass
                else:
                    current_path = os.path.join(current_path, target_dir).replace('\\','/')

            elif cmd == "del":
                pass

            elif cmd == "exit":
                break
            else:
                print("command not found")
