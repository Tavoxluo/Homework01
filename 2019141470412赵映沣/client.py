
from tkinter import *
from tkinter import messagebox
import socket
import ssl
import base64
import time
import os
import random



class SendMail:
    #定义常见的文件头文件体字段
    __username=''#指代发件人邮箱
    __password=''#发件人的授权码
    __recipient=''#收件人邮箱
    msg = b'\r\n'
    endmsg = b'\r\n.\r\n'
    mailserver = ('smtp.qq.com', 465)
    heloCommand = b'HELO qq.com\r\n'
    loginCommand = b'AUTH login\r\n'
    dataCommand = b'DATA\r\n'
    quitCommand = b'QUIT\r\n'
    msgsubject = b'Subject: Test E-mail\r\n'
    msgtype = b"Content-Type: multipart/mixed;boundary='BOUNDARY'\r\n\r\n"#消息体中的内容是混合组合类型，
    #可以是文本、声音、附件等不同邮件内容混合，然后每段数据之间使用boundary属性中指定的字符文本作为分隔标识符
    msgboundary = b'--BOUNDARY\r\n'
    msgmailer = b'X-Mailer:zyf\'s mailer\r\n'
    msgMIMI = b'MIME-Version:1.0\r\n'
    msgfileType = b"Content-type:application/octet-stream;charset=utf-8\r\n"
    msgfilename = b"Content-Disposition: attachment; filename=''\r\n"
    msgimgtype = b"Content-type:image/gif;\r\n"#图片动图的邮件类型
    msgimgname = b"Content-Disposition: attachment; filename=''\r\n"
    msgtexthtmltype = b'Content-Type:text/html;\r\n'#文本或html类型的邮件
    msgimgId = b'Content-ID:<test>\r\n'
    msgimgscr = b'<img src="cid:test">'
    mailcontent = ''
    __clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


    def login(self):

        #界面设计
        root = Tk()
        root.title("登录界面")
        frame = Frame(root)
        frame.pack(padx=8, pady=8, ipadx=4)
        self.__sslclientSocket.send(self.loginCommand)
        recv2 = self.__sslclientSocket.recv(1024).decode('utf-8')
        lab1 = Label(frame, text="邮箱号:")
        lab1.grid(row=0, column=0, padx=5, pady=5, sticky=W)
        u = StringVar()
        ent1 = Entry(frame, textvariable=u)
        ent1.grid(row=0, column=1, sticky='ew', columnspan=2)
        lab2 = Label(frame, text="授权码:")
        lab2.grid(row=1, column=0, padx=5, pady=5, sticky=W)
        p = StringVar()
        ent2 = Entry(frame, textvariable=p)
        ent2.grid(row=1, column=1, sticky='ew', columnspan=2)
        def getuser():
            self.__username = ent1.get()#获取发件人邮箱文本框内的信息
            self.__password = ent2.get()#获取发件人授权码文本框内的信息
            username = b'%s\r\n' % base64.b64encode(self.__username.encode('utf-8'))#编码
            self.__sslclientSocket.send(username)#发送
            recv = self.__sslclientSocket.recv(1024).decode('utf-8')#解码
            password = b'%s\r\n' % base64.b64encode(self.__password.encode('utf-8'))
            self.__sslclientSocket.send(password)
            recv = self.__sslclientSocket.recv(1024).decode('utf-8')
            print(recv)
            if recv[:3] != '235':
                messagebox.showinfo('提示信息','登录失败：账号或密码错误，请使用授权码登录. 235 reply not received from server!')
                messagebox.showinfo('提示信息!','正在重试！')
                root.destroy()
                self.login()
            else:
                messagebox.showinfo('提示信息!','登录成功！')
                root.destroy()#登录成功后，调用窗口销毁函数，关闭当前窗口，然后打开新窗口
                mailsenderCommand = b'MAIL FROM:<%s>\r\n' % self.__username.encode('utf-8')
                self.__sslclientSocket.send(mailsenderCommand)
                root2 = Tk()
                root2.title("发送界面")
                root2.wm_geometry('400x400')
                frame2 = Frame(root2)
                frame2.pack(padx=8, pady=8, ipadx=4)
                lab10 = Label(frame2, text="收件人邮箱号:")
                lab10.grid(row=0, column=0, padx=5, pady=5, sticky=W)
                v = StringVar()
                ent3 = Entry(frame2, textvariable=v)
                ent3.grid(row=0, column=1, sticky='ew', columnspan=2)
                lab11 = Label(frame2,text="邮件主题:")
                lab11.grid(row=1, column=0, padx=5, pady=5, sticky=W)
                w = StringVar()
                ent4 = Entry(frame2, textvariable=w)
                ent4.grid(row=1, column=1, sticky='ew', columnspan=2)
                lab12 = Label(frame2,text="邮件正文:")
                lab12.grid(row=2, column=0, padx=5, pady=5, sticky=W)
                x = StringVar()
                ent5 = Entry(frame2,text="textvariable=x")
                ent5.grid(row=2, column=1, sticky='ew', columnspan=2)
                lab13 = Label(frame2,text="文件路径:")
                lab13.grid(row=3, column=0, padx=5, pady=5, sticky=W)
                y = StringVar()
                ent6 = Entry(frame2, textvariable=y)
                ent6.grid(row=3, column=1, sticky='ew', columnspan=2)
                filepath =""#将文件路径置为空，便于之后判断
                lab14 = Label(frame2,text="图片路径:")
                lab14.grid(row=4, column=0, padx=5, pady=5, sticky=W)
                z = StringVar()
                ent7 = Entry(frame2, textvariable=z)
                ent7.grid(row=4, column=1, sticky='ew', columnspan=2)
                imgpath=""#图片路径置空，便于之后判断
                def sendmaill():
                    self.__recipient = ent3.get()#获取收件人文本框的内容
                    subject = ent4.get()#获取邮件主题
                    filepath = ent6.get()#获取文件路径
                    imgpath = ent7.get()#获取图片路径
                    #print(self.__recipient)
                    #print(subject)
                    #print(filepath)
                    #print(imgpath)
                    if filepath=="":
                      if imgpath=="": #代表用户不需要发送附件和图片
                          mailrecipientCommand = b'RCPT TO:<%s>\r\n' % self.__recipient.encode('utf-8')#编码收件人邮箱信息
                          self.__sslclientSocket.send(mailrecipientCommand)#发送信息
                          recv = self.__sslclientSocket.recv(1024).decode('utf-8')
                          self.__sslclientSocket.send(self.dataCommand)#建立连接
                          recv = self.__sslclientSocket.recv(1024).decode('utf-8')
                          self.msgsubject = b'Subject: %s\r\n' % subject.encode('utf-8')#编码邮件主题
                          self.__sslclientSocket.send(self.msgsubject)#发送邮件主题
                          self.__sslclientSocket.send(self.msgmailer)#发送发件人邮箱
                          self.__sslclientSocket.send(self.msgtype)#发送邮件类型
                          self.__sslclientSocket.send(b'Content-Transfer-Encoding:7bit\r\n\r\n')
                          self.__sslclientSocket.send(b'\r\n\r\n' + self.msgboundary)
                          self.__sslclientSocket.send(b'Content-Type: text/html;charset=utf-8\r\n')
                          self.__sslclientSocket.send(b'Content-Transfer-Encoding:7bit\r\n\r\n')
                          self.mailcontent = ent5.get()#接收邮件正文部分的内容
                          self.__sslclientSocket.sendall(b'%s\r\n'%self.mailcontent.encode('utf-8'))#发送邮件正文部分
                          self.__sslclientSocket.send(self.endmsg)
                      else :#代表用户不需要发附件，只需要发送图片
                          mailrecipientCommand = b'RCPT TO:<%s>\r\n' % self.__recipient.encode('utf-8')
                          self.__sslclientSocket.send(mailrecipientCommand)
                          recv = self.__sslclientSocket.recv(1024).decode('utf-8')
                          self.__sslclientSocket.send(self.dataCommand)
                          recv = self.__sslclientSocket.recv(1024).decode('utf-8')
                          self.msgsubject = b'Subject: %s\r\n' % subject.encode('utf-8')
                          self.__sslclientSocket.send(self.msgsubject)
                          self.__sslclientSocket.send(self.msgmailer)
                          self.__sslclientSocket.send(self.msgtype)
                          self.__sslclientSocket.send(b'Content-Transfer-Encoding:7bit\r\n\r\n')
                          self.mailcontent = ent5.get()
                          if os.path.isfile(imgpath):
                            time.sleep(0.1)
                            filename = os.path.basename(imgpath)
                            randomid = filename.split('.')[1]+str(random.randint(1000, 9999)) 
                            time.sleep(0.1)
                            self.msgimgId = b'Content-ID:%s\r\n' % randomid.encode('utf-8')
                            self.__sslclientSocket.send(b'\r\n\r\n' + self.msgboundary)
                            self.__sslclientSocket.send(self.msgimgtype)#发送图片文件类型
                            self.__sslclientSocket.send(self.msgimgId)#发送图片获取的imgid
                            self.msgimgname = b"Content-Disposition: attachment; filename='%s'\r\n" % filename.encode('utf-8')
                            self.__sslclientSocket.send(self.msgfilename)
                            time.sleep(0.1)
                            self.__sslclientSocket.send(b'Content-Transfer-Encoding:base64\r\n\r\n')
                            self.__sslclientSocket.send(self.msg)
                            fb = open(imgpath, 'rb')
                            while True:
                                filedata = fb.read(1024)
                                if not filedata:
                                    break
                                self.__sslclientSocket.send(base64.b64encode(filedata))
                                time.sleep(0.1)
                            fb.close()
                            time.sleep(0.1)
                            self.__sslclientSocket.send(b'\r\n\r\n' + self.msgboundary)
                            self.__sslclientSocket.send(self.msgtexthtmltype)
                            self.__sslclientSocket.send(b'Content-Transfer-Encoding:8bit\r\n\r\n')#使用8bit的编码方式发送
                            msgimgscr = b'<img src="cid:%s">'%randomid.encode('utf-8')
                            time.sleep(0.1)
                            self.__sslclientSocket.send(msgimgscr)
                            time.sleep(0.1)
                            self.__sslclientSocket.sendall(b'%s' % self.mailcontent.encode('utf-8'))

                            time.sleep(0.1)
                            self.__sslclientSocket.send(self.endmsg)#发送结束消息
                    else :
                       if imgpath=="":#用户需要发附件，不需要发图片
                           mailrecipientCommand = b'RCPT TO:<%s>\r\n' % self.__recipient.encode('utf-8')
                           self.__sslclientSocket.send(mailrecipientCommand)
                           recv = self.__sslclientSocket.recv(1024).decode('utf-8')
                           self.__sslclientSocket.send(self.dataCommand)
                           recv = self.__sslclientSocket.recv(1024).decode('utf-8')
                           self.msgsubject = b'Subject: %s\r\n' % subject.encode('utf-8')
                           self.__sslclientSocket.send(self.msgsubject)
                           self.__sslclientSocket.send(self.msgmailer)
                           self.__sslclientSocket.send(self.msgtype)
                           self.__sslclientSocket.send(b'Content-Transfer-Encoding:7bit\r\n\r\n')
                           self.__sslclientSocket.send(b'\r\n\r\n' + self.msgboundary)
                           self.__sslclientSocket.send(b'Content-Type: text/html;charset=utf-8\r\n')
                           self.__sslclientSocket.send(b'Content-Transfer-Encoding:7bit\r\n\r\n')
                           self.mailcontent = ent5.get()
                           self.__sslclientSocket.sendall(b'%s\r\n'%self.mailcontent.encode('utf-8'))
                           if os.path.isfile(filepath):
                                filename = os.path.basename(filepath)
                                self.__sslclientSocket.send(b'\r\n\r\n' + self.msgboundary)
                                self.__sslclientSocket.send(self.msgfileType)
                                self.msgfilename = b"Content-Disposition: attachment; filename='%s'\r\n" % filename.encode('utf-8')
                                self.__sslclientSocket.send(self.msgfilename)
                                self.__sslclientSocket.send(b'Content-Transfer-Encoding:base64\r\n\r\n')
                                self.__sslclientSocket.send(self.msg)
                                fb = open(filepath,'rb')
                                while True:
                                    filedata = fb.read(1024)
                                    # print(filedata)
                                    if not filedata:
                                        break
                                    self.__sslclientSocket.send(base64.b64encode(filedata))
                                    time.sleep(1)
                                fb.close()
                                time.sleep(0.1)
                                self.__sslclientSocket.send(self.endmsg)
                       else :#用户需要发附件也需要发图片
                          mailrecipientCommand = b'RCPT TO:<%s>\r\n' % self.__recipient.encode('utf-8')
                          self.__sslclientSocket.send(mailrecipientCommand)
                          recv = self.__sslclientSocket.recv(1024).decode('utf-8')
                          self.__sslclientSocket.send(self.dataCommand)
                          recv = self.__sslclientSocket.recv(1024).decode('utf-8')
                          self.msgsubject = b'Subject: %s\r\n' % subject.encode('utf-8')
                          self.__sslclientSocket.send(self.msgsubject)
                          self.__sslclientSocket.send(self.msgmailer)
                          self.__sslclientSocket.send(self.msgtype)
                          self.__sslclientSocket.send(b'Content-Transfer-Encoding:7bit\r\n\r\n')
                          self.mailcontent = ent5.get()
                          if os.path.isfile(imgpath):
                            time.sleep(0.1)
                            filename = os.path.basename(imgpath)
                            randomid = filename.split('.')[1]+str(random.randint(1000, 9999)) 
                            time.sleep(0.1)
                            self.msgimgId = b'Content-ID:%s\r\n' % randomid.encode('utf-8')
                            self.__sslclientSocket.send(b'\r\n\r\n' + self.msgboundary)
                            self.__sslclientSocket.send(self.msgimgtype)
                            self.__sslclientSocket.send(self.msgimgId)
                            self.msgimgname = b"Content-Disposition: attachment; filename='%s'\r\n" % filename.encode('utf-8')
                            self.__sslclientSocket.send(self.msgfilename)
                            time.sleep(0.1)
                            self.__sslclientSocket.send(b'Content-Transfer-Encoding:base64\r\n\r\n')
                            self.__sslclientSocket.send(self.msg)
                            fb = open(imgpath, 'rb')
                            while True:
                                filedata = fb.read(1024)
                                if not filedata:
                                    break
                                self.__sslclientSocket.send(base64.b64encode(filedata))
                                time.sleep(0.1)
                            fb.close()
                            time.sleep(0.1)
                            self.__sslclientSocket.send(b'\r\n\r\n' + self.msgboundary)
                            self.__sslclientSocket.send(self.msgtexthtmltype)
                            self.__sslclientSocket.send(b'Content-Transfer-Encoding:8bit\r\n\r\n')
                            msgimgscr = b'<img src="cid:%s">'%randomid.encode('utf-8')
                            time.sleep(0.1)
                            self.__sslclientSocket.send(msgimgscr)
                            time.sleep(0.1)
                            self.__sslclientSocket.sendall(b'%s' % self.mailcontent.encode('utf-8'))
                            time.sleep(0.1)
                            if os.path.isfile(filepath):
                                filename = os.path.basename(filepath)
                                self.__sslclientSocket.send(b'\r\n\r\n' + self.msgboundary)
                                self.__sslclientSocket.send(self.msgfileType)
                                self.msgfilename = b"Content-Disposition: attachment; filename='%s'\r\n" % filename.encode('utf-8')
                                self.__sslclientSocket.send(self.msgfilename)
                                self.__sslclientSocket.send(b'Content-Transfer-Encoding:base64\r\n\r\n')
                                self.__sslclientSocket.send(self.msg)
                                fb = open(filepath,'rb')
                                while True:
                                    filedata = fb.read(1024)
                                    
                                    if not filedata:
                                        break
                                    self.__sslclientSocket.send(base64.b64encode(filedata))
                                    time.sleep(1)
                                fb.close()
                                time.sleep(0.1)
                            
                 
                            self.__sslclientSocket.send(self.endmsg)
                    messagebox.showinfo('提示信息','发送成功！')
                button1 = Button(frame2, text="发送", command=sendmaill, default='active')#为发送按钮定义一个事件sendmaill，点击的时候调用
                button1.grid(row=5, column=1)
                button3 = Button(frame2, text="退出", command=quit)
                button3.grid(row=5, column=2, padx=5, pady=5)
                

        button = Button(frame, text="登录", command=getuser, default='active')#为登录按钮定义一个事件getuser，点击的时候调用
        button.grid(row=2, column=1)
        lab3 = Label(frame, text="")
        lab3.grid(row=2, column=0, sticky=W)
        button2 = Button(frame, text="退出", command=quit)
        button2.grid(row=2, column=2, padx=5, pady=5)

        #以下代码居中显示窗口

        root.update_idletasks()
        x = (root.winfo_screenwidth() - root.winfo_reqwidth()) / 2
        y = (root.winfo_screenheight() - root.winfo_reqheight()) / 2
        root.geometry("+%d+%d" % (x, y))
        root.mainloop()

        





    #使用socket套接字连接qq邮箱服务器，并设置ssl验证
    def socketconnet(self):
        print("正在连接服务器……")
        self.__sslclientSocket = ssl.wrap_socket(self.__clientSocket, cert_reqs=ssl.CERT_NONE,
                                            ssl_version=ssl.PROTOCOL_SSLv23)
        self.__sslclientSocket.connect(self.mailserver)
        recv = self.__sslclientSocket.recv(1024).decode('utf-8')
        if recv[:3] != '220':
            print('服务器连接失败：220 reply not received from server.')
            print('正在重试……')
            self.socketconnet()
        print("成功连接服务器……")
        print("正在请求服务器响应……")
        self.__sslclientSocket.send(self.heloCommand)
        recv1 = self.__sslclientSocket.recv(1024).decode('utf-8')
        if recv1[:3] != '250':
            print('服务器响应失败：250 replay not received from server')
            time.sleep(2)
            print('正在重试……')
            self.socketconnet()
        print("成功请求服务器响应……")
        

    
    
   



if __name__ == '__main__':
    try:
        sendmail = SendMail()
        sendmail.socketconnet()
        sendmail.login()
        sendmail.quitconnect()
        
    except Exception:
            print(Exception)
    finally:
        exit(0)
