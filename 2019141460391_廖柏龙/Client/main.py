from tkinter import *
from LoginPage import *

if __name__=="__main__":
    root = Tk()
    root.title('聊天登陆')
    #进入登录界面
    LoginPage(root)

    # 事件循环，一旦产生事件，就会刷新组件
    root.mainloop()
