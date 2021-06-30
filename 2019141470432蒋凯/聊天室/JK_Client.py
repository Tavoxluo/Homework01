import socket
import tkinter
from tkinter import font
import tkinter.messagebox
import threading
import json
import tkinter.filedialog
from tkinter.scrolledtext import ScrolledText

IP = ''
PORT = ''
user = ''
listbox1 = ''  # 用于显示在线用户的列表框
show = 1  # 用于判断是开还是关闭列表框
users = []  # 在线用户列表
chat = '--------------------------'  # 聊天对象

#登陆窗口

root0 = tkinter.Tk()   #创建窗体
root0.geometry("300x150")
root0.title('登录界面')
root0.resizable(0,0)
one = tkinter.Label(root0,width=300,height=150)
one.pack()

IP0 = tkinter.StringVar()  
IP0.set('')
USER = tkinter.StringVar()
USER.set('')

labelIP = tkinter.Label(root0,text='IP地址',font=("楷体",10))
labelIP.place(x=20,y=20,width=100,height=40)
entryIP = tkinter.Entry(root0, width=60, textvariable=IP0)
entryIP.place(x=120,y=25,width=100,height=30)

labelUSER = tkinter.Label(root0,text='用户名',font=("楷体",10))
labelUSER.place(x=20,y=70,width=100,height=40)
entryUSER = tkinter.Entry(root0, width=60, textvariable=USER)
entryUSER.place(x=120,y=75,width=100,height=30)

def Login(*args):
	global IP, PORT, user
	IP, PORT = entryIP.get().split(':')
	user = entryUSER.get()
	if not user:
		tkinter.messagebox.showwarning('warning', message='用户名为空!')
	else:
		root0.destroy()

loginButton = tkinter.Button(root0, text ="登录", command = Login,bg="lightgreen",font=("楷体",10))
loginButton.place(x=135,y=120,width=40,height=25)
root0.bind('<Return>', Login)	#重新调出登录界面

root0.mainloop()

# 建立连接
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((IP, int(PORT)))
if user:
    s.send(user.encode())  # 发送用户名
else:
    s.send('用户名不存在'.encode())
    user = IP + ':' + PORT

# 聊天窗口
root1 = tkinter.Tk()
root1.geometry("640x480")
root1.title('jk的聊天室')
root1.resizable(0,0)

# 消息界面
listbox = ScrolledText(root1)
listbox.place(x=135, y=0, width=640, height=320)
listbox.tag_config('tag1', foreground='red',backgroun="white",font=('楷体', 12))
listbox.insert(tkinter.END, '欢迎进入jk的聊天室!', 'tag1')

INPUT = tkinter.StringVar()
INPUT.set('')
entryIuput = tkinter.Entry(root1, width=120, textvariable=INPUT)
entryIuput.place(x=135,y=320,width=580,height=170)

# 在线用户列表
listbox1 = tkinter.Listbox(root1,bg = "floralwhite")
listbox1.place(x=5, y=0, width=130, height=490)


def send(*args):
	message = entryIuput.get() + '~' + user + '~' + chat		#私聊功能:内容~发送者~接收者
	s.send(message.encode())
	INPUT.set('')

sendButton = tkinter.Button(root1, text ="发送",anchor = 'n',command = send,font=('楷体', 12),bg = 'Tan')
sendButton.place(x=570,y=440,width=55,height=30)
root1.bind('<Return>', send)

#接收消息
def receive():
	global uses
	while True:
		data = s.recv(1024)
		data = data.decode()
		print(data)

		#对接收到的消息进行判断，如果是在线用户列表，便清空在线用户列表框，并将此列表输出在在线用户列表中
		try:		
			uses = json.loads(data)
			listbox1.delete(0, tkinter.END)
			listbox1.insert(tkinter.END, "在线用户")
			listbox1.insert(tkinter.END, "--------------------------")
			for x in range(len(uses)):
				listbox1.insert(tkinter.END, uses[x])
			users.append('--------------------------')
		except:
			data = data.split('~')
			message = data[0]
			userName = data[1]
			chatwith = data[2]
			message = '\n' + message
			if chatwith == '--------------------------':   # 群聊
				if userName == user:
					listbox.insert(tkinter.END, message)
				else:
					listbox.insert(tkinter.END, message)
			elif userName == user or chatwith == user:  # 私聊
				if userName == user:
					listbox.tag_config('tag2', foreground='red')	#发送人显示信息为红色
					listbox.insert(tkinter.END, message, 'tag2')
				else:
					listbox.tag_config('tag3', foreground='green')	#接收人显示信息为绿色
					listbox.insert(tkinter.END, message,'tag3')

			listbox.see(tkinter.END)
r = threading.Thread(target=receive)
r.start()  # 开始线程接收信息

root1.mainloop()
s.close()
