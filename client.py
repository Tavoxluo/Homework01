import time
from socket import *
import tkinter as tk
#import asyncio
from threading import Thread
import configparser
import os

# 读取ini配置数据
curpath = os.path.dirname(os.path.realpath(__file__))
cfgpath = os.path.join(curpath, 'data.ini')
print(cfgpath)

conf = configparser.ConfigParser()
conf.read(cfgpath,encoding="utf-8")
sections = conf.sections()
print(sections)
items = conf.items('server_ini')
print(items)

serverIP = items[0][1]
print(serverIP)
serverPort = int(items[1][1])
print(serverPort)


# 创建socket
#serverPort = 666
clientSocket = socket(AF_INET, SOCK_STREAM)
clientSocket.connect((serverIP,serverPort))

# 初始-选择界面
def main():
    win = tk.Tk()
    win.title("Client")
    win.geometry("500x400")

    def chat_broad():
        win.destroy()
        main_broad()
    def chat_one():
        win.destroy()
        main_list()

    b_broad = tk.Button(win, text="进入群聊界面", width=15, height=1, command=chat_broad)
    b_broad.pack()

    b_one = tk.Button(win, text="进入私聊界面", width=15, height=1, command=chat_one)
    b_one.pack()

    win.mainloop()

# 创建群聊的客户端界面
def display_broad():
    global window_broad
    global entry_broad
    global text_broad
    global b_submit_broad

    window_broad = tk.Tk()
    window_broad.title("Client")
    window_broad.geometry("500x400")

    text_broad = tk.Text(window_broad, height=20)
    text_broad.pack()

    entry_broad = tk.Entry(window_broad)
    entry_broad.pack()

    b_submit_broad = tk.Button(window_broad, text="发送", width=5, height=1, command=send_broad)
    b_submit_broad.pack()

    def broad_return():
        window_broad.destroy()
        #stop_thread(thread_send_b)
        #stop_thread(thread_read_b)
        main()

    b_return_broad = tk.Button(window_broad, text="返回", width=5, height=1, command=broad_return)
    b_return_broad.pack() #各个模块均设置有返回键，方便彼此之间的切换（另外经测试，各种交叉切换过后的各个模块仍能正常运行和显示）

    window_broad.mainloop()

# 实现异步法一：双线程（成功）
def send_broad():
    #window.mainloop()
    sentence = entry_broad.get()
    #sentence = input("聊天：")
    clientSocket.send((sentence+"broad_pattern").encode()) #将讯息的末尾十三个字符作为其标识符：broad_pattern作为广播讯息转发，toone_pattern作为私聊讯息转发
    print("send success")
    entry_broad.delete(0, tk.END) # 要注意清空输入框的内容，否则会陷入死循环

# 程序分为三个模块，即群聊模块、选择私聊对象模块和私聊模块，原本为每个模块都写了各自的信息接收进程，但之后发现了一个问题：
# python中的thread线程是无法中止或暂停的，因此当从一个模块切换至另一个模块时，前一个模块的信息接收线程等仍存活着
# 为了避免讯息接收发生混乱，我在三个模块中分别设置了三种信息标识符，并对服务器做了对应的修改，甚至尝试当不符合条件的接收线程在接收到信息时time.sleep几秒、在前一个线程的基础上调用后一个线程、或是使用thread实例的join()函数对前一个线程进行堵塞
# 但上述举措都无法解决一个不易被察觉的问题（由多线程异步IO导致的）：即当客户端同时有两个以上的接收（socket.recv()）线程存在时，服务器端传回的讯息只会被最早创建的那个接收线程接收到，其他线程无论如何都无法接收（即便最早的那个线程已被暂停或尚未执行至其中的recv步，服务器也会持续等待这个线程接收而不是其他的，像是进入了一种堵塞状态）
# 对此在网上也并没有找到很好的解决方法，因此我最终决定将三个模块的接收线程合并为一（即下面这个read函数），由此客户端讯息接收的步骤或逻辑是：
# - 每次向服务器发送讯息时，都附加上该讯息所属模块的标识符，服务器根据这个标识符判断应该执行哪一部分的代码；而在服务器端，每次向客户端返回数据时，同样会附带其所属模块的标识符；同时整个read函数被分为三部分（根据功能的扩展还可以分出更多），通过数据的标识符判断应该由哪个模块来接收这个讯息。
# - 简而言之，整个客户端的各线程共享的是同一个接收进程，这一函数承载了客户端讯息的识别和接收工作（因为函数中实际上包含了3个socket.recv函数，但通过if语句和讯息标识符区别和并行开来，这样前面的问题就得到了很好的解决
# （ps. 不想彻底杀死线程，主要是考虑到各模块之间的切换可能会很频繁，有些模块之间还存在较大关联-比如选择私聊对象和私聊。另外参考error信息，python中一个thread好像只能被唤醒一次，重新创建同名线程的代价好像比较大）
def read():
    while True:
        #window.mainloop()
        print("start read")
        response_type = clientSocket.recv(1024).decode()
        print(response_type)
        if response_type == "response_to_broad":
            response = clientSocket.recv(1024).decode()
            print("read success")
            #if response:  # 同理，只有在接收到有效内容时才更新聊天区
            #print(response)
            text_broad.insert('end', response + "\n")
            response = "" # 同理，要清空
        if response_type == "response_as_list":
            #time.sleep(1)
            # 另外掌握了一个python语言的一个语法知识点，即定义的函数内部对函数外全局变量的赋值和引用操作是无效的（默认只是和全局变量重名的函数内局部变量）
            # 因此，想要在函数体内部对函数外全局变量的值进行修改，必须在函数体内以global特殊字符按相同的变量名进行二次定义，这样在函数内部对全局变量值的修改才会定向至对应的函数外全局变量并被保存下来
            global cur_clients
            cur_clients = clientSocket.recv(1024).decode().split("^^")
            # 标识出本机
            count = 0
            while count<len(cur_clients):
                if cur_clients[count]==str(clientSocket.getsockname()):
                    cur_clients[count]+="(本机，请勿私聊)"
                    break
                count+=1
            print("后端已接收到：",cur_clients)
            print("客户端列表已接收")
        if response_type == "response_to_one":
            # window.mainloop()
            print("start read")
            response = clientSocket.recv(1024).decode()
            print("read success")
            # if response:  # 同理，只有在接收到有效内容时才更新聊天区
            # print(response)
            text_toone.insert('end', response + "\n")
            response = ""  # 同理，要清空

