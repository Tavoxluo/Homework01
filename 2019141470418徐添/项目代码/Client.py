import socket
import sys
from multiprocessing import Process
import os

MAX_BYTES = 65535
ADDRESS = '127.0.0.1'
PORT = 1600


#将注册或者登陆信息打包发送给服务器端
def Person_Message(sock ,choice):
    name = input('please input name:')
    password = input('please input password:')
    text = str(choice) + '  ' + name + '  ' + password
    data = text.encode('ascii')
    sock.sendto(data ,(ADDRESS ,PORT))
    data ,address= sock.recvfrom(MAX_BYTES)
    return data.decode('ascii') ,name ,address


#将用户聊天信息传送给公共频道
def Chat_Message(sock ,name ,address):
    print('Please enter the chat content:\n\n(input \033[1;44mExit\033[0m to quit the room,\n'
          'input \033[1;44ms/name/message\033[0m for Private chat)\t\t\tHistory:')
    #创建进程，父进程发送消息，子进程接受消息
    p = Process(target = rcvmsg ,args = (sock ,name ,address))
    p.start()
    sendmsg(sock ,name ,address)


#发送消息
def sendmsg(sock ,name ,address):
    while True:
        message = input()
        Words = message.split('/')
        if Words[0] == 's':
            Destination = Words[1]
            true_message = Words[2]
            text = '4' + '  ' + name + '  ' + str(address) + '  ' + true_message + '  ' + Destination
            data = text.encode('ascii')
            sock.sendto(data ,(ADDRESS , PORT))
            print('OK!')
        elif message == 'Exit':
            text = '5' + '  ' + name + '  ' + str(address)
            data = text.encode('ascii')
            sock.sendto(data ,(ADDRESS ,PORT))
            sys.exit('You have exited the chat room\n')
        else:
            text = '3' + '  ' + name + '  ' + str(address) + '  ' + message
            data = text.encode('ascii')
            sock.sendto(data ,(ADDRESS ,PORT))


#接收消息
def rcvmsg(sock ,name ,address):
    while True:
        data ,address= sock.recvfrom(MAX_BYTES)
        message = data.decode('ascii')
        if message == 'exit':
            os._exit(0)
        else:
            print('\t\t\t\t\t\t' + message)

    
#套接字连接
def main():
    sock = socket.socket(socket.AF_INET ,socket.SOCK_DGRAM)
    while True:
        while True:
            choice = int(input('please select:\n 1、register 2、login\n'))
            if choice == 1 or choice == 2:
                break
            print('Unknown command')
        #signal标识注册或者登陆时返回的值
        signal ,name ,address = Person_Message(sock ,choice)
        if signal == 'OK':
            os.system("cls")
            print('\t\t\t\tYou have successfully entered the room\t\t')
            break
        elif signal == 'Error_UserExist':
            print('User already exists!')
        elif signal == 'Error_PasswordError':
            print('Password error!')
        elif signal == 'Error_UserNotExist':
            print('user does not exist!')
    Chat_Message(sock ,name ,address)


if __name__ == "__main__":
    main()
