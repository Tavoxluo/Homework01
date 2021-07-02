# -*- coding: utf-8 -*-
"""
Created on Thu Jul  1 10:09:01 2021

@author: 张高源
"""

import smtplib
import tkinter
from email.mime.text import MIMEText
from email.header import Header
from email.utils import parseaddr, formataddr

class Window:

    def __init__(self,root):
        #文本框和标签设置
        label1 = tkinter.Label(root,text='SMTP')#邮件服务器
        
        label2 = tkinter.Label(root,text='发地址')#发送地址
        
        label3 = tkinter.Label(root,text='授权码')#smtp授权码
        
        label4 = tkinter.Label(root,text='收地址')#收邮件地址

        label5 = tkinter.Label(root,text='主题')#邮件主题
        
        label6 = tkinter.Label(root,text='发件人')#发件人名
        
        label1.place(x=5,y=5)
        
        label2.place(x=5,y=55)
        
        label3.place(x=5,y=80)
        
        label4.place(x=5,y=105)
        
        label5.place(x=5,y=130)
        
        label6.place(x=5,y=155)
        
        self.entryPop = tkinter.Entry(root)
        
        self.entryFrom = tkinter.Entry(root)
        
        self.entryPass = tkinter.Entry(root,show = '*')#密码隐藏
        
        self.entryTo = tkinter.Entry(root)
        
        self.entrySub = tkinter.Entry(root)
        
        self.entryUser = tkinter.Entry(root)
        
        self.entryPop.place(x=50,y=5)
        
        self.entryFrom.place(x=50,y=55)

        self.entryPass.place(x=50,y=80)
        
        self.entryTo.place(x=50,y=105)
        
        self.entrySub.place(x=50,y=130)
        
        self.entryUser.place(x=50,y=155)
        
        self.get = tkinter.Button(root,text='发送邮件',command = self.Get)
        
        self.get.place(x=60,y=180)
        
        self.text=tkinter.Text(root)
        
        self.text.place(y=220)

    def Get(self):

        try:
            
            #获取文本框内容
            host = self.entryPop.get()
            
            user = self.entryUser.get()
            
            pw = self.entryPass.get()
            
            fromaddr = self.entryFrom.get()
            
            toaddr=self.entryTo.get()
            
            subject=self.entrySub.get()
            
            text = self.text.get(1.0,tkinter.END)
            
            server = smtplib.SMTP()
            
            server.connect(host)
            
            server.login(fromaddr,pw)
            
            message = MIMEText(text,'plain','utf-8')#邮件内容，纯文本，编码方式
            
            def _format_addr(s):
                
                    addr = parseaddr(s)
                    
                    return formataddr(addr)
                
            message['From'] = _format_addr(u'%s <%s>' % (user,fromaddr))#附上发送人
            
            message['Subject']= Header(subject,'utf-8')#附上主题
            
            server.sendmail(fromaddr,toaddr,message.as_string())#发送
            
            server.quit()#关闭链接
            
            self.text.insert(tkinter.END,'发送成功')
            
        except Exception as e:
            
            self.text.insert(tkinter.END,'发送失败')
        
root =tkinter.Tk()

window=Window(root)

root.minsize(600,500)

root.mainloop()
