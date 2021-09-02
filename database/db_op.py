import sqlite3
import hashlib
import util.tools as ut

sql_insert_dir = "INSERT INTO PATH VALUES('%s', '%s')"
sql_get_chfile = "SELECT FILE.filename FROM FILE WHERE FILE.path='%s'"
sql_get_chdir = "SELECT PATH.dirname FROM PATH WHERE PATH.parentPath='%s'"

sql_get_device = "SELECT LOG.device FROM LOG,FILE WHERE FILE.hash=LOG.hash AND FILE.filename='%s' AND FILE.path='%s'"


class DB_operation(object):
    """docstring for DB_operation."""

    def __init__(self, db_location: str):
        super(DB_operation, self).__init__()
        self.db_location = db_location
        self.conn = sqlite3.connect(db_location)
        self.cur = self.conn.cursor()

    def mkdir(self, cu_path: str, dir_name: str):
        self.cur.execute("INSERT INTO PATH VALUES('%s', '%s')" % (dir_name, cu_path))

    def lsfile(self, current_path: str):
        self.cur.execute("SELECT FILE.filename FROM FILE WHERE FILE.path='%s'" % (current_path))
        data = self.cur.fetchall()
        res = []
        for row in data:
            res.append(row[0])
        return res

    def lsdir(self, current_path: str):
        self.cur.execute("SELECT PATH.dirname FROM PATH WHERE PATH.parentPath='%s'" % (current_path))
        data = self.cur.fetchall()
        res = []
        for row in data:
            res.append(row[0])
        return res

    def put(self, file_name: str, current_path: str, device_id: str):
        timestp = ut.GetIntTimeStamp()
        file_hash = ut.GetFileHash(current_path+'/'+file_name) # 这里应该是文件的记录才对
        # file_hash = ut.GetFileHash(file_name, current_path, size)
        self.cur.execute("INSERT INTO FILE VALUES('%s', '%s','%d','%d','%s')" %
                         (file_name, current_path, timestp, '100', file_hash))
        self.cur.execute("INSERT INTO LOG VALUES('%s', '%s','%s','%d')" %
                         (file_hash, 'none', device_id, timestp))
        # 删除老记录

    def getDevice(self, file_name: str, file_path: str):
        # file_hash = ut.GetFileHash(file_path+'/'+file_name)
        # self.cur.execute( %
        #                  (file_name, file_path))
        # data = self.cur.fetchall()
        # res = []
        # for row in data:
        #     res.append(row[0])
        return res

    def mkdir(self, dir_name: str, current_path: str):
        self.cur.execute("INSERT INTO PATH VALUES('%s', '%s')" % (dir_name, current_path))

    def delfile(self, file_name: str, file_path: str):
        self.cur.execute("DELETE FROM FILE WHERE filename='%s' AND path='%s'" % (file_name, file_path))

    def deldir(self, dir_name: str, parent_path: str):
        self.cur.execute("DELETE FROM PATH WHERE PATH.dirname='%s' AND PATH.parentPath='%s'" % (dir_name, parent_path))
        self.cur.execute("DELETE FROM FILE WHERE path LIKE '%s'" %
                         (ut.ConflatePath(parent_path, dir_name)))

    def commit(self):
        self.conn.commit()

    def close(self):
        self.cur.close()
        self.conn.close()
