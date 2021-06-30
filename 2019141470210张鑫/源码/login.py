import tkinter as tk
import tkinter.ttk as ttk
from time import sleep
import mainWindow
import socket
import sys


class LoginPage:
    # 默认的地址和端口号
    host = '127.0.0.1'
    port = 7777
    def __init__(self):

        self.root = tk.Tk()
        self.root.title('login')
        self.account_get = tk.StringVar()
        self.password_get = tk.StringVar()
        self.host_get = tk.StringVar()
        self.port_get = tk.StringVar()
        self.text = tk.StringVar()
        self.name = tk.StringVar()
        self.text.set('system:')

        # 顶部菜单
        menu = tk.Menu(self.root)
        menu.add_cascade(label = 'SHOW MORE',command =self.show_more)
        self.root.config(menu = menu,bg = 'mediumaquamarine')
    # 标指量 用来控制 show more 行为
        self.active = False


        self.canvas = tk.Canvas(self.root,width = 300,height = 170,bg = 'green')

        image_file = tk.PhotoImage(file = '.\\bg\\bg3.gif')
        image = self.canvas.create_image(150,0,anchor = 'n',image = image_file)
        self.canvas.grid(column = 0,row = 0,columnspan = 5,rowspan = 5,padx = 0,pady = 0)
        icon_password = tk.PhotoImage(file = '.\icon\icon_pass.gif')
        icon_account = tk.PhotoImage(file = '.\icon\icon_account.gif')

        self.host_label = ttk.Label(self.root,text = 'host')
        self.port_label = ttk.Label(self.root,text = 'port')
        # 读入地址的设置选项
        self.host_values = self.be_tupe(self.read_from('./config/setting.txt'))
        self.host_text = ttk.Combobox(self.root,textvariable = self.host_get,value = self.host_values)
        # 读入port的设置选项
        self.port_values = self.be_tupe(self.read_from('./config/port.txt'))
        self.port_text = ttk.Combobox(self.root,textvariable = self.port_get,value = self.port_values )
        self.account_label = ttk.Label(self.root, text='account',image = icon_account,).grid(column=1, row=1,columnspan = 1)
        self.password_labe = ttk.Label(self.root, text='password',image = icon_password,).grid(column=1, row=2,columnspan = 1)
        # 读入account的设置选项
        self.account_values = self.be_tupe(self.read_from('./config/account.txt'))
        self.account = ttk.Combobox(self.root, textvariable=self.account_get,value = self.account_values).grid(column = 2, row = 1)

        # 默认不可见密码
        self.password = tk.Entry(self.root, textvariable=self.password_get,show = '*').grid(column = 2,row = 2)

        self.button = ttk.Button(self.root, text='login', command=self.login).grid(column = 1,row = 3,columnspan = 1)
        self.button = ttk.Button(self.root, text = 'register',command = self.register).grid(column = 2,row = 3,columnspan = 1 )
        self.text_recv = ttk.Label(self.root,textvariable = self.text).grid(column = 3,row = 3,columnspan =2,rowspan =2)
        self.name_labe = ttk.Label(self.root,text = 'name')
        self.name = ttk.Entry(self.root,textvariable = self.name )


        self.root.mainloop()

    # 把一个字符串变成元组
    def be_tupe(self,text:str):
        txt = text.split()
        tup =()
        for t in txt:
            tup+=(t,)
        return tup

    # 顶部菜单函数，显示更多的输入框
    def show_more(self):
        if not self.active:
            self.port_text.grid(column = 1,row =0,columnspan = 1)
            self.port_label.grid(column = 3,row =0,columnspan = 1)
            self.host_text.grid(column = 2,row =0,columnspan = 1)
            self.host_label.grid(column = 1,row = 0)
            self.port_text.grid(column = 4,row = 0,columnspan = 1)
            self.name_labe.grid(column = 3,row = 1,columnspan = 1)
            self.name.grid(column = 4,row =1)
            self.active = True
        else:
            self.port_text.grid_remove()
            self.port_label.grid_remove()
            self.host_text.grid_remove()
            self.port_text.grid_remove()
            self.name_labe.grid_remove()
            self.name.grid_remove()
            self.host_label.grid_remove()
            self.active = False

# 从配置文件中读入
    def read_from(self,filename):
        f = open(filename)
        read_data = f.read()
        values = read_data
        f.close()
        return values

# 向文件写入
    def write_to(self,filename,text):
        f = open(filename,'a')
        f.writelines('\n'+text)



    # 与目标主机建立连接
    def build(self):
        try:
            if self.host_get.get() != '':
                print('get host:',self.host_get.get())
                self.host = self.host_get.get()
            if self.port_get.get() != '':
                self.port = int(self.port_get.get())
            self.s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
            print(self.host, self.port)
            print(self.port)
            self.s.connect((self.host,self.port))
            print('build the connection successfully!')
            # 存入数据
            if not  self.port_get.get() in self.port_values:
                self.write_to('./config/port.txt',self.port_get.get())
            if not self.host_get.get() in self.host_values:
                self.write_to('./config/setting.txt',self.host_get.get())
        except:
            print('build the connection failed!')

    # login 按钮的控制函数
    def login(self):

        self.build()

        if self.check(self.account_get.get(),self.password_get.get()):
            # 销毁当前页面，并创建一个新的页面
            self.root.destroy()
            # 存入账户方便下次登录
            if  not self.account_get.get() in self.account_values:
                self.write_to('./config/account.txt',self.account_get.get())
            mainWindow.Main(self.s, self.account_get.get(), 0)

    # 检测帐号与密码是否则正确的
    def check(self,account,password):
        msg ='login'+str(account)+str(password)

        if self.send_recv(msg) == 'sendt~login successfully!':
            return True
        else:
            return False

    def send_recv(self,msg):
            self.s .send(msg.encode())
            sleep(0.1)
            text = self.s.recv(1024).decode()
            self.text.set(text)
            return text

    def register(self):
        self.build()
        name = self.name.get()[0:5]
        if len(name) < 5:
            n = 5 - len(self.name.get())
            for i in range(0,n):
                name += ' '
        print(name, len(name))
        msg = 'regis'+name+self.password_get.get()
        anw = self.send_recv(msg)


if __name__ == '__main__':
    try:
        l = LoginPage()
    except:
        print('用户点击 x 关闭！')
        sys.exit()

