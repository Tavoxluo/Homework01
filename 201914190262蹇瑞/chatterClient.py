import socket
import threading
import configparser

config = configparser.ConfigParser()
config.read('config.ini')
host = config.get('baseconf','host')

port = int(config.get('baseconf','port'))
s = socket.socket()
s.connect((host, port))

def read_server(s):
    while True:
        # 子线程负责从服务端接受数据并打印
        content = s.recv(2048).decode('utf-8')
        print(content)

threading.Thread(target=read_server, args=(s,)).start()
flag = 0
while True:

    if flag ==0:
        nickName = input("请输入您的昵称：")
        nickName = '!'+nickName
        flag = 1
        s.send(nickName.encode('utf-8'))
        continue
    else:
        line = input('')
        if line == 'exit':
            s.close()
            break
        # 主线程负责将用户输入的数据发送到socket中
        s.send(line.encode('utf-8'))