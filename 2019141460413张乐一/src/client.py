from server import appendHistory
import tkinter.filedialog
import tkinter.messagebox
import tkinter
import threading
import hashlib
import socket
import time
from datetime import datetime
import sys
import os

import lib

#初始窗口
class LoginWin:

    def show(self):
        self.win.mainloop()

    def destroy(self):
        self.win.destroy()

    def __init__(self):
        self.win = tkinter.Tk()
        self.user = tkinter.StringVar()
        self.pwd = tkinter.StringVar()

        self.win.geometry("320x240")
        self.win.title("登录")
        self.win.resizable(width=False, height=False)

        self.labelAcnt = tkinter.Label(self.win,text='账号')
        self.labelAcnt.place(relx=0.055, rely=0.1, height=31, width=89)
        self.entryUser = tkinter.Entry(self.win,textvariable=self.user)
        self.entryUser.place(relx=0.28, rely=0.11, height=26, relwidth=0.554)

        self.labelPwd = tkinter.Label(self.win,text='密码')
        self.labelPwd.place(relx=0.055, rely=0.27, height=31, width=89)

        self.entryPwd = tkinter.Entry(self.win,show="*",textvariable=self.pwd)
        self.entryPwd.place(relx=0.28, rely=0.28, height=26, relwidth=0.554)

        self.loginBtn = tkinter.Button(self.win,text='登录',command=onLoginBtnClicked)
        self.loginBtn.place(relx=0.13, rely=0.6, height=32, width=88)

        self.regBtn = tkinter.Button(self.win,text='注册',command=onRegBtnClicked)
        self.regBtn.place(relx=0.6, rely=0.6, height=32, width=88)

#主窗口
class MainWin:
    closedFunction = None

    def show(self):
        self.win.mainloop()

    def destroy(self):
        try:
            self.closedFunction()
        except:
            pass
        self.win.destroy()

    def __init__(self):
        self.win = tkinter.Tk()
        self.win.protocol('WM_DELETE_WINDOW', self.destroy)
        self.win.geometry("480x320")
        self.win.title("聊天室")
        self.win.resizable(width=False, height=False)

        self.msg = tkinter.StringVar()
        self.name = tkinter.StringVar()

        self.userList = tkinter.Listbox(self.win)
        self.userList.place(relx=0.75, rely=0.15, relheight=0.72, relwidth=0.23)

        self.labelAcnt = tkinter.Label(self.win,text='在线用户列表')
        self.labelAcnt.place(relx=0.76, rely=0.075, height=21, width=101)

        self.history = tkinter.Text(self.win,state='disabled')
        self.history.place(relx=0.02, rely=0.24, relheight=0.63, relwidth=0.696)

        self.entryMsg = tkinter.Entry(self.win,textvariable=self.msg)
        self.entryMsg.place(relx=0.02, rely=0.9, height=24, relwidth=0.59)

        self.sendBtn = tkinter.Button(self.win,text='发送',command=onSendBtnClicked)
        self.sendBtn.place(relx=0.62, rely=0.89, height=28, width=45)

        self.sendFileBtn = tkinter.Button(self.win,text='发送文件',state='disabled',command=onFileBtnClicked)
        self.sendFileBtn.place(relx=0.752, rely=0.89, height=28, width=108)

        self.labelPwd = tkinter.Label(self.win,textvariable=self.name)
        self.labelPwd.place(relx=0.24, rely=0.0, height=57, width=140)


loginWin = None
mainWin = None
mySocket = None
userName = ''
currentSession = ''
users = {}
filename = ''
filenameShortened = ''
fileTransferPending = False


#关闭连接
def closeSocket():
    try:
        lib.send(mySocket, {'command': 'close'})
        mySocket.settimeout(None)
        mySocket.shutdown(2)
        mySocket.close()
    except:
        pass

#执行登录
def onLoginBtnClicked():
    global mySocket, userName, loginWin, mainWin
    mySocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    mySocket.settimeout(5)    # 非阻塞
    if loginWin.user.get() != '' and loginWin.pwd.get() != '':
        mySocket.connect((lib.SERVERIP, lib.SERVERPORT))
        lib.send(mySocket, {'command': 'login', 'user': loginWin.user.get(),'pwd': hashlib.sha1(loginWin.pwd.get().encode('utf-8')).hexdigest()})#利用hashlib进行简单的密码加密
        serverResponse = lib.recv(mySocket)
        #关闭登录窗口，打开主窗口
        if serverResponse['response'] == 'succeed':
            userName = loginWin.user.get()
            loginWin.destroy()
            mainWin = MainWin()
            mainWin.closedFunction = onClosed
            mainWin.name.set('Hi!\n%s' % userName)
            mainWin.userList.bind('<<ListboxSelect>>', onSessionSelect)
            lib.send(mySocket, {'command': 'getUsers'})
            lib.send(mySocket, {'command': 'getHistory', 'peer': ''})
            #多线程启动接收消息
            t = threading.Thread(target=recvAsync, args=())
            t.setDaemon(True) # 主进程结束时直接杀死子进程
            t.start()
            mainWin.show()
        elif serverResponse['response'] == 'fail':
            tkinter.messagebox.showerror('警告', '登录失败：' + serverResponse['reason'])
            mySocket.settimeout(None)
            closeSocket()
    else:
        tkinter.messagebox.showerror('警告', '账号和密码不能为空！')

