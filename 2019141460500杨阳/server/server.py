from time import strftime, localtime, time
from server_socket import ServerSocket
from socker_wrapper import SockerWrapper
from threading import Thread
from response_protocol import *
from db import DB


class Server(object):

    def __init__(self):
        self.server_socket = ServerSocket()

        # 请求id和方法关联字典

        self.request_handle_function = {}
        self.register(REQUEST_LOGIN, self.request_login_handle)
        self.register(REQUEST_CHAT, self.request_chat_handle)
        self.register(REQUEST_MEMBER, self.request_member_handle)
        self.register(REQUEST_DELETE_MSG, self.request_delete_msg_handle)
        self.register(REQUEST_CHAT_MSG, self.request_chat_msg_handle)
        self.register(REQUEST_MSG_SEARCH, self.request_msg_search_handle)
        self.register(REQUEST_MEMBER_MSG, self.request_member_msg_handle)
        self.register(REQUEST_MEMBER_DELETE, self.request_member_delete_handle)
        self.register(REQUEST_MEMBER_EDIT, self.request_member_edit_handle)
        self.register(REQUEST_MEMBER_REGISTER, self.request_register_handle)

        # 创建保存当前登录用户的字典
        self.clients = {}

        # 创建数据库管理对象
        self.db = DB()

    def register(self, request_id, handle_function):
        self.request_handle_function[request_id] = handle_function

    def startup(self):

        while True:
            print('正在连接')
            soc, addr = self.server_socket.accept()
            print('获取到客户端连接')
            print(soc, addr)
            # 使用套接字生成包装对象
            client_soc = SockerWrapper(soc)

            # 收发消息
            t = Thread(target=self.request_handle, args=(client_soc,))
            t.start()

            # 匿名函数：
            # Thread(target=lambda: self.request_handle(client_soc)).start()

    def request_handle(self, client_soc):
        while True:

            # 接受客户端数据

            recv_data = client_soc.recv_data()
            if not recv_data:
                # 没数据就关闭
                self.remove_offline_user(client_soc)
                client_soc.close()
                break

            # 解析数据
            parse_data = self.parse_request_text(recv_data)

            # 分析请求类型

            handle_function = self.request_handle_function.get(parse_data['request_id'])
            if handle_function:
                handle_function(client_soc, parse_data)

    def remove_offline_user(self, client_soc):
        # 客户端下线
        print("有人寄了")
        for username, info in self.clients.items():
            if info['sock'] == client_soc:
                nickname = info['nickname']

                print(self.clients)
                del self.clients[username]
                print(self.clients)
                response_text1 = ResponseProtocol.send_delmember(nickname, username)
                print(response_text1)
                for u_name, info1 in self.clients.items():
                    info1['sock'].send_data(response_text1)
                break

    def parse_request_text(self, text):
        # 解析客户端数据

        # 登录： 0001|username|password
        # 聊天： 0002|username|password

        print("解析数据：" + text)
        request_list = text.split(DELIMITER)
        # 按照类型解析数据
        request_data = {}
        request_data['request_id'] = request_list[0]

        if request_data['request_id'] == REQUEST_LOGIN:
            # 用户请求登录
            request_data['username'] = request_list[1]
            request_data['password'] = request_list[2]

        elif request_data['request_id'] == REQUEST_CHAT:
            # 用户发送来的消息
            request_data['username'] = request_list[1]
            request_data['messages'] = request_list[2]

        elif request_data['request_id'] == REQUEST_MEMBER:
            # 用户请求在线人员信息
            request_data['username'] = request_list[1]
            request_data['nickname'] = request_list[2]

        elif request_data['request_id'] == REQUEST_DELETE_MSG:
            request_data['id'] = request_list[1]

        elif request_data['request_id'] == REQUEST_MSG_SEARCH:
            request_data['id'] = request_list[1]
            request_data['st'] = request_list[2]
            request_data['et'] = request_list[3]
            request_data['msg'] = request_list[4]

        elif request_data['request_id'] == REQUEST_MEMBER_EDIT:
            request_data['type'] = request_list[1]
            if request_data['type'] == 'nickname':
                request_data['msg'] = request_list[2]
                request_data['username'] = request_list[3]
            if request_data['type'] == 'password':
                request_data['old_password'] = request_list[2]
                request_data['new_password'] = request_list[3]
                request_data['username'] = request_list[4]

        elif request_data['request_id'] == REQUEST_MEMBER_REGISTER:
            request_data['nickname'] = request_list[1]
            request_data['password'] = request_list[2]

        elif request_data['request_id'] == REQUEST_MEMBER_DELETE:
            request_data['username'] = request_list[1]

        return request_data

    def request_register_handle(self, client_soc, request_data):

        print("收到注册请求")
        nickname = request_data['nickname']
        password = request_data['password']
        sql = "INSERT INTO users(user_nickname,user_password) VALUES ('%s','%s')" % \
              (nickname, password)
        result = self.db.add_one(sql)
        print(result)
        send_data = ResponseProtocol.send_register(str(result), nickname)
        client_soc.send_data(send_data)

    def request_msg_search_handle(self, client_soc, request_data):
        print('收到查询请求')
        if request_data['id'] == '全部':
            if request_data['msg'] == '':
                sql = "select * from msg WHERE msg_time>'%s' and msg_time<'%s'" % (
                    request_data['st'], request_data['et'])
                result = self.db.get_all(sql)
                a = str(result)
                send_msg = ResponseProtocol.send_search_msg(a)
                client_soc.send_data(send_msg)

            else:
                msg = '%' + request_data['msg'] + '%'
                sql = "select * from msg WHERE (msg_time>'%s' and msg_time<'%s') and msg like '%s'" % (
                    request_data['st'], request_data['et'], msg)
                result = self.db.get_all(sql)
                a = str(result)
                send_msg = ResponseProtocol.send_search_msg(a)
                client_soc.send_data(send_msg)

        else:
            if request_data['msg'] == '':
                sql = "select * from msg WHERE (msg_time>'%s' and msg_time<'%s') and user_name = '%s'" % (
                    request_data['st'], request_data['et'], request_data['id'])
                result = self.db.get_all(sql)
                a = str(result)
                send_msg = ResponseProtocol.send_search_msg(a)
                client_soc.send_data(send_msg)

            else:
                msg = '%' + request_data['msg'] + '%'
                sql = "select * from msg WHERE (msg_time>'%s' and msg_time<'%s') and (msg like '%s' and user_name = " \
                      "'%s')" % (request_data['st'], request_data['et'], msg, request_data['id'])
                result = self.db.get_all(sql)
                a = str(result)
                send_msg = ResponseProtocol.send_search_msg(a)
                client_soc.send_data(send_msg)
        pass

    def request_member_msg_handle(self, client_soc, request_data):
        print('收到用户信息请求')
        sql2 = "select user_name,user_nickname from users"
        result2 = self.db.get_all(sql2)
        a2 = str(result2)
        b = ResponseProtocol.send_member_msg(a2)
        client_soc.send_data(b)

    def request_member_delete_handle(self, client_soc, request_data):
        username = request_data['username']
        sql = "delete from users where user_name='%s'" % username
        self.db.delete_one(sql)
        client_soc.send_data(RESPONSE_MEMBER_DELETE)

    def request_member_edit_handle(self, client_soc, request_data):
        print('收到编辑请求')
        if request_data['type'] == 'nickname':
            sql = "UPDATE users SET user_nickname='%s' WHERE user_name='%s'" % (
                request_data['msg'], request_data['username'])
            self.db.update_one(sql)
            sql1 = "UPDATE msg SET nickname='%s' WHERE user_name='%s'" % (request_data['msg'], request_data['username'])
            self.db.update_one(sql1)
            msg = ResponseProtocol.send_member_edit_password('2')
            client_soc.send_data(msg)

        elif request_data['type'] == 'password':
            sql = "select user_name from users where user_name='%s' and user_password='%s'" % (request_data['username'],
                                                                                               request_data[
                                                                                                   'old_password'])
            result = self.db.get_one(sql)
            if result is None:
                msg = ResponseProtocol.send_member_edit_password('0')
                client_soc.send_data(msg)

            else:
                sql1 = "update users set user_password='%s' where user_name='%s' " % (
                request_data['new_password'], request_data['username'])
                self.db.update_one(sql1)
                msg = ResponseProtocol.send_member_edit_password('1')
                client_soc.send_data(msg)

    def request_delete_msg_handle(self, client_soc, request_data):
        print('收到删除请求')
        id = request_data['id']
        sql = "DELETE FROM msg WHERE id = %s" % id
        self.db.delete_one(sql)
        client_soc.send_data(RESPONSE_DELMSG)

    def request_chat_msg_handle(self, client_soc, request_data):
        print('收到更新消息记录请求')
        sql = "select * from msg"
        result = self.db.get_all(sql)
        a = str(result)
        sql2 = "select user_name,user_nickname from users"
        result2 = self.db.get_all(sql2)
        a2 = str(result2)
        b = ResponseProtocol.send_msg(a, a2)

        client_soc.send_data(b)

    def request_member_handle(self, client_soc, request_data):

        # 昵称不能包含’|‘，’@‘
        print('收到成员请求')
        username = request_data['username']
        nickname = request_data['nickname']
        response_text1 = ResponseProtocol.send_member(nickname, username)
        client_soc.send_data(response_text1 + '@')
        for u_name, info in self.clients.items():
            if u_name == username:
                for u_name1, info1 in self.clients.items():
                    if u_name1 == username:
                        print('1')
                        continue
                    response_text2 = ResponseProtocol.send_member(info1['nickname'], u_name1)
                    print(response_text2)
                    client_soc.send_data(response_text2 + '@')
                continue
            info['sock'].send_data(response_text1 + '@')

    def request_login_handle(self, client_soc, request_data):
        # 处理登录
        print('收到登录处理')
        # 获取账号密码
        username = request_data['username']
        password = request_data['password']

        # 查询数据库
        ret, nickname, username = self.check_user_login(username, password)

        # 登陆成功则保存当前用户
        if ret == '1':
            if username in self.clients:
                ret = '2'
            else:
                self.clients[username] = {'sock': client_soc, 'nickname': nickname}

        # 拼接消息
        response_text = ResponseProtocol.response_login_result(ret, nickname, username)

        # 将消息返回客户端
        client_soc.send_data(response_text)

    def request_chat_handle(self, client_soc, request_data):
        # 处理聊天
        print('收到聊天处理', request_data)
        # 获取消息内容
        username = request_data['username']
        messages = request_data['messages']
        nickname = self.clients[username]['nickname']
        send_time = strftime('%Y-%m-%d %H:%M:%S', localtime(time()))
        sql = "INSERT INTO msg(user_name,nickname,msg,msg_time) VALUES (%s,'%s','%s','%s')" % \
              (username, nickname, messages, send_time)
        print(sql)
        self.db.add_one(sql)
        # sql1 = "select * from msg where msg_time BETWEEN '2021-6-11' AND '2021-6-14'"
        # self.db.get_all(sql1)
        # 拼接消息文本
        msg = ResponseProtocol.response_chat(nickname, messages)

        # 转发给在线用户
        for u_name, info in self.clients.items():
            if u_name == username:
                continue
            info['sock'].send_data(msg)

    def check_user_login(self, username, password):
        # 检查用户是否登录成功  1：成功
        # 从数据库查询用户信息
        result = self.db.get_one("select * from users where user_name='%s'" % username)
        result2 = self.db.get_one("select * from manage where manage='%s'" % username)
        # 没有查询结果说明用户不存在，登录失败
        if not result:
            if not result2:
                return '0', '', username

            elif password != result2['password']:
                return '0', '', username

            else:
                return '3', '', username

        # 如果有结果，密码不正确，登陆失败
        if password != result['user_password']:
            return '0', '', username
        # 否则登录成功
        return '1', result['user_nickname'], username


if __name__ == '__main__':
    Server().startup()
