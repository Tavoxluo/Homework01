import socket
import threading
import configparser

config = configparser.ConfigParser()
config.read('config.ini')
host = config.get('baseconf','host')
port = int(config.get('baseconf','port'))

s = socket.socket()
socket_list = []
client_List = {}
nickSocketList = {}
s = socket.socket()
s.bind((host, port))
s.listen()


def read_client(s):
    try:
        # 接收客户端的数据
        return s.recv(2048).decode('utf-8')
    except:
        # 若有异常，说明连接失败，则删除该socket
        print(str(addr) + ' Left!')
        socket_list.remove(s)
        del client_List[nickName]
        if client_List is not None:
            print(client_List)
        else:
            print('None')


def socket_target(s,nickName):
    #conn = s
    #print(s)
    try:
        while True:
            content = read_client(s)
            if content is None:
                break
            else:
                if content =='#':
                    s.send(str(client_List).encode('utf-8'))
                    continue
                elif content == '&':
                    s.send("1、输入#查询在线成员 2、输入要发送的内容并@某用户可私聊 3、其他功能正在开发中......".encode('utf-8'))
                    continue
                elif '@' in content:
                    nick = content.split('@')[1]
                    date = content.split('@')[0]
                    nickSocketList[nick].send((nick + ' 对你说：'+ date).encode('utf-8'))
                    continue
                else:
                    print(nickName + ' say: ' + content)
            # 将一个客户端发送过来的数据广播给其他客户端
            for client in socket_list:
                client.send((nickName + ' '+ 'say: ' + ' ' + content).encode('utf-8'))
    except:
        print('Error!')


while True:
    conn, addr = s.accept()
    # 每当有客户连接后，就将其加到socket列表中
    nickName = read_client(conn).split('!')[1]
    client_List[nickName] = addr
    nickSocketList[nickName] = conn
    print(client_List)
    #print(nickName)
    socket_list.append(conn)
    print(nickName + ' ' + str(addr) + ' Joined!')
    # 每当有客户连接后，就启动一个线程为其服务
    threading.Thread(target=socket_target, args=(conn,nickName,)).start()