from socket import *
from threading import Thread
import configparser
import os

curpath = os.path.dirname(os.path.realpath(__file__))
cfgpath = os.path.join(curpath, 'data.ini')
print(cfgpath)

conf = configparser.ConfigParser()
conf.read(cfgpath,encoding="utf-8")
sections = conf.sections()
print(sections)
items = conf.items('server_ini')
print(items)

serverIP = items[0][1]
print(serverIP)
serverPort = int(items[1][1])
print(serverPort)

serverSocket = socket(AF_INET,SOCK_STREAM) #TCP
serverSocket.bind((serverIP,serverPort))
serverSocket.listen(1)
print(serverSocket.getsockname(),gethostname(),serverPort)

print('The server is ready to receive')

# 客户端系统分群聊和私聊两种模式，服务器承担的主要工作便是信息类型的判断和转发：
# 即服务器保存着一个当前所有在线客户端的IP和端口号列表（之后的迭代可以用数据库保存这一部分信息，还可以扩展出用户昵称等个人信息）
# - 根据接收到的讯息的标识符判断，如果是群聊模式，则服务器会将接收到的讯息转发至每一个在线客户端（完善后可设计仅转发至某个特定的小群聊中，现在的设计更像是全网广播）
# - 如果是获取客户列表，则服务器向发出请求的客户端返回当前所有在线客户端的IP和端口号列表
# - 如果是私聊模式，则服务器会将讯息转发至客户端双击选择的聊天对象，同时基于人性化的信息呈现考量，还会返回一份讯息至发出该讯息的主机

# 为每一个客户端单独设置一个线程，并保持长连接
def work(sock, addr, client_list):
    print("start work")
    try:
        while True:
            # 判断为广播模式
            data = sock.recv(1024).decode()
            #print(data[-13:])
            if data[-13:]=="broad_pattern":
                #data = sock.recv(1024).decode()
                data = data[:-13]
                print("接收到："+data)
                if len(data) > 0:
                    # 服务器对客户端讯息的展示逻辑是：如果为广播模式，则将接收到的信息转发至每一个现有用户的客户端界面上；如为一对一的私聊模式，则仅转发给指定用户
                    # 广播模式
                    #print('(%s)：' % str(addr), data)
                    for i in client_list:
                        print(i[0])
                        i[0].send('response_to_broad'.encode())
                        i[0].send(('(%s)：' % str(addr)+data).encode()) #client端的逻辑是：只有收到服务器的相应信息才允许继续发送下一条信息。因此每次成功接收到客户端信息都要给一个响应
                else:
                    print('客户端%s已关闭' % str(addr))
                    break
            # 判断为私聊模式-获取通讯录
            if data[-13:] == "toone_pattern":
                print("进入私聊模式")
                client_sum = ""
                for client in client_list:
                    client_sum+=str(client[1])+"^^"

                sock.send("response_as_list".encode())
                sock.send(client_sum[:-2].encode())
            # 判断为私聊
            if data[-13:] == "xchat_pattern":
                data = data[:-13]
                cur_client = sock.recv(1024).decode()
                print("接收到：" + data)
                print("发送至：" + cur_client)
                sock.send('response_to_one'.encode())
                sock.send(('(%s)：' % str(addr) + data).encode()) #发送给本机的消息
                for i in client_list:
                    print(i[1])
                    if str(i[1])==cur_client:
                        i[0].send('response_to_one'.encode())
                        i[0].send(('(%s)：' % str(addr) + data).encode()) #发送给对方主机的消息

    except ConnectionResetError:
        pass #忽略客户端关闭的错误

# 原本单线程的通讯逻辑是：至多支持客户端和服务器端之间的来回通信，无法再多加哪怕一个客户端（存在堵塞）。
# 因此我觉得无论是多个客户端的情况，还是依托服务器的信息转发等，都必须要实现多线程-即为每一个客户端与服务器之间的连接建立一个线程
# 这样顺带着也就实现了长连接，即不用每次发消息都重新建立一次连接，同时也就不必为每次连接都重新分配一个端口号
# （通过在线程内部设置循环的方式-即只要该客户端还有信息要发/发送的信息不为空等，则循环就不会终止，也就保持了长连接）
client_list = []
while True:
    clientSocket, addr = serverSocket.accept()
    print('客户端(%s)已成功连接...' % str(addr))
    if [clientSocket, addr] not in client_list:
        client_list.append([clientSocket, addr])
    # 由于线程创建是在循环里创建和启动的
    # 因此每循环一次就会产生一个线程
    thread = Thread(target=work, args=(clientSocket, addr,client_list))
    thread.start()

serverSocket.close()