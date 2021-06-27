# coding=UTF-8
import sys
import tkinter
import socket
import threading
import time
from tkinter import scrolledtext, messagebox


def readFromServer(s):
    while True:
        # 线程中运行接受数据函数，本地调用函数获取接收消息时间，打印
        content = s.recv(2048).decode()
        text.insert(tkinter.INSERT, time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()) + '\n')
        text.insert(tkinter.INSERT, content+'\n\n')

def sendMessage():
    # 从输入框中获取目标对象与消息文本，并发送至服务器
    tar = efriend.get()
    line = esend.get()
    # 设定$字符为清空消息框与消息记录
    if line=='$':
        text.delete(1.0,'end')
    else:
        s.send(tar.encode() + '$'.encode() + line.encode())
        text.insert(tkinter.INSERT, time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()) + '\n')
        text.insert(tkinter.INSERT, 'you: '+ line + '\n\n')


def sendNickname():
    # 登陆函数，从输入框中获取服务器ip与端口号
    host = eip.get()
    port = eport.get()
    # 创建全局变量s，并创建socket
    global s
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((host, int(port)))
    # 获取昵称，创建接收服务器消息的线程，并向服务器发送登陆消息
    nickName = euser.get()
    t=threading.Thread(target=readFromServer, args=(s,))
    # 守护线程，为了使主线程结束时关闭子线程
    t.daemon=1
    t.start()
    s.send(nickName.encode())

# 窗体关闭时结束进程
def my_close():
    # True or Flase
    res = messagebox.askokcancel('提示', '是否关闭窗口')
    if res == True:
        if res == True:
            win.destroy()

# 以下为前台界面代码

win = tkinter.Tk()

win.title("聊天客户端")
win.geometry("545x400+600+400")
win.protocol('WM_DELETE_WINDOW', my_close)
labelUse = tkinter.Label(win, text="用户名").grid(row=0, column=0)
euser = tkinter.Variable()
entryUser = tkinter.Entry(win, textvariable=euser).grid(row=0, column=1)

labelIp = tkinter.Label(win, text="服务器ip").grid(row=1, column=0)
eip = tkinter.Variable()
entryIp = tkinter.Entry(win, textvariable=eip).grid(row=1, column=1)

labelPort = tkinter.Label(win, text="端口port").grid(row=2, column=0)
eport = tkinter.Variable()
entryPort = tkinter.Entry(win, textvariable=eport).grid(row=2, column=1)

button = tkinter.Button(win, text="登录", command=sendNickname).grid(row=1, column=2)

text = scrolledtext.ScrolledText(win, height=20, width=60)
labeltext = tkinter.Label(win, text="消息框").grid(row=4, column=0)
text.grid(row=4, column=1)

esend = tkinter.Variable()
labelesend = tkinter.Label(win, text="发送的消息").grid(row=6, column=0)
entrySend = tkinter.Entry(win, textvariable=esend).grid(row=6, column=1)

efriend = tkinter.Variable()
labelefriend = tkinter.Label(win, text="发给谁").grid(row=5, column=0)
entryFriend = tkinter.Entry(win, textvariable=efriend).grid(row=5, column=1)

button2 = tkinter.Button(win, text="发送", command=sendMessage).grid(row=6, column=2)

win.mainloop()
sys.exit(0)









