import sqlite3

sql_file_table = '''CREATE TABLE FILE 
           (filename TEXT, 
            path TEXT, 
            timestamp INTEGER, 
            size INTEGER, 
            hash INTEGER
            );'''
sql_path_table = '''CREATE TABLE PATH 
           (dirname TEXT, 
            parentPath TEXT
            );'''
sql_log_table = '''CREATE TABLE LOG 
           (hash INTEGER, 
            status TEXT, 
            device TEXT, 
            timestamp INTEGER
            );'''

def init(db_file_path: str):
    conn = sqlite3.connect(db_file_path)
    cur = conn.cursor()
    
    cur.execute(sql_file_table)
    cur.execute(sql_path_table)
    cur.execute(sql_path_table)

    conn.commit()
    cur.close()
    conn.close()
    pass