from socket import *
import tkinter as tk
import tkinter.scrolledtext as tst
import time
import tkinter.messagebox
import threading


class Application(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        self.grid()
        self.createWidgets()

    def createWidgets(self):
        # 显示聊天窗口
        self.textEdit = tst.ScrolledText(self, width=50, height=15)
        self.textEdit.grid(row=0, column=0, rowspan=1, columnspan=4)
        # 定义标签，改变字体颜色
        self.textEdit.tag_config('server', foreground='red')
        self.textEdit.tag_config('guest', foreground='green')

        # 编辑窗口
        self.inputText = tk.Text(self, width=40, height=5)
        self.inputText.grid(row=1, column=0, columnspan=1)
        # 按下回车即可发送消息
        self.inputText.bind("<KeyPress-Return>", self.textSendReturn)
        # 发送按钮
        self.btnSend = tk.Button(self, text='send', command=self.textSend)
        self.btnSend.grid(row=1, column=3)
        # 开启一个线程用于接收消息并显示在聊天窗口
        t = threading.Thread(target=self.getInfo)
        t.start()

    def textSend(self):
        # 获取Text的所有内容
        str = self.inputText.get('1.0', 'end-1c')
        if str != "":
            # 显示发送时间和发送消息
            timemsg = '服务端' + time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()) + '\n'
            self.textEdit.config(state='normal')
            self.textEdit.insert(tk.END, timemsg, 'server')
            self.textEdit.insert(tk.END, str + '\n')
            # 将滚动条拉到最后显示最新消息
            self.textEdit.see(tk.END)
            self.textEdit.config(state='disabled')
            self.inputText.delete(0.0, tk.END)  # 删除输入框的内容
            # 发送数据到服务端
            sendMessage = bytes(str, encoding='utf8')
            # 发送输入的数据
            connectionSocket.send(sendMessage)
        else:
            tk.messagebox.showinfo('警告', "不能发送空白信息！")

    def getInfo(self):
        while True:
            recMsg = connectionSocket.recv(1024).decode("utf-8") + '\n'
            revTime = '客户端' + time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()) + '\n'
            # 通过设置state属性设置textEdit可编辑
            self.textEdit.config(state='normal')
            self.textEdit.insert(tk.END, revTime, 'guest')
            self.textEdit.insert(tk.END, recMsg)
            # 将滚动条拉到最后显示最新消息
            self.textEdit.see(tk.END)
            # 通过设置state属性设置textEdit不可编辑
            self.textEdit.config(state='disabled')

    def textSendReturn(self, event):
        if event.keysym == "Return":
            self.textSend()


root = tk.Tk()
root.title('服务端')

# 网络相关
# 指定服务器使用的端口
serverPort = 10000
serverSocket = socket(AF_INET, SOCK_STREAM)
# 绑定端口
serverSocket.bind(('127.0.0.2', serverPort))
# 定义最大连接数
serverSocket.listen(5)
print('等待连接....')
# 接受请求则建立一个连接
connectionSocket, addr = serverSocket.accept()
print('一个连接')
app = Application(master=root)
app.mainloop()