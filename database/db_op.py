import sqlite3
import hashlib
import util.tools as ut
import local.task_queue as tq
import queue
import local.task as tsk
import net.client_request as req


class DB_operation(object):
    """docstring for DB_operation."""

    def __init__(self, db_location: str):
        super(DB_operation, self).__init__()
        self.db_location = db_location
        self.conn = sqlite3.connect(db_location)
        self.cur = self.conn.cursor()

        if ut.isServer():
            self.cur.execute(
                "SELECT device_id FROM Device")
            data = self.cur.fetchall()
            for row in data:
                tq.DEVICE_TASK[row[0]] = queue.Queue(-1)

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
        self.cur.execute("INSERT INTO File VALUES('%s', '%s',%s,'%s')" % (
            file_name, file_hash, str(file_time), file_path))

        self.conn.commit()

        if is_board_cast:
            self.cur.execute(
                "SELECT device_id,device_ip FROM Device WHERE device_status='available'")
            data = self.cur.fetchall()

            for row in data:
                if ut.isServer():
                    tq.DEVICE_TASK[row[0]] = tsk.task_sql_insert_file(
                        ut.GetMyDeviceID(), file_name, file_hash, file_time, file_path)
                else:
                    req.SendTask(tsk.task_sql_insert_file(
                        ut.GetMyDeviceID(), file_name, file_hash, file_time, file_path), row[1])

    def commitPath(self, base_path: str, is_board_cast: bool):

        while True:
            now_path = base_path
            direct = ut.GetFileName(now_path)
            pp = ut.GetBasePath(now_path)
            self.cur.execute(
                "INSERET INTO Path VALUES('%s','%s')" % direct, pp)
            now_path = pp
            if direct == '/':
                break

        self.conn.commit()

        if is_board_cast:
            self.cur.execute(
                "SELECT device_id,device_ip FROM Device WHERE device_status='available'")
            data = self.cur.fetchall()

            for row in data:
                if ut.isServer():
                    tq.DEVICE_TASK[row[0]] = tsk.task_sql_update_path(
                        tsk.task_sql_update_path(ut.GetMyDeviceID()), base_path)
                else:
                    req.SendTask(
                        tsk.task_sql_update_path(ut.GetMyDeviceID(), base_path), row[1])

    def commitFileLog(self, file_hash: str, device_id: str, log_time: int, is_board_cast: bool):
        self.cur.execute("INSERT INTO Log VALUES('%s', '%s',%s)" % (
            file_hash, device_id, str(log_time)))

        if is_board_cast:
            self.cur.execute(
                "SELECT device_id,device_ip FROM Device WHERE device_status='available'")
            data = self.cur.fetchall()

            for row in data:
                log_task = tsk.task_sql_insert_log(
                    ut.GetMyDeviceID(), file_hash, device_id, log_time)
                if ut.isServer():
                    tq.DEVICE_TASK[row[0]] = log_task
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
            "INSERT INTO Device VALUES('%s', '%s', '%s', '%s', '%s')" % (
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
