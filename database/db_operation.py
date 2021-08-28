import sqlite3
import hashlib
import util.tools as ut

sql_insert_dir = "INSERT INTO PATH VALUES('%s', '%s')"
sql_get_chfile = "SELECT FILE.filename FROM FILE WHERE FILE.path=%s"
sql_get_chdir = "SELECT PATH.dirname FROM PATH WHERE PATH.parentPath=%s"
sql_put_file = "INSERT INTO FILE VALUES('%s', '%s','%d','%d','%d')"
sql_put_file_log = "INSERT INTO FILE VALUES('%d', '%s','%s','%d')"
sql_del_file = "DELETE FROM FILE WHERE filename=%s AND path=%s"
sql_del_dir = "DELETE FROM FILE , PATH WHERE FILE.path=%s AND PATH.dirname=%s AND PATH.parentPath=%s"


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
        self.cur.execute(sql_get_chfile % (current_path, current_path))
        return self.cur.fetchall()

    def lsdir(self, current_path: str):
        self.cur.execute(sql_get_chdir % (current_path, current_path))
        return self.cur.fetchall()

    def put(self, file_name: str, current_path: str, size: int, device: str):
        timestp = ut.GetIntTimeStamp()
        self.cur.execute(sql_put_file %
                         (file_name, current_path, timestp, size, ut.GetFileHash(file_name, current_path, size)))
        self.cur.execute(sql_put_file_log %
                         (timestp, 'uploading', device, timestp))

    def delfile(self, file_name: str, file_path: str):
        self.cur.execute(sql_del_file % (file_name, file_path))

    def deldir(self, dir_name: str, parent_path: str):
        self.cur.execute(sql_del_dir %
                         (dir_name+'/'+parent_path, dir_name, parent_path))

    def commit(self):
        self.conn.commit()
