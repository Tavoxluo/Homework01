from tkinter import *
import socket
import time
import threading
from tkinter import scrolledtext

#定义一个client类
class client():
    def __init__(self):
        self.root=Tk()
        self.root.title('我是client')
        self.root.geometry('600x400')
        self.sk=socket.socket()
        self.server_ip='127.0.0.1'
        self.server_port=int(8888)
        self.recvbuf=str()#接收区缓存
        self.sendbuf=str()#发送区缓存
        self.recvstr=StringVar(value=self.recvbuf)
        self.sendstr=StringVar(value=self.sendbuf)
        self.ip=StringVar(value=self.server_ip)
        self.port=IntVar(value=self.server_port)
        #标签
        self.ip_label=Label(self.root,text='输入服务器IP地址')
        self.port_label=Label(self.root,text='输入服务器端口号(大于1024即可)')
        self.c_label=Label(self.root,text='输入框')
        self.s_label=Label(self.root,text='当前收到')
        self.recorde_label=Label(self.root,text='聊天记录（请在建立连接后通信）')
        #文本框
        self.ip_entry=Entry(self.root,textvariable=self.ip)
        self.port_entry=Entry(self.root,textvariable=self.port)
        self.c_entry=Entry(self.root,textvariable=self.sendstr)
        self.s_entry=Entry(self.root,textvariable=self.recvstr,state='disabled')
        self.recorde=scrolledtext.ScrolledText(self.root,width=50,height=10)
        #按钮
        self.btn0=Button(self.root,text='建立连接',command=lambda:self.started(self.ip,self.port))
        self.btn1=Button(self.root,text='发送',command=lambda:self.sending(self.sk))
        #排列
        self.c_label.grid(row=0,column=0)
        self.c_entry.grid(row=0,column=1)
        self.s_label.grid(row=1,column=0)
        self.s_entry.grid(row=1,column=1)
        self.btn0.grid(row=2,column=0)
        self.btn1.grid(row=2,column=1)
        self.ip_entry.grid(row=3,column=1)
        self.ip_label.grid(row=3,column=0)
        self.port_entry.grid(row=4,column=1)
        self.port_label.grid(row=4,column=0)
        self.recorde_label.grid(row=5,column=1)
        self.recorde.grid(row=6,column=1)
        self.root.after(500,self.update)
        self.root.mainloop()
    #开始连接
    def started(self,ip,port):
        self.recorde.insert(INSERT,'waiting...\n')
        self.sk.connect((self.server_ip,self.server_port))
        print('连接成功')
        self.recorde.insert(INSERT,time.strftime('%Y-%m-%d %H:%M:%S')+' connected\n')
        return
    #发送数据
    def senddata(self,s):
        self.sendbuf=self.sendstr.get()
        s.send(bytes(self.sendbuf,'utf8'))
        self.recorde.insert(INSERT,time.strftime('%Y-%m-%d %H:%M:%S')+' 客户端:'+self.sendbuf+'\n')
        return
    #接收数据
    def recvdata(self,s):
        try :
            self.recvbuf=str(s.recv(1024),'utf8')
            if not self.recvbuf:
                return
            self.recvstr.set(self.recvbuf)
            self.recorde.insert(INSERT,time.strftime('%Y-%m-%d %H:%M:%S')+' 服务器:'+self.recvbuf+'\n')
        except Exception as e:
            print(e)
        return
    #对senddata()和recvdata()方法采用多线程
    def sending(self,s):
        threading.Thread(target=self.senddata,args=(s,)).start()
        return
    def recving(self,s):
        threading.Thread(target=self.recvdata,args=(s,)).start()
        return
    #更新缓存区
    def update(self):
        try:
            self.recving(self.sk)
        except Exception as e:
            print(e)
        self.root.after(500,self.update)
        return

if __name__=='__main__':
    app=client()
