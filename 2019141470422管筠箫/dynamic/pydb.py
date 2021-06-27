from pymysql import *


class MysqlFunc:
    def __init__(self):
        self.conn = connect(host='localhost', port=3306, user='root', password='gyx110401', database='stock',
                       charset='utf8')
        # 创建cursor对象
        self.cs = self.conn.cursor()

    def close(self):
        # 关闭cursor对象
        self.cs.close()
        self.conn.close()

    def execute_sql(self, sql):
        self.cs.execute(sql)
