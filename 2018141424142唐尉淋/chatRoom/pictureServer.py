import os
import time
import json
import socket
import threading

import socketUtils
from config import *

FILE_WRITE_LOADING = {}


def pictureServer():
    first = './服务端图片缓存/'  # 图片的保存文件夹
    os.chdir(first)  # 把first设为当前工作路径
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((PICTURE_SERVER_IP, PICTURE_SERVER_PORT))
    s.listen(5)

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


PictureServer = threading.Thread(target=pictureServer)
PictureServer.start()
