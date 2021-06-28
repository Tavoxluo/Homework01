from socket import *
import re


def handle_client(client_socket):
    """为一个客户端服务"""
    # 接收对方发送的数据
    recv_data = client_socket.recv(1024).decode("utf-8")  # 1024表示本次接收的最大字节数
    # 打印从客户端发送过来的数据内容
    # print("client_recv:",recv_data)
    request_header_lines = recv_data.splitlines()
    for line in request_header_lines:
        print(line)

    # 返回浏览器数据
    # 设置内容body
    # 使用正则匹配出文件路径
    print("------>", request_header_lines[0])
    print("file_path---->", "./html/" + re.match(r"[^/]+/([^\s]*)", request_header_lines[0]).group(1))
    ret = re.match(r"[^/]+/([^\s]*)", request_header_lines[0])
    if ret:
        file_path = "./html/" + ret.group(1)
        if file_path == "./html/":
            file_path = "./html/index.html"
        print("file_path *******", file_path)

    try:
        # 设置返回的头信息 header
        response_headers = "HTTP/1.1 200 OK\r\n"  # 200 表示找到这个资源
        response_headers += "\r\n"  # 空一行与body隔开
        # 读取html文件内容
        file_name = file_path  # 设置读取的文件路径
        f = open(file_name, "rb")  # 以二进制读取文件内容
        response_body = f.read()
        f.close()
        # 返回数据给浏览器
        client_socket.send(response_headers.encode("utf-8"))  # 转码utf-8并send数据到浏览器
        client_socket.send(response_body)  # 转码utf-8并send数据到浏览器
    except:
        # 如果没有找到文件，那么就打印404 not found
        # 设置返回的头信息 header
        response_headers = "HTTP/1.1 404 not found\r\n"  # 200 表示找到这个资源
        response_headers += "\r\n"  # 空一行与body隔开
        response_body = "<h1>sorry,file not found</h1>"
        response = response_headers + response_body
        client_socket.send(response.encode("utf-8"))

    client_socket.close()


def main():
    # 创建套接字
    server_socket = socket(AF_INET, SOCK_STREAM)
    # 设置当服务器先close 即服务器端4次挥手之后资源能够立即释放，这样就保证了，下次运行程序时 可以立即绑定7788端口
    server_socket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
    # 设置服务端提供服务的端口号
    server_socket.bind(('', 7788))
    # 使用socket创建的套接字默认的属性是主动的，使用listen将其改为被动，用来监听连接
    server_socket.listen(128)  # 最多可以监听128个连接
    # 开启while循环处理访问过来的请求
    while True:
        # 如果有新的客户端来链接服务端，那么就产生一个新的套接字专门为这个客户端服务
        # client_socket用来为这个客户端服务
        # server_socket就可以省下来专门等待其他新的客户端连接while True:
        client_socket, clientAddr = server_socket.accept()
        handle_client(client_socket)


if __name__ == "__main__":
    main()
