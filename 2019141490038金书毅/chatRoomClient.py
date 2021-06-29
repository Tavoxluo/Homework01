#!/usr/bin/env python
# -*- coding: utf-8 -*-
# 文件名：client.py

import socket
import threading

print('请输入服务器IP')
ip = input()
s = socket.socket()
i=0
#错误处理
while i==0:
    try:
        p=s.connect((ip, 30000))
        i=1
    except:
        print('输入错误')
        ip = input()

print('连接成功')
def read_server(s):
    while True:
        # 子线程负责从服务端接受数据并打印
        content = s.recv(2048).decode('utf-8')
        print(content)


threading.Thread(target=read_server, args=(s,)).start()

while True:
    line = input()
    if line == 'exit':
        break
    # 主线程负责将用户输入的数据发送到socket中
    s.send(line.encode('utf-8'))
