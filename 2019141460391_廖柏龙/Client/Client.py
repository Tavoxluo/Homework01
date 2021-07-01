import socket
import configparser

#读取ini配置文件
cf = configparser.ConfigParser()
cf.read("ip.ini")
ip = cf.get('IP', 'ip1') #"100.75.227.90"

# 参数（domain，type，protocol） 其中domain为协议域或者协议族，决定使用地址的类型，其中
# AF_INET表示采用ipv4和端口号为16位的组合 type决定socket类型，protocol决定使用的协议
tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

def linkToServer():

    port = 8080
    tcp.connect((ip, port))

#用于用户
def account(account,password):
    try:
        tcp.send(('A:'+account+'\n'+password).encode('gbk'))
        msg = tcp.recv(1024)
        if msg == b'true':
            return True
        else:
            return False
    except:
        return False

#用于登录验证
def login(account):
    #测试 print("来了")
    try:
        tcp.send(('L:'+account).encode('gbk'))
        msg = tcp.recv(1024)
        if msg == b'true':
            return True
        else:
            return False
    except:
        return False

#用于新建用户
def newAccount(account,password):
    try:
        tcp.send(('N:' + account + '\n' + password).encode('gbk'))
        msg = tcp.recv(1024)
        if msg == b'true':
            return True
        else:
            return False
    except:
        return False
