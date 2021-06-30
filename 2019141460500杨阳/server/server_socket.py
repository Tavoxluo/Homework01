import socket
from config import *

class ServerSocket(socket.socket):


    def __init__(self):
        # 设置TCP类型
        super(ServerSocket, self).__init__(socket.AF_INET, socket.SOCK_STREAM)

        # 绑定地址和端口
        self.bind((SERVER_IP, SERVER_PORT))

        # 设置为监听模式
        self.listen(128)
