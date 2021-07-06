# -*- coding:utf-8 -*-
# 导入socket库
from socket import *
import base64
# 因为使用的是python2版本所以需要转换为utf-8编码格式
import base64
# 设置主机以及端口号，buffersize为字符最大缓冲数,端口号110是pop的收邮件端口
host = 'pop.qq.com'
port = 110
buffersize = 65536
address = (host, port)
# tcp连接实例初始化并建立连接
sktcp = socket(AF_INET, SOCK_STREAM)
sktcp.connect(address)
recv = sktcp.recv(buffersize)
print(recv)

# 用户登陆验证
user = '534973156@qq.com'
passwd = 'gsevlbljghgfbhad'
user = 'USER {} \r\n'.format(user).encode('utf-8')
passwd = 'PASS {} \r\n'.format(passwd).encode('utf-8')
sktcp.send(bytes(user))
recv = sktcp.recv(buffersize)
recv = str(recv.decode('utf-8'))
print('user:', recv)
sktcp.send(passwd)
recv = sktcp.recv(buffersize)
recv = str(recv.decode('utf-8'))
print('password: ', recv)

# 请求服务器返回关于邮箱的统计资料，前面数字是邮件总数。后面数字是所有邮件的总字节数
stat = 'STAT \r\n'.encode('utf-8')
sktcp.send(bytes(stat))
recv = sktcp.recv(buffersize)
recv = str(recv.decode('utf-8'))
print('stat:', recv)
# 请求服务器返回关于邮箱里面的邮件编号和每个邮件的大小，前面数字是邮件的编号，后面的数字是对应编号邮件的大小
list = 'LIST \r\n'.encode('utf-8')
sktcp.send(bytes(list))
recv = sktcp.recv(buffersize)
recv = str(recv.decode('utf-8'))
print('list:', recv)
no = input('您想要查看哪封邮件？')
# 返回由参数标识的邮件的全部文本，并设置为已读
retr = 'RETR {}\r\n'.format(no).encode('utf-8')
sktcp.send(bytes(retr))
recv = sktcp.recv(buffersize)
recv = base64.b64decode(recv)
print('(第{}封邮件的内容是)：'.format(no), recv)

# 退出连接，退出结束
recv = sktcp.recv(buffersize)
recv = str(recv.decode('utf-8'))
print(recv)
recv = sktcp.recv(buffersize * 3)
recv = base64.b64decode(recv)
recv = str(recv.decode())
print(recv)

quit = 'QUIT\r\n'.encode('utf-8')
sktcp.send(bytes(quit))
recv = sktcp.recv(buffersize)
recv = str(recv)
print('quit:', recv)

# 关闭tcp连接
sktcp.close()
input("please input any key to exit!")
