from pymysql import connect
from config import *
import re


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

        # 如果数据表已经存在使用 execute() 方法删除表。
        a = self.table_exists(self.cursor, 'manage')
        print(a)
        if not a:
            # 创建数据表SQL语句

            sql3 = """CREATE TABLE `users` (
            `user_name`  int NOT NULL AUTO_INCREMENT ,
            `user_password`  varchar(30) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL ,
            `user_nickname`  varchar(30) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL ,
            PRIMARY KEY (`user_name`),
            INDEX `user_name` (`user_name`) USING BTREE
            )
            ENGINE=InnoDB
            DEFAULT CHARACTER SET=utf8 COLLATE=utf8_general_ci
            AUTO_INCREMENT=31
            ROW_FORMAT=DYNAMIC"""

            self.cursor.execute(sql3)


            sql = """CREATE TABLE `manage` (
            `manage`  varchar(10) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL ,
            `password`  varchar(30) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL ,
            PRIMARY KEY (`manage`)
            )
            ENGINE=InnoDB
            DEFAULT CHARACTER SET=utf8 COLLATE=utf8_general_ci
            ROW_FORMAT=DYNAMIC
            """

            self.cursor.execute(sql)

            sql2 = """CREATE TABLE `msg` (
            `user_name`  int NOT NULL ,
            `nickname`  varchar(30) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL ,
            `msg_time`  datetime NOT NULL ,
            `msg`  varchar(500) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL ,
            `id`  int NOT NULL AUTO_INCREMENT ,
            PRIMARY KEY (`id`),
            FOREIGN KEY (`user_name`) REFERENCES `users` (`user_name`) ON DELETE CASCADE ON UPDATE RESTRICT,
            INDEX `user_name` (`user_name`) USING BTREE
            )
            ENGINE=InnoDB
            DEFAULT CHARACTER SET=utf8 COLLATE=utf8_general_ci
            AUTO_INCREMENT=96
            ROW_FORMAT=DYNAMIC"""

            self.cursor.execute(sql2)



            sql3 = "INSERT INTO manage(manage, password) VALUES ('yy', '123456')"

            self.add_one(sql3)




    def table_exists(self, con, table_name):  # 这个函数用来判断表是否存在
        sql = "show tables;"
        con.execute(sql)
        tables = [con.fetchall()]
        table_list = re.findall('(\'.*?\')', str(tables))
        table_list = [re.sub("'", '', each) for each in table_list]
        if table_name in table_list:
            return 1  # 存在返回1
        else:
            return 0  # 不存在返回0

    def close(self):
        self.cursor.close()
        self.conn.close()

    def get_one(self, sql):
        # 执行sql语句
        self.cursor.execute(sql)

        # 获取查询结果
        query_result = self.cursor.fetchone()

        if not query_result:
            return None

        # 判断是否有结果
        fileds = [filed[0] for filed in self.cursor.description]

        # 使用字段和数据合成字典返回
        return_data = {}
        for filed, value in zip(fileds, query_result):
            return_data[filed] = value

        return return_data

    def add_one(self, sql):
        # 执行sql语句
        self.cursor.execute(sql)
        # 提交到数据库执行
        self.conn.commit()
        tag_id = self.cursor.lastrowid
        return tag_id

    def get_all(self, sql):
        self.cursor.execute(sql)
        # 获取所有记录列表
        results = self.cursor.fetchall()
        return results

    def delete_one(self, sql):
        self.cursor.execute(sql)
        self.conn.commit()

    def update_one(self, sql):
        self.cursor.execute(sql)
        self.conn.commit()
