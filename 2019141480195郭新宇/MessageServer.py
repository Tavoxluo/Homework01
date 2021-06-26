# coding=UTF-8
import socket
import threading

# 设定本机端口，在服务器中运行时端口需重新设定
host='127.0.0.1'
port='30000'

# 记录昵称列表和socket列表，创建服务器socket并开启监听
nickName_list={}
nickSocketList = {}
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((host, int(port)))
server.listen()

# 获取客户端消息函数，连接断开时清除连接
def readFromClient(server):
    try:
        return server.recv(2048).decode()
    except:
        del nickName_list[nickName]

# 获取消息，识别消息发送对象，进行转发，连接断开时显示退出的用户
def sendMessage(server,nickName):
    try:
        while True:
            text=readFromClient(server)
            content = text.split('$')[1]
            tar = text.split('$')[0]
            if content is None:
                break
            # 此为定义的查询字符！，当接收消息为！时，向客户端发送当前在线人员列表
            if content =='!':
                server.send(str(nickName_list).encode())
                continue
            else:
                nickSocketList[tar].send(('from ' + nickName + ' ： ' + content).encode())

    except:
        print(nickName+'离开了')


while True:
    # 连接，接受用户登录，更新在线用户列表，发送提示信息，开启线程
    conn, addr = server.accept()
    nickName = readFromClient(conn)
    nickName1 = str(nickName)
    nickSocketList[nickName] = conn
    nickName_list[nickName1]='在线'
    conn.send(str(nickName_list).encode()+'\n'.encode())
    conn.send('输入!查看当前在线用户\n输入$以清除聊天框'.encode())
    t=threading.Thread(target=sendMessage, args=(conn, nickName))
    t.daemon = 1
    t.start()

