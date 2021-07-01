import tkinter as tk
from tkinter import messagebox
from smtplib import SMTP
from email.header import Header
from email.mime.text import MIMEText
import time
#设置tkinter主界面
window = tk.Tk()
window.title('快乐代码')
window.geometry('800x700')
#设置各种输入框
l_1 = tk.Label(window, text='请输入发送邮箱：')
l_1.grid(row=0)
e_sender = tk.Entry(window, show = None)
e_sender.grid(row=0, column=1, sticky=tk.W)
l_2 = tk.Label(window, text='请输入发送邮箱授权码：')
l_2.grid(row=1)
e_password = tk.Entry(window, show = None)
e_password.grid(row=1, column=1, sticky=tk.W)
tk.Label(window, text="请输入接收邮箱：").grid(row=2)
e_receivers = tk.Entry(window, width=70,show = None)
e_receivers.grid(row=2, column=1, sticky=tk.W)
tk.Label(window, text='请输入发送内容标题：').grid(row=3)
e_title = tk.Entry(window, show=None)
e_title.grid(row=3, column=1, sticky=tk.W)
tk.Label(window, text='请输入发送内容：').grid(row=4)
t = tk.Text(window)
t.grid(row=4, column=1, sticky=tk.W)
tk.Label(window, text='请输入发送次数：').grid(row=5)
e_times = tk.Entry(window, show = None)
e_times.grid(row=5, column=1, sticky=tk.W)
tk.Label(window, text='请设置发送时间间隔(单位s):').grid(row=6)
e_sleep = tk.Entry(window, show = None)
e_sleep.grid(row=6, column=1, sticky=tk.W)
#获取用户输入的值赋值给变量
def submit():
    global sender
    sender = e_sender.get()
    global password
    password = e_password.get()
    global receivers
    receivers = e_receivers.get()
    global something
    something = t.get('0.0','end')
    global times
    times = e_times.get()
    global sleep
    sleep = e_sleep.get()
    global title
    title = e_title.get()
#发送邮件    
def do():
    message = MIMEText(something, 'plain', 'utf-8')
    message['From'] =sender  #发件人
    message['To'] = receivers   #收件人
    subject = title
    message['Subject'] = Header(subject, 'utf-8') #邮件头设置
    smtper = SMTP('smtp.163.com')     #服务器地址
    #请自行修改下面的登录口令
    smtper.login(sender,password) #此处password输入授权码
    #循环发送times次
    for i in range(int(times)):
        smtper.sendmail(sender, receivers, message.as_string()) 
        time.sleep(int(sleep)) #设置发送间隔
    tk.messagebox.showinfo(title='好哇', message='邮件发送成功'+times+'次！')   
    
tk.Button(window, text='提交', command=submit).grid(row=7)
tk.Button(window, text='发送', command=do).grid(row=7, column=1)  
window.mainloop()
