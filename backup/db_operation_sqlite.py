import sqlite3
import hashlib
import util.tools as ut

sql_insert_dir = "INSERT INTO PATH VALUES('%s', '%s')"
sql_get_chfile = "SELECT FILE.filename FROM FILE WHERE FILE.path='%s'"
sql_get_chdir = "SELECT PATH.dirname FROM PATH WHERE PATH.parentPath='%s'"

sql_get_device = "SELECT LOG.device FROM LOG,FILE WHERE FILE.hash=LOG.hash AND FILE.filename='%s' AND FILE.path='%s'"

sql_put_file = "INSERT INTO FILE VALUES('%s', '%s','%d','%d','%s')"
sql_put_file_log = "INSERT INTO LOG VALUES('%s', '%s','%s','%d')"
sql_mkdir = "INSERT INTO PATH VALUES('%s', '%s')"
sql_del_file = "DELETE FROM FILE WHERE filename='%s' AND path='%s'"
sql_cascade_del_file = "DELETE FROM FILE WHERE path LIKE '%s'"
sql_del_dir = "DELETE FROM PATH WHERE PATH.dirname='%s' AND PATH.parentPath='%s'"


class DB_operation(object):
    """docstring for DB_operation."""

    def __init__(self, db_location: str):
        super(DB_operation, self).__init__()
        self.db_location = db_location
        self.conn = sqlite3.connect(db_location)
        self.cur = self.conn.cursor()

    def mkdir(self, cu_path: str, dir_name: str):
        self.cur.execute(sql_insert_dir % (dir_name, cu_path))

    def lsfile(self, current_path: str):
        self.cur.execute(sql_get_chfile % (current_path))
        data = self.cur.fetchall()
        res = []
        for row in data:
            res.append(row[0])
        return res

    def lsdir(self, current_path: str):
        self.cur.execute(sql_get_chdir % (current_path))
        data = self.cur.fetchall()
        res = []
        for row in data:
            res.append(row[0])
        return res

    def put(self, file_name: str, current_path: str, device_id: str):
        timestp = ut.GetIntTimeStamp()
        file_hash = ut.GetFileHash(current_path+'/'+file_name) # 这里应该是文件的记录才对
        # file_hash = ut.GetFileHash(file_name, current_path, size)
        self.cur.execute(sql_put_file %
                         (file_name, current_path, timestp, '100', file_hash))
        self.cur.execute(sql_put_file_log %
                         (file_hash, 'none', device_id, timestp))
        # 删除老记录

    def getDevice(self, file_name: str, file_path: str):
        file_hash = ut.GetFileHash(file_path+'/'+file_name)
        self.cur.execute(sql_put_file %
                         (file_name, file_path))
        data = self.cur.fetchall()
        res = []
        for row in data:
            res.append(row[0])
        return res

    def mkdir(self, dir_name: str, current_path: str):
        self.cur.execute(sql_mkdir % (dir_name, current_path))

    def delfile(self, file_name: str, file_path: str):
        self.cur.execute(sql_del_file % (file_name, file_path))

    def deldir(self, dir_name: str, parent_path: str):
        self.cur.execute(sql_del_dir % (dir_name, parent_path))
        self.cur.execute(sql_cascade_del_file %
                         (ut.ConflatePath(parent_path, dir_name)))

    def commit(self):
        self.conn.commit()

    def close(self):
        self.cur.close()
        self.conn.close()
