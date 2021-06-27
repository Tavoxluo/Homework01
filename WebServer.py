import socket
import re
import threading
import dynamic.toy_frame
import sys


class WebServer:
    def __init__(self, port):
        # http是基于tcp协议之上的，故先要建立tcp连接
        self.tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # tcp绑定本地ip和端口
        self.tcp_socket.bind(('', port))
        # 监听套接字转为被动接受状态
        self.tcp_socket.listen(128)

    def run(self):
        # 持续等待连接
        while True:
            # 监听套接字等待连接
            connection_socket, client_addr = self.tcp_socket.accept()
            # 创建线程来处理一个客户端的请求
            t1 = threading.Thread(target=self.serve_client, args=(connection_socket,))
            t1.start()
            # p1 = multiprocessing.Process(target=self.serve_client, args=(connection_socket,))
            # p1.start()
            # print(t1)
        # 关闭监听套接字
        tcp_socket.close()

    def deal_dynamic(self, file_name, connection_socket):
        # 以.html结尾就被认为是动态资源的请求
        # env作为参数传给框架内的application函数
        env = dict()
        env['PATH_INFO'] = file_name
        # 调用框架内的application函数返回body
        # 这里body就是encoding出来的字符
        body = dynamic.toy_frame.application(env, self.set_response_header)

        # header在框架内已经被调用，在服务器中再表示出来
        header = "HTTP/1.1 %s\r\n" % self.status
        # "200 OK", [('Content-Type', 'text/html;charset=GBK')]
        for head in self.headers:
            header += "%s:%s\r\n" % (head[0], head[1])
        # header += "Transfer-Encoding: chunked\r\n"

        # header和body之间有一个空行
        header += "\r\n"
        # 将header和body拼接
        response = header + body
        # 发送数据
        connection_socket.send(response.encode("utf-8"))

    def deal_static(self, file_name, connection_socket):
        try:
            f = open("./static" + file_name, "rb")
        except:
            response_body = "请求页面不存在".encode("GBK")
            response = "HTTP/1.1 404 NOT FOUND\r\n"
            # 设置content-length字段可以使得由浏览器断开连接
            # 404显示的内容也要用二进制发过去，否则中文会乱码，因为len计算的一个汉字长度为1
            response += "Content-Length:%d\r\n" % len(response_body)
            # response += 'Content-Type: text/plain;charset=utf8\r\n'
            response += "\r\n"
            # 加上body字段
            # response += response_body
            connection_socket.send(response.encode("GBK"))
            connection_socket.send(response_body)
        else:
            # 回应请求 浏览器请求回应里面回成用\r\n表示
            response = "HTTP/1.1 200 OK\r\n"
            # 读出服务器上存储的静态资源内容
            html_content = f.read()
            response += "Content-Length:%d\r\n" % len(html_content)
            # response += 'Content-Type: text/html\r\n'
            # response += "Transfer-Encoding: gzip, chunked\r\n"
            # response += "Keep-Alive: max=5, timeout=1\r\n"
            # 回应里面加上一个空行，隔开头部和内容
            response += "\r\n"
            # 服务端回应
            connection_socket.send(response.encode("GBK"))
            connection_socket.send(html_content)
            # 注意直接使用open的话就要关闭

    def serve_client(self, connection_socket):
        # 接收浏览器发来的http请求
        request = connection_socket.recv(1024).decode("utf-8")
        # print(request)

        if request:
            # 分割每个请求，便于观察调试
            print("------")
            # 按行分割request，存储进列表
            request_split = request.splitlines()
            # 用正则表达式匹配request 提取出请求的html
            # GET /index.html HTTP/1.1
            # 将正则表达式分组，方便提取出×××.html
            ret = re.match(r"[^/]+(/[^ ]*)", request_split[0])
            file_name = ""
            if ret:
                file_name = ret.group(1)
                print(file_name)

                if file_name == "/":
                    file_name += "login.html"

            # 返回页面信息
            # 根据解析出的file_name判断请求的是动态资源还是静态资源
            # 设置为伪静态 虽然是以Html结尾但仍然是动态资源
            # 因为前端便于简单全部以get请求，故此处有几个特殊的url需要处理
            url_login = r"/loginsuccess\.html\?username=(.*)\&password=(.*)"
            url_register = r"/register.html\?username=(.*)\&password=(.*)\&confirm=(.*)"
            ret_login = re.match(url_login, file_name)
            ret_register = re.match(url_register, file_name)
            # ret为真就不执行下面这个if
            if not file_name.endswith(".html") and not ret_login and not ret_register:
                self.deal_static(file_name, connection_socket)
            else:
                self.deal_dynamic(file_name, connection_socket)
        # 尽管默认有了keep-Alive头，发送完就关闭实际上就是短连接
        connection_socket.close()


    def set_response_header(self, status, headers):
        self.status = status
        self.headers = headers


def main():
    if len(sys.argv) == 2:
        try:
            port = int(sys.argv[1])  # port
        except Exception as e:
            print("端口输入错误")
            return
    else:
        print("请以如下方式运行:(您运行该项目的python解释器路径) WebServer.py 7777(端口号可设定)")
        return

    server = WebServer(port)
    server.run()


if __name__ == '__main__':
    main()