#执行注册
def onRegBtnClicked():
    global mySocket, loginWin
    mySocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    mySocket.settimeout(5)
    if loginWin.user.get() != '' and loginWin.pwd.get() != '':
        mySocket.connect((lib.SERVERIP, lib.SERVERPORT))
        lib.send(mySocket, {'command': 'register', 'user': loginWin.user.get(),'pwd': hashlib.sha1(loginWin.pwd.get().encode('utf-8')).hexdigest()})
        serverResponse = lib.recv(mySocket)
        if serverResponse['response'] == 'succeed':
            tkinter.messagebox.showinfo('注意', '注册成功！')
        elif serverResponse['response'] == 'fail':
            tkinter.messagebox.showerror('警告', '注册失败：' + serverResponse['reason'])
    else:
        tkinter.messagebox.showerror('警告', '账号和密码不能为空！')
        mySocket.settimeout(None)
        closeSocket()

#异步接收消息
def recvAsync():
    global mySocket, users, mainWin, currentSession, fileTransferPending, filenameShortened, filename
    while True:
        try:#为防止主进程结束时由于发送的数据未定义而print exception stacktrace
            data = lib.recv(mySocket)
        except:
            pass
        try:
            data['type'] == 'getUsers'
        except:
            break
        if data['type'] == 'getUsers':
            users = {}
            for user in [''] + data['data']:
                users[user] = False
            refreshUserList()
        elif data['type'] == 'getHistory':
            if data['peer'] == currentSession:
                mainWin.history['state'] = 'normal'# 解锁history可以修改
                mainWin.history.delete('1.0', 'end')
                mainWin.history['state'] = 'disabled'# 加锁history
                for entry in data['data']:
                    appendHistory(entry[0], entry[1], entry[2])
        elif data['type'] == 'peerJoined':
            users[data['peer']] = False
            refreshUserList()
        elif data['type'] == 'peerLeft':
            if data['peer'] in users.keys():
                del users[data['peer']]
            if data['peer'] == currentSession:
                currentSession = ''
                mainWin.sendFileBtn.configure(state='disabled')
                mainWin.name.set('%s -> global' % userName)
                users[''] = False
                lib.send(mySocket, {'command': 'getHistory', 'peer': ''})
            refreshUserList()
        elif data['type'] == 'msg':
            if data['peer'] == currentSession:
                now = datetime.now()
                appendHistory(data['peer'], now.strftime("%Y-%m-%d, %H:%M:%S"), data['msg'])
            else:
                users[data['peer']] = True
                refreshUserList()
        elif data['type'] == 'broadcast':
            if currentSession == '':
                now = datetime.now()
                appendHistory(data['peer'], now.strftime("%Y-%m-%d, %H:%M:%S"), data['msg'])
            else:
                users[''] = True
                refreshUserList()
        #文件接收
        elif data['type'] == 'fileReq':
            if tkinter.messagebox.askyesno('注意', '%s 想要发文件给你\文件名：%s\n大小: %s\n接收?' % (
            data['peer'], data['filename'], data['size'])):
                lib.send(mySocket, {'command': 'fileAccept', 'peer': data['peer']})
                try:
                    totalBytes = 0
                    addr = (lib.FILEIP, lib.FILEPORT)# 文件发送绑定ip，端口
                    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    server.bind(addr)
                    server.listen(5)
                    client_socket, addr = server.accept()
                    starttime = time.time()
                    with open(data['filename'], "wb") as f:
                        while True:
                            fdata = client_socket.recv(1024)
                            totalBytes += len(fdata)
                            if not fdata:
                                break
                            f.write(fdata)
                    f.close()
                    client_socket.close()
                    server.close()
                    endtime = time.time()
                    receivedMD5 = getfileMD5(data['filename'])# 文件名解密
                    if receivedMD5 == data['md5']:
                        tkinter.messagebox.showinfo('注意', '文件接收成功！')
                    mainWin.history['state'] = 'normal'
                    mainWin.history.insert('end', 'Received %s bytes from %s in %s seconds\n\n' % (totalBytes, data['peer'], format(endtime - starttime, '.2f')), 'hint')
                    mainWin.history.see('end')
                    mainWin.history['state'] = 'disabled'
                except:
                    pass
            else:
                lib.send(mySocket, {'command': 'fileDeny', 'peer': data['peer']})
        #文件被拒收
        elif data['type'] == 'fileDeny':
            mainWin.sendFileBtn.configure(text='发送文件')
            if currentSession == '':
                mainWin.sendFileBtn.configure(state='disabled')
            else:
                mainWin.sendFileBtn.configure(state='normal')
            tkinter.messagebox.showinfo('警告', '对方拒绝接收！')
        #文件发送
        elif data['type'] == 'fileAccept':
            try:
                totalBytes = 0
                starttime = time.time()
                addr = (data['ip'], lib.FILEPORT)
                client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                client.connect(addr)
                with open(filename, 'rb') as f:
                    while True:
                        fdata = f.read(1024)
                        if not fdata:
                            break
                        totalBytes += len(fdata)
                        client.send(fdata)
                f.close()
                client.close()
                endtime = time.time()
                mainWin.history['state'] = 'normal'
                mainWin.history.insert('end', 'Sent %s bytes in %s seconds\n\n' % (totalBytes, format(endtime - starttime, '.2f')), 'hint')
                mainWin.history.see('end')
                mainWin.history['state'] = 'disabled'
            finally:
                filename = ''
                filenameShortened = ''
                fileTransferPending = False
            mainWin.sendFileBtn.configure(text='发送文件')
            if currentSession == '':
                mainWin.sendFileBtn.configure(state='disabled')
            else:
                mainWin.sendFileBtn.configure(state='normal')
            tkinter.messagebox.showinfo('注意', '文件发送成功！')

