import socket
import threading
from chatterbot import ChatBot
#创建机器人
bot = ChatBot(
    'Bob',
    storage_adapter='chatterbot.storage.MongoDatabaseAdapter'
)
#定义机器人的返回函数
def r(s):return bot.get_response(s).text
# 多线程服务器
def handle_conn(sock, address):
    print("deal with connection ....")
    t = threading.Thread(target=process_conn, args=(sock, address))
    t.start()


def process_conn(sock, address):
    print(threading.current_thread())

    while True:  # 多次为一个客户端服务
        recv_data = sock.recv(1024)
        recv_data = bytes.decode(recv_data)#因为收到的数据为字节码，需要转为字符串传递给机器人
        print(recv_data)
        if recv_data:
            sock.send(r(recv_data).encode("utf-8"))
        else:
            break
    # 5. close socket
    print("close socket..")
    sock.close()


def main():
    # 1. 创建套接字
    tcp_server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # 2. 绑定本地地址和8089端口
    tcp_server_socket.bind(("127.0.0.1", 8089))
    # 3.开启监听
    tcp_server_socket.listen()

    while True:
        print(threading.current_thread())
        print("waitting ........")
        new_client_socket, client_addr = tcp_server_socket.accept()
        handle_conn(new_client_socket, client_addr)

if __name__ == '__main__':
    main()