import socket
from config import *

class ClientSocket(socket.socket):

    def __init__(self):
        # 设置TCP类型
        super(ClientSocket, self).__init__(socket.AF_INET, socket.SOCK_STREAM)
        super(ClientSocket, self).connect((SERVER_IP, SERVER_PORT))

    def recv_data(self):
        # 接受数据并返回
        return self.recv(20000).decode('utf-8')

    def send_data(self, message):

        return self.send(message.encode('utf-8'))