def main_broad():
    try:
        #display()
        thread_send_b = Thread(target=send_broad, args=())

        display_broad()
        #display_start()
        while True:
            thread_send_b.start()

    except ConnectionResetError:
        pass


# 创建通讯录界面
def display_choose_client():
    global window_choose
    global listc

    window_choose = tk.Tk()
    window_choose.title("Client")
    window_choose.geometry("500x400")

    label = tk.Label(window_choose,text="所有在线用户列表",bg="grey",width=30,height=2)
    label.pack()

    listc = tk.Listbox(window_choose,width=400)
    listc.pack()
    print("前端已接收到：", cur_clients)
    for client in cur_clients:
        listc.insert(listc.size(), client)

    #实现了简单的通讯录内搜索的功能
    entry_choose = tk.Entry(window_choose)
    entry_choose.pack()

    def search_client():
        keywords = entry_choose.get()
        entry_choose.delete(0,len(keywords))
        print(keywords)
        listc.delete(0,len(client_list))
        for client in client_list:
            if keywords==client:
                listc.insert(listc.size(), client)

    b_search = tk.Button(window_choose, text="搜索", width=5, height=1, command=search_client)
    b_search.pack()

    # 双击某个用户进入与该用户的私聊聊天室
    def toone_chat(event):
        main_toone(listc.get(listc.curselection()))
        window_choose.destroy()
    listc.bind('<Double-Button-1>', toone_chat)

    def list_return():
        window_choose.destroy()
        main()

    b_return_broad = tk.Button(window_choose, text="返回", width=5, height=1, command=list_return)
    b_return_broad.pack()

    window_choose.mainloop()

def main_list():
    try:
        clientSocket.send("toone_pattern".encode())
        print("私聊模式标识符发送完毕")
        time.sleep(1) #加入1秒延迟，使得数据列表的更新先进行，界面的生成后进行，否则更新后的用户列表数据无法正常显示
        display_choose_client()
    except ConnectionResetError:
        pass

# 创建私聊的客户端界面
def display_toone():
    global window_toone
    global entry_toone
    global text_toone
    global b_submit_toone

    window_toone = tk.Tk()
    window_toone.title("Client")
    window_toone.geometry("500x400")

    text_toone = tk.Text(window_toone, height=20)
    text_toone.pack()

    entry_toone = tk.Entry(window_toone)
    entry_toone.pack()

    b_submit_toone = tk.Button(window_toone, text="发送", width=5, height=1, command=send_toone)
    b_submit_toone.pack()

    def toone_return():
        window_toone.destroy()
        main()

    b_return_toone = tk.Button(window_toone, text="返回", width=5, height=1, command=toone_return)
    b_return_toone.pack()

    window_toone.mainloop()

def send_toone():
    sentence = entry_toone.get()
    clientSocket.send(
        (sentence + "xchat_pattern").encode())
    clientSocket.send(str(current_client).encode())
    print("send success")
    entry_toone.delete(0, tk.END)

def main_toone(cur_client):
    try:
        global current_client
        current_client = cur_client
        print("当前对话用户："+cur_client)
        thread_send = Thread(target=send_toone, args=())
        #thread_read = Thread(target=read_toone, args=())

        #thread_read.start()
        display_toone()
        thread_send.start()
    except ConnectionResetError:
        pass

thread_read = Thread(target=read, args=()) #为了避免信息接收产生干扰性的延迟，信息接收线程的创建及初始化应在主程序运行之前完成
thread_read.start()
cur_clients = []

main()