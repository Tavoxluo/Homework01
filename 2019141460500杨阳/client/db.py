from pymysql import connect
from config import *


class DB(object):
    def __init__(self):
        # 连接数据库
        self.conn = connect(host=DB_HOST,
                            port=DB_PORT,
                            database=DB_NAME,
                            user=DB_USER,
                            password=DB_PASS)

        # 获取游标
        self.cursor = self.conn.cursor()

    def close(self):
        self.cursor.close()
        self.conn.close()

    def get_msg(self, sql):
        self.cursor.execute(sql)
        # 获取所有记录列表
        results = self.cursor.fetchall()
        print(results)
        return results

    def delete_one(self, sql):
        self.cursor.execute(sql)
        self.conn.commit()
