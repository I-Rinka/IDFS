import pyrqlite.dbapi2 as rqapi
import subprocess
import tempfile
import util
import time
import sys


class rqdb(object):
    """"""

    def __init__(self, host):
        super(rqdb, self).__init__()
        self.is_start = False
        self.rq_process = None
        self.host = host
        self.connection = None
        self.my_id = util.GetMyID()
        self.rqlited_path = "C:/Users/I_Rin/rqlited.exe"

    def start_db(self, raft_port: int, http_port: int):
        self.rq_process = subprocess.Popen([self.rqlited_path, '-raft-addr',
                                            self.host+':'+raft_port.__str__(), '-http-addr', self.host+':'+http_port.__str__(), "rqlite.log"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=False)
        self.is_start = True

    def connect_db(self, host: str, http_port: int):
        self.connection = rqapi.connect(host=host, port=http_port)
        self.is_start = True

    def close_db(self):
        self.is_start = False
        if self.rq_process is not None:
            self.rq_process.kill()
            self.rq_process = None

    def create_tables(self):
        if self.is_start and self.connection is not None:
            try:
                with self.connection.cursor() as cursor:
                    cursor.execute(  # file table
                        """
                        CREATE TABLE IF NOT EXISTS file_table(  
                        filename       TEXT    NOT NULL,  
                        path           TEXT    NOT NULL,  
                        timestamp      INT     NOT NULL,  
                        contenthash    TEXT,
                        CONSTRAINT ft_pk PRIMARY KEY(filename,path)
                        );
                        """
                    )
                    cursor.execute(  # path table
                        """
                        CREATE TABLE IF NOT EXISTS path_table(  
                        dirname        TEXT     NOT NULL,  
                        parentdir      TEXT     NOT NULL,
                        CONSTRAINT pt_pk PRIMARY KEY(dirname,parentdir)
                        );
                        """
                    )
                    cursor.execute(  # log table
                        """
                        CREATE TABLE IF NOT EXISTS log_table(
                        deviceid        TEXT     NOT NULL,  
                        timestamp       INT      NOT NULL,
                        contenthash     TEXT     NOT NULL,
                        filename       TEXT    NOT NULL,  
                        path           TEXT    NOT NULL,  
                        CONSTRAINT lt_pk PRIMARY KEY(contenthash,deviceid)
                        );
                        """
                    )
                    cursor.execute(  # device table
                        """
                        CREATE TABLE IF NOT EXISTS device_table(
                        deviceid        TEXT     NOT NULL PRIMARY KEY,  
                        status    TEXT     NOT NULL,  
                        lasttime        INT      NOT NULL,
                        deviceip    TEXT
                        );
                        """
                    )
            except:
                pass
            finally:
                pass

    def add_device(self, device_id: str):
        if self.is_start and self.connection is not None:
            try:
                with self.connection.cursor() as cursor:
                    cursor.execute(
                        """
                        INSERT OR REPLACE INTO device_table VALUES('{deviceid}','available',{lasttime},'{myip}');
                        """.format(deviceid=device_id, lasttime=int(time.time()),myip=self.host)
                    )
            finally:
                pass

    def offline_device(self, device_id: str):
        if self.is_start and self.connection is not None:
            try:
                with self.connection.cursor() as cursor:
                    cursor.execute(
                        """
                        UPDATE device_table
                        SET status='offline'
                        WHERE deviceid = '{deviceid}';
                        """.format(deviceid=device_id)
                    )
            finally:
                pass

    def upload_file(self, file_name: str, IDFS_path: str, file_time: int, content_hash: str):
        if self.is_start and self.connection is not None:
            try:
                with self.connection.cursor() as cursor:
                    cursor.execute(
                        """
                        INSERT OR REPLACE INTO file_table VALUES('{filename}','{path}',{timestamp},'{contenthash}');
                        """.format(filename=file_name, path=IDFS_path, timestamp=file_time, contenthash=content_hash)
                    )
                    cursor.execute(
                        """
                        INSERT OR REPLACE INTO log_table(deviceid,timestamp,filename,path,contenthash) VALUES ('{myid}',{logtime},'{filename}','{path}','{contenthash}');
                        """.format(myid=self.my_id, logtime=int(time.time()), filename=file_name, path=IDFS_path, contenthash=content_hash)
                    )
            finally:
                pass

    def download_file(self, file_name: str, IDFS_path: str, content_hash: str):
        if self.is_start and self.connection is not None:
            try:
                with self.connection.cursor() as cursor:
                    cursor.execute(  # file table
                        """
                        INSERT OR REPLACE INTO log_table(deviceid,timestamp,filename,path,contenthash) VALUES ('{myid}',{logtime},"{filename}","{filepath}",'{contenthash}');
                        """.format(myid=self.my_id, filename=file_name, path=IDFS_path, logtime=int(time.time()), contenthash=content_hash)
                    )
            finally:
                pass

    def get_available_device(self, file_name: str, IDFS_path: str):
        if self.is_start and self.connection is not None:
            try:
                with self.connection.cursor() as cursor:
                    cursor.execute(  # file table
                        """
                        SELECT device_table.*,log_table.contenthash FROM log_table,device_table WHERE device_table.status='available' AND log_table.filename="{filename}" AND log_table.path="{path}" AND log_table.deviceid=device_table.deviceid
                        ORDER BY log_table.timestamp DESC;
                        """.format(filename=file_name, path=IDFS_path)
                    )
                    dic=cursor.fetchall()
                    # return dic
                    dv_id=[]
                    dv_ip=[]
                    dv_file_hash=[]
                    if dic is not None:
                        for line in dic:
                            dv_id.append(line[0])
                            dv_ip.append(line[3])
                            dv_ip.append(line[4])
                    return dv_id,dv_ip,dv_file_hash
            finally:
                pass
