import socket
import io
import sys
import datetime
import threading
import configparser


class WSGIServer(object):
    # socket的两个参数初始化
    address_family = socket.AF_INET
    socket_type = socket.SOCK_STREAM
    # 允许队列，后面可能删
    request_queue_size = 10

    def __init__(self, server_address):
        # 创建socket，利用socket获取客户端的请求
        self.listen_socket = socket.socket(
            self.address_family,
            self.socket_type
        )
        # 设置socket的工作模式
        self.listen_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        # 绑定地址
        self.listen_socket.bind(server_address)
        # 激活需求队列
        self.listen_socket.listen(self.request_queue_size)
        # 获得本地服务IP和端口
        # host, port = self.listen_socket.getsockname()[:2]
        # 根据设置获取IP和端口
        host, port = SERVER_ADDRESS
        # 获得服务器别名
        self.server_name = socket.getfqdn(host)
        self.server_port = port
        # 返回的头信息Return headers set by Web framework/Web application
        self.headers_set = []

    # 设置server对接的应用程序（处理程序）
    def set_app(self, application):
        self.application = application

    # 启动WSGI server服务，不停的监听并获取socket数据。
    def serve_forever(self):
        print('WSGIServer: Serving HTTP on port {port} ...\n'.format(port=PORT))
        while True:  # 无限循环监听
            # 获得监听到的socket请求
            client_socket, client_address = self.listen_socket.accept()
            # 创建新线程
            new_thread = threading.Thread(target=self.handle_one_request, args=(client_socket,))
            # 启动新线程
            new_thread.start()

    # 解决请求函数
    def handle_one_request(self, client_socket):
        # 获取请求数据
        self.request_data = request_data = client_socket.recv(1024).decode('utf8')
        if request_data:
            '''
            # 逐行打印请求报文
            print(''.join(
                '< {line}\n'.format(line=line)
                for line in request_data.splitlines()
            ))
            '''
            # 分解报文，得到请求报文信息
            # 用需求信息组成环境字典
            env = self.parse_request(request_data)
            # 给应用传递两个参数，environ，start_response
            result = self.application(env, self.start_response)
            # 用从web应用传回的response给客户发送完成请求报文
            self.finish_response(result, client_socket)
        else:
            client_socket.close()

    # 分解报文
    def parse_request(self, text):
        # 获得报文第一行，拆分
        request_line = text.splitlines()[0]
        request_line = request_line.rstrip('\r\n')

        # 拆分各个模块信息
        (request_method,  # GET/POST
         path,  # '/...'
         request_version  # HTTP/1.1
         ) = request_line.split()
        return self.get_environ(request_method, path)

    # 获取environ数据并设置当前server的工作模式
    def get_environ(self, request_method, path):
        # werkzeug_request = Request()
        env = {
            'wsgi.version': (1, 0),
            'wsgi.url_scheme': 'http',
            'wsgi.input': io.StringIO(self.request_data),
            'wsgi.errors': sys.stderr,
            'wsgi.multithread': True,
            'wsgi.multiprocess': False,
            'wsgi.run_once': False,
            'REQUEST_METHOD': request_method,
            'PATH_INFO': path,
            'SERVER_NAME': self.server_name,
            'SERVER_PORT': str(self.server_port)
        }
        # 返回环境值
        return env

    # 初始化返回报文
    def start_response(self, status, response_headers, exc_info=None):
        # 必要的报文要素，记录报文发送时间和server版本
        now_time = datetime.datetime.now()
        str_now_time = datetime.datetime.strftime(now_time, '%Y-%m-%d %H:%M:%S')
        server_headers = [
            ('Date', str_now_time),
            ('Server', 'WSGIServer 0.2'),
        ]
        self.headers_set = [status, response_headers + server_headers]

    # 完成回复报文
    def finish_response(self, result, client_socket):
        try:
            # 获取返回报文头信息
            status, response_headers = self.headers_set
            # 准备发送报文头
            response_head = 'HTTP/1.1 {status}\r\n'.format(status=status)
            response = 'HTTP/1.1 {status}\r\n'.format(status=status)
            for header in response_headers:
                response_head += '{0}: {1}\r\n'.format(*header)
                response += '{0}: {1}\r\n'.format(*header)
            response_head += '\r\n'
            response += '\r\n'

            # 准备发送报文体
            response_body = b''
            for data in result:
                response += str(data, encoding="utf-8")
                response_body += data
            '''
            # 输出报文内容
            print(''.join(
                '> {line}\n'.format(line=line)
                for line in response.splitlines()
            ))
            '''
            client_socket.send(response_head.encode('GBK'))
            client_socket.send(response_body)
            # client_socket.sendall(response.encode('utf8'))
        except Exception:
            print('Exception')


# 创建server实例
def make_server(server_address, application):
    server = WSGIServer(server_address)
    server.set_app(application)
    return server


if __name__ == '__main__':
    # 基础参数设置
    config = configparser.ConfigParser()
    config.read('config.ini', encoding='utf-8')
    HOST = config.get("ipconfig", "HOST")
    PORT = config.getint("ipconfig", "PORT")
    SERVER_ADDRESS = (HOST, PORT)
    # web应用调用路径
    app_path = 'flask_app:flask_app'  # sys.argv[1]
    # 分解文件名和app实例名
    _module, _application = app_path.split(':')
    # import需求文件
    module = __import__(_module)
    _application = getattr(module, _application)
    # 创建server
    httpd = make_server(SERVER_ADDRESS, _application)
    # 一直运行server
    httpd.serve_forever()
