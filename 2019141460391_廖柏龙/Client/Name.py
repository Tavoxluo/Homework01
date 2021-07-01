from tkinter import *
from tkinter.messagebox import *
from MainPage import *
from Client import *


class Name(object):
    def __init__(self, master=None):
        self.root = master  # 定义内部变量root
        self.username = StringVar()
        self.password = StringVar()
        self.createPage()

    def createPage(self):
        self.page = Frame(self.root)  # 创建Frame
        self.page.pack()
        Label(self.page).grid(row=0, stick=W)
        Label(self.page, text='请输入您的昵称!').grid(row=1, stick=W, pady=10)
        Label(self.page, text='昵称: ').grid(row=2, stick=W, pady=10)
        Entry(self.page, textvariable=self.username).grid(row=2, column=1, stick=E)
        Button(self.page, text='确定', command=self.getCheck).grid(row=3, stick=W, pady=10)

    def getCheck(self):
        account = self.username.get()
        #print(name)
        #tcp.send(account.encode('gbk'))
        if login(account):
            self.page.destroy()
            MainPage(self.root)
        else:
            showinfo(title='错误', message='用户名已存在！')
