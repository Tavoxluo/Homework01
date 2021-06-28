#!/usr/bin/env python
# -*- coding: utf-8 -*-
# 文件名：server.py

import socket
import threading
from tkinter import *
import time

hostname = socket.gethostname()
ip = socket.gethostbyname(hostname)
print('当前服务器IP为：'+ip)
socket_list = []
s = socket.socket()
s.bind((ip, 30000))
s.listen(1)


def read_client(s):
    try:
        # 接收客户端的数据
        return s.recv(2048).decode('utf-8')
    except:
        # 若有异常，说明连接失败，则删除该socket
        print(str(addr) + ' Left!')
        socket_list.remove(s)




def socket_target(s):
    try:
        while True:
            content = read_client(s)
            if content is None:
                break
            else:
                print(content)

            # 将一个客户端发送过来的数据广播给其他客户端
            for client in socket_list:
                client.send((str(addr) + ' say: ' + content).encode('utf-8'))
    except:
        print('Error!')



while True:
    conn, addr = s.accept()
    # 每当有客户连接后，就将其加到socket列表中
    socket_list.append(conn)
    print(str(addr) + ' Joined!')
    # 每当有客户连接后，就启动一个线程为其服务
    threading.Thread(target=socket_target, args=(conn,)).start()
