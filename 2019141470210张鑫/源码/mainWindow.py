import  threading
import  sys
import tkinter as tk
import tkinter.ttk as ttk
import tkinter.messagebox
from time import sleep


class Main:

    def __init__(self,s,user_id,recv_id):
        self.s = s

        self.root = tk.Tk()
        # 用户的id 显示在窗口标题上
        self.id = user_id
        # 0 代表在群聊中聊天,其他则代表与好友聊天
        self.recv_id = recv_id
        if self.recv_id == 0:
            # 群聊
            self.header = 'broad' + str(user_id)
            self.root.title('user_id:'+str(self.id)+'  临时在线聊天室')
        else:
            # 私聊
            self.header = 'sendt' + str(self.id) + str(self.recv_id)
            self.root.title('user_id:'+str(self.id)+'  recv_id:'+str(self.recv_id))

        self.root.geometry('800x600')
        self.root.attributes('-alpha',0.8)
        # self.root.configure(bg = 'black')
        self.root.protocol('WM_DELETE_WINDOW',self.sign_out)
        self.message_to_send = tk.StringVar()

        # 背景图
        image_file = tk.PhotoImage(file='./bg/bg1.gif')
        canvas = tk.Canvas(self.root, width=800, height=600)
        image = canvas.create_image(400, 300, image=image_file)
        canvas.grid(column=0, row=0,columnspan = 5,rowspan = 5,padx = 20,pady =20)

        self.frame_out = tk.Frame(self.root,
                              # bg ='grey',
                             height=400,
                                  # width=780
                                  ).grid(row=0, columnspan=2, padx=10, pady=20)
        self.frame_in_text = tk.Frame(self.root,
                                      # bg='grey',
                                      height=150,
                                      # width=600
                                      ).grid(row=1, column=0, ipadx=0, padx=10,
                                                                  columnspan=1, sticky='w')
        self.frame_in_button = tk.Frame(self.root,
                                        # bg='grey',
                                        height=150,
                                        # width=150
                                        ).grid(row=1, column=1, ipadx=0, padx=10,
                                                                    columnspan=1, sticky='w')
        self.frame_out_text = tk.Frame(self.frame_out,
                                   bg='green',
                                  height=400,
                                       # width=600
                                       ).grid(row=0, column=0, padx=10, pady=10,
                                                              sticky='w')
        self.frame_out_friend = tk.Frame(self.frame_out,
                                     # bg ='grey',
                                    height=400,
                                         # width=150
                                         ).grid(row=0, column=1, padx=10, pady=10, sticky='e')
        # frame_in = tk.Frame(window,bg = 'red',height = 150,width = 800).grid(row = 1,pady =20,sticky = 'w')

        # show = tk.Text(frame_out_text,height =25,width =85).grid(row =0,column =0,padx =10,pady = 10,sticky ='w')
        self.edit = ttk.Combobox(self.frame_in_text, textvariable=self.message_to_send, width=80,value = ('你好','再见'))
        self.edit.bind('<Return>',self.press_enter)
        self.edit.grid(row=1, column=0)
        self.show_list = tk.Listbox(self.frame_out_text, height=20, width=85)
        self.show_list.insert('end', '聊天记录')
        self.show_list.itemconfig(0,{'bg':'yellow'})
        self.show_list.bind('<Double-Button-3>',self.history_del)
        self.show_list.grid(row=0, column=0, padx=20, pady=10, sticky='w')
        self.button_send = ttk.Button(self.frame_in_button, command=self.send_message, text='SEND').grid(row=1, column=1,sticky = 'w')

        # 好友列表区域,实现点击一个按钮之后可以开启一个新的窗口，与好友聊天
        self.friends_list = tk.Listbox(self.frame_out_friend,height = 20,width = 18)
        self.friends_list.bind('<Double-Button-1>', self.new_page)
        # self.friends_list.bind('<Button-2>',self.friend_control)
        self.friends_list.bind('<Double-Button-3>',self.friend_del)
        self.friends_list.insert('end','好友列表')
        self.friends_list.grid(row = 0,column = 1,padx = 15,pady =10, sticky = 'w',columnspan = 2)

        # 顶部菜单栏
        self.menu = tk.Menu(self.root)
        self.menu_friend = tk.Menu(self.menu,tearoff = 0)
        self.menu_friend.add_cascade(label = 'DELETE FRIEND',command = self.friend_del)
        self.menu_friend.add_cascade(label = 'ADD FRIEND',command = self.friend_add)
        self.menu.add_cascade(label = 'FRIEND',menu = self.menu_friend)

        self.menu_history =  tk.Menu(self.menu,tearoff = 0)
        self.menu_history.add_cascade(label = 'DELETE HISTORY',command = self.history_del)
        self.menu_history.add_cascade(label = 'CHECK HISTORY',command = self.check_history)
        self.menu.add_cascade(label = 'HISTORY',menu = self.menu_history)

        self.menu_me = tk.Menu(self.menu,tearoff = 0)
        self.menu.add_cascade(label = 'ME',menu = self.menu_me)
        self.menu_me.add_cascade(label = 'SIGN OUT',command = self.sign_out )
        self.menu_me.add_cascade(label = 'CHANGE NAME',command = self.name_change)
        self.menu_me.add_cascade(label = 'CHANGE PASSWORD',command = self.password_change)

        self.menu_show = tk.Menu(self.menu,tearoff = 0)
        self.menu.add_cascade(label = 'SHOW',menu = self.menu_show)
        self.menu_show.add_cascade(label = 'SHOW FRIENDS',command = self.show_friends)
        self.menu_show.add_cascade(label = 'SHOW ONLINE',command =self.show_online)

        self.root.config(menu = self.menu)




        # 添加好友的搜索框
        self.friend_add_id = tk.StringVar()
        self.friend_add_entry = ttk.Entry(self.frame_out_friend,textvariable = self.friend_add_id).grid(column = 1,row =0,sticky ='n')

        # 按钮用来刷新好友列表
        # self.button_flush = ttk.Button(self.frame_in_button,command = self.show_friends ,text ='FLUSH').grid(row =1,column = 1,padx =50,sticky = 'w',columnspan = 1)

        # 刷新列表
        self.show_online()
        # 多线程进行
        thread_show = threading.Thread(target=self.show_message)
        thread_show.setDaemon(True)
        thread_show.start()
        self.root.mainloop()


    # 显示聊天室的人
    def show_online(self):
        msg = 'shonl'
        self.s.send(msg.encode())

    # 鼠标双击好友弹出新的窗口与好友聊天
    def new_page(self,event):
        curr = self.friends_list.curselection()
        text = self.friends_list.get(curr)
        index = self.friends_list.index(curr)
        self.friends_list.itemconfig(index,{'bg':'white'})
        if text[0] == '0':
            self.recv_id = '0'
            self.header = 'broad'+str(self.id)
            self.root.title('user_id:'+str(self.id)+' 临时聊天室')
            self.show_online()
        if text == '当前在线(点击返回好友列表)':
            self.show_friends()
        else:
            self.recv_id = text[0:5]
            self.header = 'sendt'+str(self.id)+str(self.recv_id)
            self.root.title('user_id:' + str(self.id) + '  recv_id:' + text)
            self.check_history()

    # # 鼠标中键点击进行添加和删除好友 已废
    # def friend_control(self,event):
    #     print('friend_control')
    #
    #     from pages import friend
    #     friend.Friend(user_id = self.id)
    #
    # 鼠标右键点击删除好友
    def friend_del(self,event = ''):
        flag = tkinter.messagebox.askyesno(title='删除好友', message='您确定要删除该好友吗？删除后不可恢复')
        if flag == True:
            try:
                print('delete friend')
                curr = self.friends_list.curselection()
                text = self.friends_list.get(curr)
                friend_id = text[0:5]
                msg = 'delfr'+str(self.id)+str(friend_id)
                self.s.send(msg.encode())
                self.show_friends()
            except:
                tkinter.messagebox.showwarning(title='ERROR', message='输入格式不正确！！')


    # 下线
    def sign_out(self):
        flag = tkinter.messagebox.askyesno(title='退出登录', message='您确定要退出登录吗?')
        if flag == True:
            print('sign out')
            msg = 'signo'+str(self.id)
            self.s.send(msg.encode())
            # 等待服务器端发送完消息,参考TCP的四次挥手
            sleep(0.1)
            self.s.close()
            sys.exit()



    # 更改名字
    def name_change(self):
        try:
            print('change name')
            new_name = self.friend_add_id.get()[0:5]
            if new_name =='':
                # self.show_list.insert('end','请在输入框中输入新名字(最大长度5)，再点击change name')
                tkinter.messagebox.showwarning(title='ERROR', message='请在输入框中输入新名字(最大长度5)，再点击change name')
                return
            msg = 'chana'+self.id+new_name
            self.s.send(msg.encode())
        except:
            tkinter.messagebox.showwarning(title = 'ERROR',message='未知错误！')

    # 更改密码
    def password_change(self):
        print('change password')
        new_password = self.friend_add_id.get()
        if new_password == '':
            # self.show_list.insert('end','请先再输入框中输入新密码，再点击change password')
            tkinter.messagebox.showwarning(title='ERROR', message='请先再输入框中输入新密码，再点击change password！')
            return
        msg = 'chapa'+self.id+new_password
        self.s.send(msg.encode())

    # 删除历聊天记录
    def history_del(self,event = ''):
        flag = tkinter.messagebox.askyesno(title='删除好友', message='您确定要删除该记录吗？'
                                                                 '删除后不可恢复')
        if flag == True:
            if self.recv_id == 0:
                # self.show_list.insert('end','请先选定一个好友再进行操作')
                tkinter.messagebox.showwarning(title='ERROR', message='请先选定一个好友再进行操作！')
                return
            curr = self.show_list.curselection()
            text = self.show_list.get(curr)
            txt = text.split()
            name = txt[2][0:len(txt[2])-1]
            if  len(name)<5:
                n = 5 - len(name)
                for i in range(0,n):
                    name = name + ' '
            print(len(name))
            msg = 'delhs'+name+txt[0]+' '+txt[1]
            self.s.send(msg.encode())
            from time import sleep
            sleep(0.1)
            self.check_history()


    # 添加好友
    def friend_add(self):
        print('add friend')
        id = self.friend_add_id.get()
        msg = 'addfr'+self.id+str(id)
        self.s.send(msg.encode())


    # 查看历史记录
    def check_history(self):
        # 清空
        self.show_list.delete(0,tk.END)
        id = self.recv_id
        print(id)
        if id == 0:
            # self.show_list.insert('end','错误！您需要先选择一个好友再查看聊天记录')
            tkinter.messagebox.showwarning(title='ERROR', message='错误！您需要先选择一个好友再查看聊天记录！')
            return
        msg = 'chehs'+str(id)
        self.s.send(msg.encode())

    # 显示主机发来的消息
    def show_message(self):
        print('start showing message!')
        while True:
            meg = self.s.recv(1024).decode()
            header = meg[0:5]
            meg = meg[5:]
            print(header,meg)
            # 如果这个消息是别人发给的就显示在历史记录上
            if header == 'sendt':
                self.show_list.grid_remove()

                self.show_list.insert(tk.END, meg)
                self.show_list.grid(row=0, column=0, padx=10, pady=10, sticky='w')
                print('insert', meg)
            # 如果这个消息是用来更新好友列表的
            if header == 'frien':
                self.friends_list.grid_remove()
                self.friends_list.insert(tk.END,meg)
                self.friends_list.grid(row = 0,column = 1,padx = 15,pady =10, sticky = 'w')
                print('show friends list')
            # 这个消息用来通知主机端有新消息，把相应的好友列表的人标上颜色
            if header == 'highl':
                sender_id = meg
                index = 0
                for i in range(0,self.friends_list.size()):
                    text = self.friends_list.get(i)[0:5]
                    if text == sender_id:
                        index = i
                self.friends_list.itemconfig(index,{'bg':'red'})
                # 如果是搜索好友结果没有这个id,那么警告
            if header == 'adder':
                tkinter.messagebox.showwarning(title='ERROR', message='未查到相关id,请重新检查！')
                print('add friend failed, no such id!')

            # 头部为 shonl 则刷 好友列表显示 在线人
            if header == 'shonl':
                self.friends_list.delete(0,tk.END)
                self.friends_list.grid_remove()
                self.friends_list.insert(tk.END,'当前在线(点击返回好友列表)')
                while meg !='':
                    self.friends_list.insert(tk.END,meg[0:10])
                    meg = meg[10:]
                self.friends_list.grid(row = 0,column = 1,padx = 15,pady =10, sticky = 'w')


    # 发送信息给主机
    def send_message(self):
        mes = self.header + self.message_to_send.get()
        self.s.send((mes).encode())
        self.message_to_send.set('')
        print('send',mes)

    # 输入框按回车后发送消息
    def press_enter(self,event):
        self.send_message()



    # 显示好友列表
    def show_friends(self):
        # 删除表重所有元素
        self.friends_list.delete(0,tk.END)
        self.show_list.delete(0,tk.END)
        self.friends_list.insert(tk.END, '0 临时聊天室')
        msg = 'shofr'+str(self.id)
        self.s.send(msg.encode())



