import socketserver
import pickle
import time
from datetime import datetime

import lib

users = None
history = None

#加载user记录到users变量
def loadUser():
    try:
        return pickle.load(open('users.dat', 'rb'))
    except:
        return {}

#注册函数
def register(usr, pwd):
    if usr not in users.keys():
        users[usr] = pwd
        saveUser()
        return True
    else:
        return False

#验证登录有效性
def validate(usr, pwd):
    if usr in users.keys() and users[usr] == pwd:
        return True
    return False

#将刚注册用户的信息以二进制的方式存进user.dat
def saveUser():
    pickle.dump(users, open('users.dat', 'wb'))

#利用pickle.load()将history.dat里面的二进制记录转换为字符串显示
def loadHistory():
    try:
        return pickle.load(open('history.dat', 'rb'))
    except:
        return {}


def getKey(u1, u2):
    return (u1, u2) if (u2, u1) not in history.keys() else (u2, u1)

#
def appendHistory(sender, receiver, msg):
    if receiver == '':                             #公用聊天
        key = ('','')
    else:
        key = getKey(sender, receiver)             #私人聊天
    if key not in history.keys():                  #为一个具有新的sender和receiver的聊天创建一条记录
        history[key] = []                          #将新的信息元组存入键值为(sender,receiver)的数组中
    now = datetime.now()
    history[key].append((sender, now.strftime("%Y-%m-%d, %H:%M:%S"), msg))
    saveHistory()

#取出history.dat文件中的历史聊天记录
def getHistory(sender, receiver):
    if receiver == '':
        key = ('','')
    else:
        key = getKey(sender, receiver)
    return history[key] if key in history.keys() else []

#存储一条新的记录进入history.dat
def saveHistory():
    pickle.dump(history, open('history.dat', 'wb'))

#sever处理客户发来命令的函数
class Handler(socketserver.BaseRequestHandler):
    clients = {}

    def setup(self):
        self.user = ''
        self.filePeer = ''
        self.authed = False


    def handle(self):
        while True:
            data = lib.recv(self.request)
            if not self.authed:
                self.user = data['user']
                #登录
                if data['command'] == 'login':
                    #验证用户并加入群组
                    if validate(data['user'], data['pwd']):
                        lib.send(self.request, {'response': 'succeed'})
                        self.authed = True
                        for user in Handler.clients.keys():
                            lib.send(Handler.clients[user].request, {'type': 'peerJoined', 'peer': self.user})
                        Handler.clients[self.user] = self#在服务器中注册当前用户为在线状态
                    else:
                        lib.send(self.request, {'response': 'fail', 'reason': '账号或密码错误！'})
                #注册
                elif data['command'] == 'register':
                    if register(data['user'], data['pwd']):
                        lib.send(self.request, {'response': 'succeed'})
                    else:
                        lib.send(self.request, {'response': 'fail', 'reason': '账号已存在！'})
            else:
                #列表显示当前在线用户
                if data['command'] == 'getUsers':
                    users = []
                    for user in Handler.clients.keys():
                        if user != self.user:
                            users.append(user)
                    lib.send(self.request, {'type': 'getUsers', 'data': users})
                #聊天记录
                elif data['command'] == 'getHistory':
                    lib.send(self.request, {'type': 'getHistory', 'peer': data['peer'], 'data': getHistory(self.user, data['peer'])})
                elif data['command'] == 'chat':
                    #私聊
                    if data['peer'] != '':
                        lib.send(Handler.clients[data['peer']].request, {'type': 'msg', 'peer': self.user, 'msg': data['msg']})
                        appendHistory(self.user, data['peer'], data['msg'])
                    #公共聊天室
                    elif data['peer'] == '':
                        for user in Handler.clients.keys():
                            if user != self.user:
                                lib.send(Handler.clients[user].request, {'type': 'broadcast', 'peer': self.user, 'msg': data['msg']})
                        appendHistory(self.user, '', data['msg'])
                #文件请求
                elif data['command'] == 'fileReq':
                    Handler.clients[data['peer']].filePeer = self.user
                    lib.send(Handler.clients[data['peer']].request, {'type': 'fileReq', 'peer': self.user, 'filename': data['filename'], 'size': data['size'], 'md5': data['md5']})
                #拒绝文件发送
                elif data['command'] == 'fileDeny' and data['peer'] == self.filePeer:
                    self.filePeer = ''
                    lib.send(Handler.clients[data['peer']].request, {'type': 'fileDeny', 'peer': self.user})
                #同意文件发送
                elif data['command'] == 'fileAccept' and data['peer'] == self.filePeer:
                    self.filePeer = ''
                    lib.send(Handler.clients[data['peer']].request, {'type': 'fileAccept', 'ip': self.client_address[0]})
                #关闭聊天
                elif data['command'] == 'close':
                    self.finish()
                    break

    #聊天关闭处理
    def finish(self):
        if self.authed:
            self.authed = False
            if self.user in Handler.clients.keys():
                del Handler.clients[self.user]#将客户从服务器中的在线用户中删除
            for user in Handler.clients.keys():
                lib.send(Handler.clients[user].request, {'type': 'peerLeft', 'peer': self.user})#通知其他用户


if __name__ == '__main__':
    users = loadUser()
    history = loadHistory()
    
    #启动多线程tcpServer作为服务器
    app = socketserver.ThreadingTCPServer((lib.SERVEIP, lib.SERVEPORT), Handler)
    app.serve_forever()