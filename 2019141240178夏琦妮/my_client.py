# coding: utf-8
# client.py


import json  # 消息序列化
import socket  # 网络通信
import struct  # 字节转换
import time

# import _thread
import init


def send_request(sock, in_, params):
    """
    实际执行发送逻辑，并获得返回结果
    :param sock:socket连接
    :param in_:请求名
    :param params:需要发送的参数
    :return:响应名以及响应的内容
    """
    # in_表示请求的名称，params表示请求的参数
    request = json.dumps({"in": in_, "params": params})  # 将请求消息体封装成json
    length_prefix = struct.pack("I", len(request))  # 将请求长度前缀编码成字符串
    sock.send(length_prefix)  # send方法有可能只会发送了部分内容，它通过返回值来指示实际发出去了多少内容
    sock.sendall(request.encode("utf-8"))  # sendall = send + flush
    length_prefix = sock.recv(4)  # 响应长度前缀
    length, = struct.unpack("I", length_prefix)  # 将字节数据解码为整型
    body = sock.recv(length)  # 响应消息体
    response = json.loads(body.decode("utf-8"))  # 反序列化，将字符串解析为json对象
    return response["out"], response["result"]  # 返回响应类型和结果 out为响应的名称，结果用result表示


def send_weather_info(s, run_index, city_name):
    out, result = send_request(s, "weather info", city_name)
    print(out, result)


def send_random_number_request(s, run_index, request_number):
    for i in range(request_number):  # 连续发送 10 个请求
        # 调用rpc函数发送请求并返回结果
        out, result = send_request(s, "random number request", "run_index %d  reader %d" % (run_index, i))
        print(out, result)
        time.sleep(1)  # 休眠 1s，便于观察


def create_conn(run_index, request_class, param):
    global s
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # 创建一个套接字
        s.connect((init.server_host, init.server_post))  # 请求连接远程服务器
        if request_class == "random":
            send_random_number_request(s, run_index, param)
        elif request_class == "weather":
            send_weather_info(s, run_index, param)
        else:
            print("参数错误")
            return

    except Exception as e:
        print(e)  # 输出出现的问题
    finally:
        s.close()  # 关闭连接...


# def print_message(index):
#     for i in range(10):
#         print(index)
#         sleep(0.5)


if __name__ == '__main__':
    print("请求开始")
    # create_conn(1, "random",10)
    create_conn(1, "weather", "chengdu")
