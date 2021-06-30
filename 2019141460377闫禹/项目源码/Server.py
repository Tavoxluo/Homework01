from socket import *
import tkinter as tk
import tkinter.scrolledtext
import time
import threading
import tkinter.messagebox


#global clientSocket
def clicked():
    string = textField.get('1.0', 'end-1c')
    if string != '':
        #显示发送时间和发送消息
        txt = '服务器端' + time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
        text.config(state='normal')
        text.insert(tk.END, txt + '\n')
        text.insert(tk.END, string + '\n')
        text.see(tk.END)
        text.config(state='disabled')
        textField.delete(0.0, tk.END)
        connectionSocket.send(string.encode())
    else:
        tk.messagebox.showerror('错误', "发送结果不能为空")


def getMessage():#此方法为接受信息
    while True:
        recvMessage = connectionSocket.recv(1024)
        recvTime = "客户端" + time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())#确定的时间格式
        text.config(state='normal')
        text.insert(tk.END, recvTime + '\n')
        text.insert(tk.END, recvMessage.decode() + '\n')
        text.see(tk.END)
        text.config(state='disabled')






serverPort = 11001
serverSocket = socket(AF_INET, SOCK_STREAM)
#serverSocket.bind(('127.0.0.1',serverPort))
serverSocket.bind(('127.0.0.1',serverPort))
serverSocket.listen(2)
print("the server is ready to receive")
connectionSocket, address = serverSocket.accept()



re = tk.Tk()
re.title("服务器端")
re.geometry("350x200")
text = tk.scrolledtext.ScrolledText(re, width=45, height=10)
text.grid(column=0, row=0, rowspan=1, columnspan=4)
textField = tk.Text(re, width=40, height=3)
textField.grid(column=0, row=1, columnspan=1)
bn1 = tk.Button(re, text="发送", command=clicked)
bn1.grid(column=1, row=1)


print("hello")
t = threading.Thread(target=getMessage)
t.start()
re.mainloop()

