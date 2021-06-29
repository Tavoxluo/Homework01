import socket
import datetime 

MAX_BYTES = 65535
ADDRESS = '127.0.0.1'
PORT = 1600

    
#选项菜单
def menu(sock ,Users_message):
    while True:
        # data ,address = sock.recvfrom(MAX_BYTES)
        # text = data.decode('ascii')
        # print('message from {} is {}'.format(address ,text))
        # text = 'hello ,too'
        # data = text.encode('ascii')
        # sock.sendto(data ,address)
        data ,address = sock.recvfrom(MAX_BYTES)
        text_list = data.decode('ascii').split('  ')

        if int(text_list[0]) == 1:
            #注册
            Register(sock ,Users_message ,text_list ,address)
        if int(text_list[0]) == 2:
            #登陆
            Login(sock ,Users_message ,text_list ,address)
        if int(text_list[0]) == 3:
            #公聊
            Public_chat(sock ,Users_message ,text_list)
        if int(text_list[0]) == 4:
            #私聊
            Private_chat(sock ,Users_message ,text_list)
        if int(text_list[0]) == 5:
            #退出
            Exit(sock ,Users_message ,text_list)

#注册
def Register(sock ,Users_message ,text_list ,address):
    name = text_list[1]
    password = text_list[2]
    if name in Users_message.keys():
        sock.sendto('Error_UserExist'.encode('ascii') ,address)
        print(Users_message)
    else:
        Users_message[name] = [password ,address]
        print(name + ' is enter the room')
        sock.sendto('OK'.encode('ascii') ,address)

#登陆
def Login(sock ,Users_message ,text_list ,address):
    name = text_list[1]
    password = text_list[2]
    if name in Users_message.keys():
        if Users_message[name][0] == password:
            sock.sendto('OK'.encode('ascii') ,address)
            print(name + ' is enter the room\n')
        else:
            sock.sendto('Error_PasswordError'.encode('ascii') ,address)
    else:
        sock.sendto('Error_UserNotExist'.encode('ascii') ,address)

#公聊
def Public_chat(sock ,Users_message ,text_list):
    name = text_list[1]
    #address = text_list[2]
    message = text_list[3]
    data = ('[' + name + ']:' + message)
    for user in Users_message.keys():
        if user != name:
            sock.sendto(data.encode('ascii') ,Users_message[user][1])
    print('[' + str(datetime.datetime.now()) + ']' + '[' + name + ']:' + message)


#私聊
def Private_chat(sock ,Users_message ,text_list):
    name = text_list[1]
    #address = text_list[2]
    message = text_list[3]
    Destination = text_list[4]
    data = ('[' + name + ']:' + message)
    for user in Users_message.keys():
        if user == Destination:
            sock.sendto(data.encode('ascii') ,Users_message[user][1])
            print('[' + str(datetime.datetime.now()) + ']' + '[' + name + ']' + ' to [' + Destination + ']: ' + message)


#退出程序
def Exit(sock ,Users_message ,text_list):
    name = text_list[1]
    address = text_list[2]
    print(address)
    data = 'exit'
    for user in Users_message.keys():
        if name == user:
            sock.sendto(data.encode('ascii') ,Users_message[user][1])
            print(name + ' is quit the room\n')
    

#套接字连接
def main():
    #用户信息存在字典中，实现可持久化存储可将用户信息写入txt等文本内
    Users_message={}
    sock = socket.socket(socket.AF_INET ,socket.SOCK_DGRAM)
    sock.bind((ADDRESS ,PORT))
    print('listen to {}'.format(sock.getsockname()))
    menu(sock ,Users_message)


if __name__ == "__main__":
    main()
