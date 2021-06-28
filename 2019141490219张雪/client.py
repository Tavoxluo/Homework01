import socket

def send_request(sendData):
   # 1. 创建套接字
   tcp_client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
   # 2. 连接本地服务器8089端口
   tcp_client_socket.connect(("127.0.0.1", 8089))
   # 3. 发送数据
   send_data = sendData
   tcp_client_socket.send(send_data.encode("utf-8"))
   data = tcp_client_socket.recv(1024)
   data = bytes.decode(data) #因为接受到的数据是字节码，需要转换为字符串
   tcp_client_socket.close()
   print('Received', repr(data))

def main():
   while 1:  #当输入不为exit时发送给服务器机器人，否则退出。
      i = input("<<<").strip()
      if i != 'exit':
         send_request(i)
      else:
         break

if __name__ == '__main__':
   main()