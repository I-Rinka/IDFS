import socket
import client.db
import util as ut
import os
import client.config as conf
import shutil

# When join current path with IDFS path, delete the first '/' in current path by using current_path[1:]
# like:  os.path.join('C:\\Users\\I_Rin\\Desktop\\IDFS\\files\\'.replace('\\','/'),'haha/xing')]

class client_CLI(object):
    """docstring for client_UI."""

    def __init__(self, db: client.db.rqdb, IDFS_root="files", my_IP=None):
        super(client_CLI, self).__init__()
        if my_IP is None:
            my_IP = socket.gethostbyname(socket.gethostname())
        self.IP = my_IP
        self.db: client.db.rqdb = db
        

    def start_cli(self):
        current_path = '/'
        server_ip = ""

        while True:
            print("~>", end=" ")
            op = input()
            cmd = ""
            if len(op.split()) > 0:
                cmd = op.split()[0]

            if cmd == "help" or cmd == "?":
                print("usable command:")
                print("""
                ls put get pwd cd
                """)

            if cmd == "connect":
                pass
            elif cmd=='ls':
                print(self.db.get_all_file())
            elif cmd == "put":
                if len(op.split()) > 1:
                    file_path = op.split()[1]
                else:
                    file_path = input("input file path:")

                if os.path.isfile(file_path):
                    file_name = os.path.basename(file_path)
                    content_hash = ut.GetFileContentHash(file_path)

                    # client upload db

                    shutil.copy(file_path, os.path.join(
                        conf.IDFS_root, content_hash))
                    # not using path hash any more, just using content hash
                    print("commit file {filehash}".format(
                        filehash=content_hash))

                else:
                    print("file not exist!")

            elif cmd == "get":
                if len(op.split()) > 1:
                    file_path = op.split()[1]
                else:
                    file_path = input("input file path:")
                # get process

            elif cmd == "pwd":
                print(current_path)

            elif cmd == "cd":
                target_dir = op.split()[1]

                if target_dir == '..':
                    current_path = os.path.dirname(
                        current_path).replace('\\', '/')
                elif target_dir == '.':
                    pass
                else:
                    current_path = os.path.join(
                        current_path, target_dir).replace('\\', '/')

            elif cmd == "del":
                pass

            elif cmd == "exit":
                break
            else:
                print("command not found")
