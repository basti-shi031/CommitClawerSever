import sqlite3


class CommitCache(object):

    def __init__(self):
        self.conn = sqlite3.connect("commitDb.db")
        self.cursor = self.conn.cursor()
        self.create_commit_table()

    def execute(self, sql):
        self.cursor.execute(sql)
        return self.cursor.fetchall()

    # 新建一张表
    def create_commit_table(self):
        tb_exists = "SELECT name FROM sqlite_master WHERE type='table' AND name='commit_table'"
        if not self.conn.execute(tb_exists).fetchone():
            self.execute(
                'create table commit_table (id  integer PRIMARY KEY autoincrement, commit_hash varchar(60),project_name varchar(60))')
            self.conn.commit()

    # 关闭
    def close(self):
        self.cursor.close()
        self.conn.close

    # 添加一个commit_hash记录
    def add_commit_hash(self, commit_hash1, project_name1):
        sql = ''' insert into commit_table
              (commit_hash,project_name)
              values
              (:st_commit,:st_project_name)'''
        # 把数据保存到name username和 id_num中
        self.cursor.execute(sql, {'st_commit': commit_hash1, 'st_project_name': project_name1})
        self.conn.commit()

    def find(self, commit_hash):
        sql = 'select * from commit_table where commit_hash=?'
        return len(self.cursor.execute(sql, (commit_hash,)).fetchall()) > 0
