import os
import time
import json
import queue
import socket
import threading

import socketUtils
from config import *

FILE_WRITE_LOADING = {}


def chatServer():
    que = queue.Queue()  # 用于存放客户端发送的信息的队列
    users = []  # 用于存放在线用户的信息  [conn, user, addr]
    lock = threading.Lock()  # 创建锁, 防止多个线程写入数据的顺序打乱

    # 用于接收所有客户端发送信息的函数
    def tcp_connect(conn: socket.socket, addr):
        # 连接后将用户信息添加到users列表
        user = socketUtils.recv_string(conn)
        if user == 'no':
            user = addr[0] + ':' + str(addr[1])
        users.append((conn, user, addr))
        print('新连接:', addr, ':', user, end='')  # 打印用户名
        d = onlines()  # 有新连接则刷新客户端的在线用户显示
        update_que(addr, d)
        try:
            while True:
                data = socketUtils.recv_string(conn)
                print("que_data", data)
                update_que(addr, data)  # 保存信息到队列
        except:
            print(user + ' 断开连接')
            delUsers(conn, addr)  # 将断开用户移出users
        finally:
            conn.close()

    # 判断断开用户在users中是第几位并移出列表, 刷新客户端的在线用户显示
    def delUsers(conn: socket.socket, addr):
        a = 0
        for i in users:
            if i[0] == conn:
                users.pop(a)
                print('剩余在线用户: ', end='')  # 打印剩余在线用户(conn)
                d = onlines()
                update_que(addr, d)
                print(d)
                break
            a += 1

    # 将接收到的信息(ip,端口以及发送的信息)存入que队列
    def update_que(addr, data):
        lock.acquire()
        try:
            que.put((addr, data))
        finally:
            lock.release()

    # 将队列que中的消息发送给所有连接到的用户
    def sendData():
        while True:
            if not que.empty():
                data = ''
                message = que.get()  # 取出队列第一个元素
                if isinstance(message[1], str):  # 如果data是str则返回Ture
                    for i in range(len(users)):
                        # user[i][1]是用户名, users[i][2]是addr, 将message[0]改为用户名
                        for j in range(len(users)):
                            if message[0] == users[j][2]:
                                data = ' ' + users[j][1] + ':' + message[1]
                                break
                        socketUtils.send_string(users[i][0], data)
                        # users[i][0].send(data.encode())
                data = data.split(':;')[0]
                if isinstance(message[1], list):  # 同上
                    # 如果是list则打包后直接发送
                    for i in range(len(users)):
                        socketUtils.send_json(users[i][0], message[1])
                        # users[i][0].send(data.encode())

    # 将在线用户存入online列表并返回
    def onlines():
        online = []
        for i in range(len(users)):
            online.append(users[i][1])
        return online

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((CHAT_SERVER_IP, CHAT_SERVER_PORT))
    s.listen(5)
    print('tcp server is running...')
    q = threading.Thread(target=sendData)
    q.start()
    try:
        while True:
            conn, addr = s.accept()
            t = threading.Thread(target=tcp_connect, args=(conn, addr))
            t.start()
    finally:
        s.close()


def fileServer():
    first = r'./resources/'
    os.chdir(first)  # 把first设为当前工作路径
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((FILE_SERVER_IP, FILE_SERVER_PORT))
    s.listen(3)

    def tcp_connect(conn, addr):
        print('Connected by: ', addr)

        while True:
            data = socketUtils.recv_string(conn)
            print("data", data)
            if data == 'quit':
                print('Disconnected from {0}'.format(addr))
                break
            order = data.split()[0]  # 获取动作
            recv_func(order, data, conn)

        conn.close()

    # 传输当前目录列表
    def sendList(conn):
        listdir = os.listdir(os.getcwd())
        listdir = json.dumps(listdir)
        socketUtils.send_string(conn, listdir)

    # 发送文件函数
    def sendFile(message, conn):
        name = message.split()[1]  # 获取第二个参数(文件名)
        print("发送文件", conn)
        for _ in range(10):
            if not FILE_WRITE_LOADING.get(name) is False:
                time.sleep(0.5)
            else:
                break

        socketUtils.send_file(conn, name)

    # 保存上传的文件到当前工作目录
    def recvFile(message, conn):
        print("message", message)
        name = message.split()[1]  # 获取第二个参数(文件名)
        FILE_WRITE_LOADING[name] = True
        filepath = socketUtils.recv_file(conn)
        FILE_WRITE_LOADING[name] = False

    # 切换工作目录
    def cd(message):
        message = message.split()[1]  # 截取目录名
        # 如果是新连接或者下载上传文件后的发送则 不切换 只将当前工作目录发送过去
        if message != 'same':
            f = r'./' + message
            os.chdir(f)
        path = os.getcwd().split('\\')  # 当前工作目录
        for i in range(len(path)):
            if path[i] == 'resources':
                break
        pat = ''
        for j in range(i, len(path)):
            pat = pat + path[j] + ' '
        pat = '\\'.join(pat.split())
        # 如果切换目录超出范围则退回切换前目录
        if not 'resources' in path:
            f = r'./resources'
            os.chdir(f)
            pat = 'resources'
        socketUtils.send_string(conn, pat)

    # 判断输入的命令并执行对应的函数
    def recv_func(order, message, conn):
        if order == 'get':
            return sendFile(message, conn)
        elif order == 'put':
            return recvFile(message, conn)
        elif order == 'dir':
            return sendList(conn)
        # elif order == 'pwd':
        #     return pwd()
        elif order == 'cd':
            return cd(message)

    try:
        while True:
            conn, addr = s.accept()
            t = threading.Thread(target=tcp_connect, args=(conn, addr))
            t.start()
    except Exception as e:
        print(e)
    finally:
        s.close()


ChatServer = threading.Thread(target=chatServer)
ChatServer.start()
FileServer = threading.Thread(target=fileServer)
FileServer.start()
