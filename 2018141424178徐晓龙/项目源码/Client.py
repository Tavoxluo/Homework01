
import os
import math
import socket

from config import IP, PORT


class ChatClient:

    def __init__(self):
        print("初始化tcp客户端")
        self.sk = socket.socket()
        self.sk.connect((IP, PORT))

    # 验证登录
    def check_user(self, user, key):
        # 请求类型
        self.sk.sendall(bytes("1", "utf-8"))
        # 依次发送用户名密码
        self.send_string_with_length(user)
        self.send_string_with_length(key)
        # 获取服务器的返回值，"1"代表通过，“0”代表不通过
        check_result = self.recv_string_by_length(1) == "1"
        if check_result:
            self.user = user
        return check_result

    # 注册
    def register_user(self, user, key):
        # 请求类型
        self.sk.sendall(bytes("2", "utf-8"))
        # 依次发送用户名密码
        self.send_string_with_length(user)
        self.send_string_with_length(key)
        # 获取服务器的返回值，"0"代表通过，“1”代表已有用户名, "2"代表其他错误
        return self.recv_string_by_length(1)

    # 发送消息
    def send_message(self, message):
        self.sk.sendall(bytes("3", "utf-8"))
        self.send_string_with_length(message)

    # 发送图片
    def send_image(self, filepath):
        self.sk.sendall(bytes("5", "utf-8"))

        (file_path, filename) = os.path.split(filepath)
        self.send_string_with_length(filename)
        self.send_file_with_length(filepath)

    ########################### 封装一些发送接受数据的方法 ##############################
    # 发送带长度的字符串
    def send_string_with_length(self, content):
        # 先发送内容的长度
        self.sk.sendall(bytes(content, encoding='utf-8').__len__().to_bytes(4, byteorder='big'))
        # 再发送内容
        self.sk.sendall(bytes(content, encoding='utf-8'))

    # 获取服务器传来的定长字符串
    def recv_string_by_length(self, len):
        return str(self.sk.recv(len), "utf-8")

    # 发送文件
    def send_file_with_length(self, filepath):
        filesize = os.path.getsize(filepath)  # 得到文件的大小,字节
        print("文件大小： ", filesize)
        # 先发送内容的长度
        self.sk.sendall(filesize.to_bytes(4, byteorder='big'))
        # 再发送内容
        with open(filepath, 'rb') as f:
            data = f.read()
            self.sk.sendall(data)

    # 获取文件
    def recv_file(self, filename):
        buff_size = 1024
        # 获取消息长度
        length = int.from_bytes(self.sk.recv(4), byteorder='big')
        print(f"读取文件: {filename}({length})")
        recv_len = 0
        file_dir = os.path.join("cache", self.user)
        if not os.path.isdir(file_dir):
            print("路径不存在，自动创建")
            os.makedirs(file_dir)
        filepath = os.path.join(file_dir, filename)
        with open(filepath, 'wb') as fp:
            while recv_len < length:
                # 判断未读取的大小是否大于默认读取大小，大于按默认读取，小于按剩余读取
                if length - recv_len > buff_size:
                    recv_tmp = self.sk.recv(buff_size)
                else:
                    recv_tmp = self.sk.recv(length - recv_len)

                recv_len += len(recv_tmp)
                fp.write(recv_tmp)
            print(filepath, recv_len, length)
            return filepath

    # 获取服务端传来的变长字符串，这种情况下服务器会先传一个长度值
    def recv_all_string(self):
        # 获取消息长度
        length = int.from_bytes(self.sk.recv(4), byteorder='big')
        b_size = 3 * 1024  # 注意utf8编码中汉字占3字节，英文占1字节
        times = math.ceil(length / b_size)
        content = ''
        for i in range(times):
            if i == times - 1:
                seg_b = self.sk.recv(length % b_size)
            else:
                seg_b = self.sk.recv(b_size)
            content += str(seg_b, encoding='utf-8')
        return content

    def send_number(self, number):
        self.sk.sendall(int(number).to_bytes(4, byteorder='big'))

    def recv_number(self):
        return int.from_bytes(self.sk.recv(4), byteorder='big')
