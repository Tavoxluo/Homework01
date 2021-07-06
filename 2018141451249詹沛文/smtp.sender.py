# -*- coding:utf-8 -*-
# 导入socket库
from socket import *
# 导入base64模块进行编码解码
import base64
import sys

# 设置主机以及端口号，buffersize为字符最大缓冲数,端口号25是smtp的发邮件端口
host = 'smtp.qq.com'
port = 25
buffersize = 65536
address = (host, port)

print("*******您已进入到qq邮箱代理服务******")
# 用户及授权码验证
sender = input('请输入服务器发送人的邮箱地址：')
password = input('请输入邮箱授权码：')
receiver = input('请输入服务器收信人的邮箱地址：')

user = base64.b64encode(bytes(sender.encode('utf-8'))) + bytes('\r\n'.encode('utf-8'))
password = base64.b64encode(bytes(password.encode('utf-8'))) + bytes('\r\n'.encode('utf-8'))

# password = base64.b64encode('yefydwzxfassbbgg') + '\r\n'
# tcp连接实例初始化并建立连接
zpwtcp = socket(AF_INET, SOCK_STREAM)
zpwtcp.connect(address)
# 220标识服务就绪，在socket连接成功后会返回此条信息
recv = zpwtcp.recv(buffersize)
recv = str(recv.decode('utf-8'))
print(recv)
if recv[:3] != '220':
    print('220 reply not received from server.')
    exit()

# SMTP的基本命令集
# HELO：向服务器标识用户身份
# MAIL：初始化邮件传输
# RCPT：表示单个的邮件接收人，常在MAIL后面可以有多个rcpt to:<xxx>
# DATA：在单个或多个RCPT命令后，表示所有的邮件接收人已标识，初始化数据传输，以.结束
# QUIT：结束会话

# HELO hostname是与服务器打招呼并告知客户端使用的机器名字，下面这条命令向服务器打招呼
hello = 'HELO PWL\r\n'
zpwtcp.send(bytes(hello.encode('utf-8')))
# 客户端收到服务器返回的消息
recv = zpwtcp.recv(buffersize)
print('hello: ', recv)
recv = str(recv.decode('utf-8'))
# 收到服务器返回消息，250表示请求邮件动作正确
if recv[:3] != '250':
    print('250 reply not received from server.')
    exit()

# 用户登陆安全验证，依次返回用户名，密码等信息
login = 'AUTH LOGIN\r\n'
zpwtcp.send(bytes(login.encode('utf-8')))
recv = zpwtcp.recv(buffersize)
print('login:', recv)
zpwtcp.send(user)
recv = zpwtcp.recv(buffersize)
print('user:', recv)
zpwtcp.send(password)
recv = zpwtcp.recv(buffersize)
print('password: ', recv)

# 告诉服务器发送人的地址
# mail_from = 'MAIL FROM: <937876430@qq.com>\r\n'
mail_from = 'MAIL FROM: <%s>\r\n' % sender
zpwtcp.send(bytes(mail_from.encode('utf-8')))
recv = zpwtcp.recv(buffersize)
print('mail from: ', recv)
# 告诉服务器收信人的地址
# mail_to = 'RCPT TO: <sk937876430@126.com>\r\n'
mail_to = 'RCPT TO: <%s>\r\n' % receiver
zpwtcp.send(bytes(mail_to.encode('utf-8')))
recv = zpwtcp.recv(buffersize)
print('rcpt to: ', recv)

# 下面开始传输信件内容
data = 'DATA\r\n'
zpwtcp.send(bytes(data.encode('utf-8')))
recv = zpwtcp.recv(buffersize)
print('data: ', recv)
print("********请输入你要发送邮件的内容********")
# sender = '534973156@qq.com'
# reciver = 'noahzhan@163.com'

# 邮件报文首部
headers = [
    'From: %s' % sender,
    'To: %s' % ','.join(receiver),
    'Subject: zpw发来的邮件', ]
# 邮件报文实体
lines = sys.stdin.readlines()
instance = str()
for line in lines:
    instance += line
body = instance
datagram = '\r\n\r\n'.join(('\r\n'.join(headers), ''.join(body)))
zpwtcp.send(bytes(datagram.encode('utf-8')))
endmsg = '\r\n.\r\n'
zpwtcp.send(bytes(endmsg.encode('utf-8')))
recv = zpwtcp.recv(buffersize)
print('datagram: ', recv)

# 退出连接，结束
quit = 'QUIT\r\n'
zpwtcp.send(bytes(quit.encode('utf-8')))
recv = zpwtcp.recv(buffersize)
print('quit: ', recv)
# 关闭tcp连接
zpwtcp.close()
input("please input any key to exit!")
exit(1)
