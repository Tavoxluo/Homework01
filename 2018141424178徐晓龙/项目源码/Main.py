import os

from layout.LoginPanel import LoginPanel
from layout.MainPanel import MainPanel
from layout.RegisterPanel import RegisterPanel
from Client import ChatClient
from utils import MD5
from tkinter import messagebox, filedialog
from threading import Thread
import time

ALLOW_IMAGE_TYPE = [".jpg", ".jpeg", ".png", ".gif"]


def send_message():
    print("send message:")
    content = main_frame.get_send_text()
    if content == "" or content == "\n":
        print("空消息，拒绝发送")
        return
    print(content)
    # 清空输入框
    main_frame.clear_send_text()
    client.send_message(content)


def send_image():
    print("send image:")
    filepath = filedialog.askopenfilename()
    if filepath:
        print("文件路径: ", filepath)
        filetype: str = os.path.splitext(filepath)[-1].lower()
        filesize = os.path.getsize(filepath)
        if filesize > 1024 * 1024 * 5:
            messagebox.showinfo("提示", "图片过大，请选择小于5MB大小以下的图片!")

        if filetype in ALLOW_IMAGE_TYPE:
            print("被允许的文件类型")
            client.send_image(filepath)
        else:
            messagebox.showinfo("提示", "您选择的图片类型是不被允许使用的!")
    else:
        print("用户未选择图片")


def close_sk():
    print("尝试断开socket连接")
    client.sk.close()


def close_main_window():
    close_sk()
    main_frame.main_frame.destroy()


def close_login_window():
    close_sk()
    login_frame.login_frame.destroy()


# 关闭注册界面并打开登陆界面
def close_reg_window():
    reg_frame.close()
    global login_frame
    login_frame = LoginPanel(login, register, close_login_window)
    login_frame.show()


# 关闭登陆界面前往主界面
def goto_main_frame(user):
    login_frame.close()
    global main_frame
    main_frame = MainPanel(user, send_message, send_image, close_main_window)
    # 新开一个线程专门负责接收并处理数据
    Thread(target=recv_data).start()
    main_frame.show()


def login():
    print("点击登录按钮")
    user, key = login_frame.get_input()
    # 密码传md5
    key = MD5.gen_md5(key)
    if user == "" or key == "":
        messagebox.showwarning(title="提示", message="用户名或者密码为空")
        return
    print("user: " + user + ", key: " + key)
    if client.check_user(user, key):
        # 验证成功
        goto_main_frame(user)
    else:
        # 验证失败
        messagebox.showerror(title="错误", message="用户名或者密码错误")


# 登陆界面前往注册界面
def register():
    print("点击注册按钮")
    login_frame.close()
    global reg_frame
    reg_frame = RegisterPanel(close_reg_window, register_submit, close_reg_window)
    reg_frame.show()


# 提交注册表单
def register_submit():
    print("开始注册")
    user, key, confirm = reg_frame.get_input()
    if user == "" or key == "" or confirm == "":
        messagebox.showwarning("错误", "请完成注册表单")
        return
    if not key == confirm:
        messagebox.showwarning("错误", "两次密码输入不一致")
        return
    # 发送注册请求
    result = client.register_user(user, MD5.gen_md5(key))
    if result == "0":
        # 注册成功，跳往登陆界面
        messagebox.showinfo("成功", "注册成功")
        close_reg_window()
    elif result == "1":
        # 用户名重复
        messagebox.showerror("错误", "该用户名已被注册")
    elif result == "2":
        # 未知错误
        messagebox.showerror("错误", "发生未知错误")


# 处理消息接收的线程方法
def recv_data():
    # 暂停几秒，等主界面渲染完毕
    time.sleep(1)
    while True:
        try:
            # 首先获取数据类型
            _type = client.recv_all_string()
            print("recv type: " + _type)
            if _type == "#!onlinelist#!":
                print("获取在线列表数据")
                online_list = list()
                for n in range(client.recv_number()):
                    online_list.append(client.recv_all_string())
                main_frame.refresh_friends(online_list)
                print(online_list)
            elif _type == "#!message#!":
                print("获取新消息")
                user = client.recv_all_string()
                print("user: " + user)
                content = client.recv_all_string()
                print("message: " + content)
                main_frame.recv_message(user, content)
            # 获取显示图片
            elif _type == "#!image#!":
                print("获取新图片消息")
                user = client.recv_all_string()
                print("user: " + user)
                filename = client.recv_all_string()
                print("filename: " + filename)
                filepath = client.recv_file(filename)
                main_frame.recv_images(user, filepath)

        except Exception as e:
            print("接受服务器消息出错，消息接受子线程结束。" + str(e))
            break


def start():
    global client
    client = ChatClient()
    global login_frame
    login_frame = LoginPanel(login, register, close_login_window)
    login_frame.show()


if __name__ == "__main__":
    start()
