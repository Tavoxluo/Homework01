from tkinter import *
from tkinter.messagebox import *
from MainPage import *
from client import *


class Account(object):
    def __init__(self, master=None):
        self.root = master  # 定义内部变量root
        self.root.geometry('%dx%d' % (300, 180))  # 设置窗口大小
        self.username = StringVar()
        self.password = StringVar()
        self.createPage()

    def createPage(self):
        self.page = Frame(self.root)  # 创建Frame
        self.page.pack()
        Label(self.page).grid(row=0, stick=W)
        Label(self.page, text='请输入您的昵称: （自选择匿名）').grid(row=1, stick=W, pady=10)
        Label(self.page, text='昵称: ').grid(row=2, stick=W, pady=10)
        Entry(self.page, textvariable=self.username).grid(row=2, column=1, stick=E)
        Button(self.page, text='确定', command=self.loginCheck).grid(row=3, stick=W, pady=10)

    def loginCheck(self):
        name = self.username.get()
        secret = self.password.get()
        if name == 'wangliang' and secret == '123456':
            self.page.destroy()
            MainPage(self.root)
        else:
            showinfo(title='错误', message='账号或密码错误！')
