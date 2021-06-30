from tkinter import Tk, Frame, Text, Button, END
from Client import *
import tkinter.font as tf
from threading import Thread
import socket

class MainPage(object):

    def __init__(self, master=None):
        self.root = master  # 定义内部变量root
        self.root.geometry('%dx%d' % (500, 530))  # 设置窗口大小
        self.root.title('匿名聊天室')
        message_frame = Frame(width=480, height=300, bg='white')
        message_exit = Frame(width=480, height=50, bg='white')
        text_frame = Frame(width=480, height=100)
        send_frame = Frame(width=480, height=30)

        def closeWindow():
            #本来作为退出标识符的，后来选择直接退出
            #tcp.send('x0000000'.encode('gbk'))
            self.root.destroy()
            return

        #使用while实现实时的获取从服务器端广播的数据
        def get_msg():
            while True:
                try:
                    information = tcp.recv(1024).decode('gbk')
                    note = information[0:1]
                    msg = information[2:]
                    text_exit.configure(state='normal')
                    text_message.configure(state='normal')
                    #每次都插入数据，并显示为最新的数据
                    if note == 'M':
                        text_message.insert(END, msg,'tag')
                        text_message.see(END)
                        text_exit.configure(state='disabled')
                        text_message.configure(state='disabled')
                    elif note == 'E':
                        text_exit.insert('end',msg)
                        text_exit.see('end')
                        text_exit.configure(state='disabled')
                        text_message.configure(state='disabled')
                except:
                    text_exit.configure(state='disabled')
                    text_message.configure(state='disabled')
                    break

        #当点击按钮时，触发这个函数，将消息框内的信息发送给客户端
        #此时客户端反馈给所有的在线用户
        def send():
            send_msg = text_text.get('0.0', END)
            if send_msg.endswith('\n'):
                send_msg = send_msg[:-1]
            if send_msg != "":
                tcp.send(('M:'+send_msg).encode('gbk'))
            text_text.delete('0.0', END)

        #自退出定义
        self.root.protocol('WM_DELETE_WINDOW', closeWindow)

        text_message = Text(message_frame)
        text_text = Text(text_frame)
        text_exit = Text(message_exit)
        button_send = Button(send_frame, text='发送', command=send)

        text_exit.configure(state='disabled')
        text_message.configure(state='disabled')

        # GUI窗口布局配置
        message_frame.grid(row=0,column=0, padx=3,pady=6)
        message_exit.grid(row=1,column=0, padx=3,pady=6)
        text_frame.grid(row=2, column=0, padx=3, pady=6)
        send_frame.grid(row=3, column=0)

        message_frame.grid_propagate(0)
        message_exit.grid_propagate(0)
        text_frame.grid_propagate(0)
        send_frame.grid_propagate(0)

        #设置text参数，在END处
        ft = tf.Font(family='微软雅黑', size=12)
        text_message.tag_add('tag',END)  # 申明一个tag,在a位置使用
        text_message.tag_config('tag', foreground='green', font=ft)  # 设置tag即插入文字的大小,颜色等

        # 布局管理
        text_message.grid()
        text_exit.grid()
        text_text.grid()
        button_send.grid()

        # 线程管理，实时的从服务器端获取数据,并将其设置为守护线程,当窗口关闭时，线程关闭
        msg_thread = Thread(target=get_msg)
        msg_thread.daemon = True
        msg_thread.start()
