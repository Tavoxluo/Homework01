#!/usr/bin/env python3  
#coding: utf-8  
import smtplib  
from tkinter import *
from email.mime.text import MIMEText  
from email.header import Header  
  
mail_host = "smtp.163.com"  # 设置服务器
mail_user = "luobinhe_vip.com"  # 用户名
mail_pass = "OTJZCUFHJIEZNWVH"  # 授权码
me = "luobinhe_vip" + "<" + "luobinhe_vip@163.com" + ">"

'''发送函数'''
def sendmail(mail_receiver, mail_subject, mail_content):

    msg = MIMEText(mail_content, 'plain', 'utf-8')#中文需参数‘utf-8’，单字节字符不需要 
    msg['Subject'] = mail_subject
    msg['From'] = me
    msg['To'] = ";".join(mail_receiver)

    try:
        smtp = smtplib.SMTP()  
        smtp.connect('smtp.163.com')  
        smtp.login(mail_user, mail_pass)  
        smtp.sendmail(mail_user, mail_receiver, msg.as_string())  
        smtp.quit()
    except smtplib.SMTPException:
        print("Error: 邮件发送错误")
  

'''可视化界面'''
def client():

    top = Tk()
    top.title("邮件发送客户端")
    top.geometry('600x700')

    '''发送人'''
    Label(top, text="发送人:", bg="yellow",font="等线", width=10, height=1).place(x=30, y=30)
    Label(top, text="luobinhe_vip@163.com",font="等线",bg="white", width=20, height=1).place(x=170, y=30)

    '''接收人'''
    Label(top, text="接收人:", bg="yellow",font="等线",width=10, height=1).place(x=30,y=70)
    receiver_entry = Entry(top,width=50)
    receiver_entry.place(x=170,y=70)

    '''主题'''
    Label(top, text="主题:", bg="yellow",font="等线",width=10, height=1).place(x=30,y=110)
    subject_entry = Entry(top,  width=50)
    subject_entry.place(x=170, y=110)

    '''内容'''
    Label(top, text="内容:", bg="yellow",font="等线",width=10, height=1).place(x=30,y=150)
    content_text = Text(top,width=60,height=20)
    content_text.place(x=30,y=190)

    def clearcontent():
        content_text.delete('0.0','end')

    def send():
        receiver = receiver_entry.get()
        subject = subject_entry.get()
        content = content_text.get('0.0','end')
        if "@" in receiver:
            try:
                sendmail(receiver,subject,content)
                print("邮件已发送")
            except IOError:
                print("发送失败")
        else:
            print("邮箱格式不对\n请确认接收人邮箱")

    '''按钮'''
    Button(top,text="清空",bd=5,font="等线",width=10,command=clearcontent).place(x=30,y=460)
    Button(top,text="发送",bd=5,font="等线",width=10,command=send).place(x=170,y=460)

    top.mainloop()

if __name__ == '__main__':
    client()
