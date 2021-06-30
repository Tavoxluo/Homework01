from tkinter import *
import socket
import time
import threading
from tkinter import scrolledtext
#定义一个server类
class server():
    def __init__(self):
        self.root=Tk()
        self.root.title('我是server')
        self.root.geometry('600x400')
        self.recvbuf=str()#接收区缓存
        self.sendbuf=str()#发送区缓存
        self.recvstr=StringVar(value=self.recvbuf)
        self.sendstr=StringVar(value=self.sendbuf)
        #标签
        self.ip_label=Label(self.root,text='输入服务器IP地址')
        self.port_label=Label(self.root,text='输入服务器端口号')
        self.s_label=Label(self.root,text='输入框')
        self.c_label=Label(self.root,text='当前收到')
        self.recorde_label=Label(self.root,text='聊天记录（请在建立连接后通信）')
        #文本框
        self.c_entry=Entry(self.root,textvariable=self.sendstr)
        self.s_entry=Entry(self.root,textvariable=self.recvstr,state='disabled')
        self.recorde=scrolledtext.ScrolledText(self.root,width=50,height=10)
        #按钮
        self.btn0=Button(self.root,text='建立连接',command=lambda:self.starting())
        self.btn1=Button(self.root,text='发送',command=lambda:self.sending())
        #排列
        self.s_label.grid(row=0,column=0)
        self.c_entry.grid(row=0,column=1)
        self.c_label.grid(row=1,column=0)
        self.s_entry.grid(row=1,column=1)
        self.btn0.grid(row=2,column=0)
        self.btn1.grid(row=2,column=1)
        self.recorde_label.grid(row=5,column=1)
        self.recorde.grid(row=6,column=1)
        self.root.after(500,self.update)
        self.root.mainloop()
    #开始连接
    def started(self):
        self.s=socket.socket()
        self.s.bind(('127.0.0.1',8888))
        self.s.listen(1)
        self.recorde.insert(INSERT,'waiting...')
        self.client,self.addr=self.s.accept()
        self.recorde.insert(INSERT,time.strftime('%Y-%m-%d %H:%M:%S')+'当前连接到IP为'+str(self.addr[0])+'端口号为'+str(self.addr[1])+'\n')
        return
    #发送数据
    def senddata(self):
        self.sendbuf=self.sendstr.get()
        self.client.send(bytes(self.sendbuf,'utf8'))
        self.recorde.insert(INSERT,time.strftime('%Y-%m-%d %H:%M:%S')+' 服务器:'+self.sendbuf+'\n')
        return
    #接收数据
    def recvdata(self):
        try :
            self.recvbuf=str(self.client.recv(1024),'utf8')
            if not self.recvbuf:
                return
            self.recvstr.set(self.recvbuf)
            self.recorde.insert(INSERT,time.strftime('%Y-%m-%d %H:%M:%S')+' 客户端:'+self.recvbuf+'\n')
        except Exception as e:
            print(e)
        return
    #对start(),senddata()和recvdata()方法采用多线程
    def starting(self):
        threading.Thread(target=self.started).start()
        return
    def sending(self):
        threading.Thread(target=self.senddata).start()
        return
    def recving(self):
        threading.Thread(target=self.recvdata).start()
        return
    #更新缓存区
    def update(self):
        try:
            self.recving()
        except Exception as e:
            print(e)
        self.root.after(500,self.update)
        return

if __name__=='__main__':
    ser=server()