#刷新用户列表并显示（*）显示有新消息
def refreshUserList():
    mainWin.userList.delete(0, 'end')
    for user in users.keys():
        name = '公共聊天室' if user == '' else user
        if users[user]:
            name += ' (*)'
        mainWin.userList.insert('end', name)

#将新发布的消息显示在聊天窗口
def appendHistory(sender, time, msg):
    mainWin.history['state'] = 'normal'
    mainWin.history.insert('end', '%s - %s\n' % (sender, time))
    mainWin.history.insert('end', msg + '\n\n', 'text')
    mainWin.history.see('end')
    mainWin.history['state'] = 'disabled'

#发送消息
def onSendBtnClicked():
    global mySocket, userName, currentSession, mainWin
    if mainWin.msg.get() != '':
        lib.send(mySocket, {'command': 'chat', 'peer': currentSession, 'msg': mainWin.msg.get()})
        now = datetime.now()
        appendHistory(userName, now.strftime("%Y-%m-%d, %H:%M:%S"), mainWin.msg.get())
        mainWin.msg.set('')
    else:
        tkinter.messagebox.showinfo('警告', '消息不能为空！')


#发送文件时的窗口响应
def onFileBtnClicked():
    global mySocket, mainWin, filename, filenameShortened, fileTransferPending
    try:
        filename = tkinter.filedialog.askopenfilename()
        if filename == '': return
        #文件的名称
        filenameShortened = ''
        if len(filename.split('/')) < len(filename.split('\\')):
            filenameShortened = filename.split('\\')[-1]
        else:
            filenameShortened = filename.split('/')[-1]
        #计算文件大小
        size = os.path.getsize(filename)
        count = 0
        while not 1 < size < 1024 and count < 6:
            size /= 1024
            count += 1
        size = str(format(size, '.2f')) + ['B', 'KB', 'MB', 'GB', 'TB', 'PB'][count]

        md5checksum = getfileMD5(filename)
        lib.send(mySocket, {'command': 'fileReq', 'peer': currentSession, 'filename': filenameShortened, 'size': size,'md5': md5checksum})
        mainWin.sendFileBtn.configure(text='等待中...')
        mainWin.sendFileBtn.configure(state='disabled')
        fileTransferPending = True
    except:
        sys.exit(1)

#用户列表选中一项时listbox进行响应
def onSessionSelect(event):
    global currentSession, mainWin, userName, users, fileTransferPending
    userlist = event.widget
    readFlag = False
    if len(userlist.curselection()) != 0:
        index = int(userlist.curselection()[0])
        if index != 0:
            if currentSession != userlist.get(index).rstrip(' (*)'):
                readFlag = True
                currentSession = userlist.get(index).rstrip(' (*)') # 当用户进入私聊窗口时清除用户列表中响应用户的未读标记并返回当前私聊对象的名字
                if not fileTransferPending:
                    mainWin.sendFileBtn.configure(state='normal') # 没有文件传输时用户可点击发送文件按钮
                mainWin.name.set('%s -> %s' % (userName, currentSession))
                users[currentSession] = False
                refreshUserList()
        elif index == 0:
            if currentSession != '':
                readFlag = True
                currentSession = ''
                mainWin.sendFileBtn.configure(state='disabled')
                mainWin.name.set('%s -> global' % userName)
                users[''] = False
                refreshUserList()
        if readFlag:
            lib.send(mySocket, {'command': 'getHistory', 'peer': currentSession})


def onClosed():
    closeSocket()

#对文件路径简单的MD5加密，返回加密后的16进制字符串
def getfileMD5(filePath):
    md5obj = hashlib.md5()
    maxbuf = 8192
    f = open(filePath, 'rb')
    while True:
        buf = f.read(maxbuf)
        if not buf:#buffer为空时停止读取
            break
        md5obj.update(buf)
    f.close()
    hash = md5obj.hexdigest()
    return str(hash).upper()


if __name__ == '__main__':
    loginWin = LoginWin()
    # loginWin.loginBtn.configure(command=onLoginBtnClicked)
    # loginWin.regBtn.configure(command=onRegBtnClicked)
    loginWin.show()
