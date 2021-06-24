# coding: utf8
# blocking_single.py

import _thread as thread
import json
import random
import socket
import struct

import requests

import init


def handle_conn(conn, addr, handlers):
    """
    由主线程创建的用来处理请求的函数
    :param conn: socket连接
    :param addr: 客户端的地址
    :param handlers: 存储处理函数的dict
    :return: 无
    """
    print(addr, "comes")
    while True:  # 循环读写
        length_prefix = conn.recv(4)  # 请求长度前缀

        if not length_prefix:  # 连接关闭了
            print(addr, "bye")
            conn.close()
            break  # 退出循环，处理下一个连接
        length, = struct.unpack("I", length_prefix)  # 将二进制解析为数字
        print("the length of request is " + str(length))
        body = conn.recv(length)  # 请求消息体
        request = json.loads(body)  # 将request的信息从字符串转化为json对象
        in_ = request['in']
        params = request['params']
        print(in_, params)

        handler = handlers[in_]  # 查找请求处理器 不同的名称进行不同的处理函数

        handler(conn, params)  # 处理请求 此处会调用ping函数


def loop(sock, handlers):
    """
    while True循环，不断接受并处理请求，只到手动终止
    :param sock: socket对象
    :param handlers: 存储处理函数的dict
    :return:无
    """
    i = 1
    while True:
        print("循环开始%d次！" % i)
        conn, addr = sock.accept()  # 接收连接
        print(conn)
        thread.start_new_thread(handle_conn, (conn, addr, handlers))  # 开启新线程进行处理 handle_conn是一个函数
        print("循环完成%d次！" % i)
        i += 1


def send_random_number(conn, params):
    """
    handlers变量中封装的一个函数
    :param conn: socket连接
    :return:无
    """
    response_param = "the random number from server is " + str(random.randint(0, 1000))  # 返回的消息
    send_result(conn, "random number response", response_param)


def send_weather_info(conn, city_name):
    url = "http://wttr.in/{}".format(city_name)
    response_txt = requests.get(url).text
    send_result(conn, "weather info response", response_txt)


def send_result(conn, out, result):
    """
    执行发送逻辑的函数
    :param conn:socket连接
    :param out:response名字
    :param result:要发送的数据
    :return:无
    """
    response = json.dumps({"out": out, "result": result})  # 响应消息体
    length_prefix = struct.pack("I", len(response))  # 响应长度前缀
    conn.send(length_prefix)  # 发送消息的长度
    conn.sendall(response.encode("utf-8"))  # 发送消息的内容


if __name__ == '__main__':
    # AF_INET 表示使用ipv4  SOCK_STREAM　流式socket，TCP
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # 创建一个 TCP 套接字
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)  # 打开 reuse addr 选项
    sock.bind((init.server_host, init.server_post))  # 绑定端口
    backlog = 5  # 传入listen函数的backlog参数表示没有调用accept进行处理的连接个数
    sock.listen(backlog)  # 监听客户端连接
    handlers = {  # 注册请求处理器
        "random number request": send_random_number,
        "weather info": send_weather_info
    }
    loop(sock, handlers)  # 进入服务循环...
