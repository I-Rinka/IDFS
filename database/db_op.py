import sqlite3
import hashlib
import util.tools as ut
import local.task_server_d as td
import queue
import local.task as tsk
import net.client_request as req


class DB_operation(object):
    """docstring for DB_operation."""

    def __init__(self, db_location: str):
        super(DB_operation, self).__init__()
        self.db_location = db_location
        self.conn = sqlite3.connect(db_location, check_same_thread=False)
        self.cur = self.conn.cursor()

    def server_init_taskQ(self):
        self.cur.execute(
            "SELECT device_id FROM Device")
        data = self.cur.fetchall()
        for row in data:
            td.DEVICE_TASK[row[0]] = queue.Queue(-1)

    def lsfile(self, path: str):
        self.cur.execute(
            "SELECT file_name FROM File WHERE file_path='%s'" % (path))
        data = self.cur.fetchall()
        res = []
        for row in data:
            res.append(row[0])
        return res

    def lsdir(self, path: str):
        self.cur.execute(
            "SELECT dirname FROM Path WHERE parentPath='%s'" % (path))
        data = self.cur.fetchall()
        res = []
        for row in data:
            res.append(row[0])
        return res

    def create_table(self):
        self.conn.execute("""
        CREATE TABLE IF NOT EXISTS File
        (
        file_name VARCHAR NOT NULL,
        file_hash VARCHAR NOT NULL,
        file_timestamp INTEGER,
        file_path VARCHAR NOT NULL,
        CONSTRAINT file_pk PRIMARY KEY (file_name,file_path)
        );""")

        self.conn.execute("""
        CREATE TABLE IF NOT EXISTS Path
        (
        dirname VARCHAR NOT NULL,
        parentPath VARCHAR NOT NULL,
        CONSTRAINT path_pk PRIMARY KEY (dirname,parentPath)
        );
        """)

        self.conn.execute("""
        CREATE TABLE IF NOT EXISTS Log
        (
        file_hash VARCHAR NOT NULL,
        device_id CHAR NOT NULL,
        log_timestamp INTEGER,
        CONSTRAINT log_pk PRIMARY KEY (file_hash,device_id,log_timestamp)
        );
        """)

        self.conn.execute("""
        CREATE TABLE IF NOT EXISTS Device
        (
        device_id CHAR NOT NULL,
        device_status VARCHAR NOT NULL,
        device_name VARCHAR NOT NULL,
        device_ip VARCHAR NOT NULL,
        CONSTRAINT device_pk PRIMARY KEY (device_id)
        );
        """)

        self.conn.commit()

    def commitFile(self, file_name, file_hash, file_time, file_path, is_board_cast: bool):
        # self.cur.execute("SELECT ISNULL((SELECT top(1) 1 from File WHERE file_name=%s,file_hash=%s,file_time=%s,file_path=%s), 0)"%(
        #     file_name, file_hash, str(file_time), file_path
        # ))

        self.cur.execute("INSERT OR REPLACE INTO File VALUES('%s', '%s',%s,'%s') " % (
            file_name, file_hash, str(file_time), file_path))

        self.conn.commit()

        if is_board_cast:
            self.cur.execute(
                "SELECT device_id,device_ip FROM Device WHERE device_status='available'")
            data = self.cur.fetchall()

            for row in data:
                if ut.isServer():
                    td.DEVICE_TASK[row[0]] = tsk.task_sql_insert_file(
                        ut.GetMyDeviceID(), file_name, file_hash, file_time, file_path)
                else:
                    req.SendTask(tsk.task_sql_insert_file(
                        ut.GetMyDeviceID(), file_name, file_hash, file_time, file_path), row[1])

    def commitPath(self, base_path: str):

        dirname = ut.GetFileName(base_path)
        basepath = ut.GetBasePath(base_path)

        self.cur.execute("SELECT EXISTS(SELECT 1 FROM Path WHERE dirname='%s' AND parentPath='%s')" % (
            dirname, base_path))

        is_board_cast = False
        res = self.cur.fetchone()
        
        print(res)
        if res[0] > 0:
            print("Found!")
        else:
            print("Not found...")
            exe = "INSERT OR REPLACE INTO Path VALUES('%s','%s')" % (
                ut.GetFileName(base_path), ut.GetBasePath(base_path))
            print(exe)
            self.cur.execute(exe)
            is_board_cast = True

        self.conn.commit()
        # is_board_cast
        # print("board cast:")
        # print(is_board_cast)
            # exe = "INSERT OR REPLACE INTO Path VALUES('%s','%s')" % (
            #     ut.GetFileName(base_path), ut.GetBasePath(base_path))

        if is_board_cast:
            self.cur.execute(
                "SELECT device_id,device_ip FROM Device WHERE device_status='available'")
            data = self.cur.fetchall()
            print(data)
            for row in data:
                if ut.isServer():
                    print("Server")
                    td.DEVICE_TASK[row[0]] = tsk.task_sql_update_path(
                        tsk.task_sql_update_path(ut.GetMyDeviceID(), base_path), base_path)
                else:
                    req.SendTask(
                        tsk.task_sql_update_path(ut.GetMyDeviceID(), base_path), row[1])

    def commitFileLog(self, file_hash: str, device_id: str, log_time: int, is_board_cast: bool):
        self.cur.execute("INSERT OR REPLACE INTO Log VALUES('%s', '%s',%s)" % (
            file_hash, device_id, str(log_time)))

        if is_board_cast:
            self.cur.execute(
                "SELECT device_id,device_ip FROM Device WHERE device_status='available'")
            data = self.cur.fetchall()

            for row in data:
                log_task = tsk.task_sql_insert_log(
                    ut.GetMyDeviceID(), file_hash, device_id, log_time)
                if ut.isServer():
                    td.DEVICE_TASK[row[0]] = log_task
                else:
                    req.SendTask(log_task, row[1])

    def isFileExist(self, file_path):
        file_name = ut.GetFileName(file_name)
        file_path = ut.GetBasePath(file_name)
        self.exe("select * from File where file_name=%s and file_path=%s")
        if self.cur.fetchone is None:
            return False
        return True

    def selectFileDevice(self, file_path: str, is_server: bool):
        fpath = ut.GetBasePath(file_path)
        fname = ut.GetFileName(file_path)
        self.cur.execute("SELECT device_ip,device_id FROM Device,File,Log WHERE device_status='available' AND File.file_hash=Log.file_hash AND Log.device_id=Device.devicce_id AND File.path='%s' AND File.file_name='%s'" % (fpath, fname))
        dev_list = []

        for row in self.cur.fetchall():
            if is_server:
                dev_list.append(row[1])
            else:
                dev_list.append(row[0])
        return dev_list

    def selectNewestFileHash(self, file_path: str):
        fpath = ut.GetBasePath(file_path)
        fname = ut.GetFileName(file_path)
        self.cur.execute(
            "SELECT file_hash FROM File WHERE file_name='%s' AND file_path='%s'" % (fname, fpath))
        return self.cur.fetchall()[0][0]

    def addDevice(self, device_id: str, device_status: str, device_name: str, deivce_ip: str):
        self.cur.execute(
            "INSERT OR REPLACE INTO Device VALUES('%s', '%s', '%s', '%s')" % (
                device_id, device_status, device_name, deivce_ip)
        )
        self.conn.commit()

    def exe(self, op: str):
        self.cur.execute(op)

    def commit(self):
        self.conn.commit()

    def close(self):
        self.cur.close()
        self.conn.close()
