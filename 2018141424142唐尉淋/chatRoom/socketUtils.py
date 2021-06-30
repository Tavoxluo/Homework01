#!/usr/bin/python
# -*- coding: UTF-8 -*-
"""
socket 库工具类
包含常见的int、str、bytes、json、file等数据的发送与读取
相应的应该依照发送数据的顺序进行读取，例如使用 send_string() 发送数据应使用 recv_string() 进行读取
"""
import os
import json
import socket

__all__ = [
    "recv", "recv_wait",
    "send_number", "recv_number",
    "send_bytes", "recv_bytes",
    "send_string", "recv_string",
    "send_json", "recv_json",
    "send_file", "recv_file",
]


def recv(conn: socket.socket, bufsize: int = 1024) -> bytes:
    """
    recv 的封装
    :param conn: socket 连接
    :param bufsize: 缓冲区大小
    :return: 接收的数据
    """
    return conn.recv(bufsize)


def recv_wait(conn: socket.socket, bufsize: int = 1024) -> bytes:
    """
    recv 的封装,等待读取够 bufsize 才会返回
    :param conn: socket 连接
    :param bufsize: 缓冲区大小
    :return: 接收的数据
    """
    return conn.recv(bufsize, socket.MSG_WAITALL)


def send_number(conn: socket.socket, number: int):
    """
    发送一个数字(int)类型的数据
    :param conn: socket 连接
    :param number: 要发送的 number
    :return:
    """
    conn.sendall(number.to_bytes(4, byteorder='big'))


def recv_number(conn: socket.socket) -> int:
    """
    接收一个数字(int)类型的数据
    :param conn: socket 连接
    :return: 接收的 number 数据
    """
    return int.from_bytes(conn.recv(4), byteorder='big')


def send_bytes(conn: socket.socket, data: bytes):
    """
    发送 bytes 类型的数据
    :param conn: socket 连接
    :param data: 要发送的 bytes 字节数据
    :return:
    """
    # 先发送内容的长度
    send_number(conn, data.__len__())
    # 再发送内容
    conn.sendall(data)


def recv_bytes(conn: socket.socket) -> bytes:
    """
    接收 bytes 类型的数据
    :param conn: socket 连接
    :return: 接收的 bytes 字节数据
    """
    # 先读取内容的长度
    length = recv_number(conn)
    # 再读取内容
    return conn.recv(length)


def send_string(conn: socket.socket, text: str, *, encoding="utf-8"):
    """
    发送字符串(String)数据
    :param conn: socket 连接
    :param text: 要发送的字符串
    :param encoding: 编码
    :return:
    """
    send_bytes(conn, bytes(text, encoding=encoding))


def recv_string(conn: socket.socket, *, encoding="utf-8") -> str:
    """
    接收字符串(String)数据
    :param conn: socket 连接
    :param encoding: 编码
    :return: 接收的字符串数据
    """
    return recv_bytes(conn).decode(encoding=encoding)


def send_json(conn: socket.socket, data: dict, *, ensure_ascii=True):
    """
    发送可以进行 json.dumps() 的字典数据
    :param conn: socket 连接
    :param data: 要发送的 dict 数据
    :param ensure_ascii: 是否使用 ASCII 编码
    :return:
    """
    send_string(conn, json.dumps(data, ensure_ascii=ensure_ascii))


def recv_json(conn: socket.socket, *, encoding="utf-8") -> dict:
    """
    接收可以使用 json.loads() 转换成 json 数据
    :param conn: socket 连接
    :param encoding: 编码
    :return:
    """
    return json.loads(recv_string(conn, encoding=encoding), encoding=encoding)


def send_file(conn: socket.socket, filepath: str):
    """
    发送文件
    :param conn: socket 连接
    :param filepath: 文件路径
    :return:
    """
    # 检查文件是否存在
    if os.path.isfile(filepath):
        # 发送文件名
        path, filename = os.path.split(filepath)
        send_string(conn, filename)
        # 发送文件数据
        with open(filepath, "rb") as fp:
            send_bytes(conn, fp.read())
    else:
        raise FileNotFoundError(f"\"{filepath}\" file not found")


def recv_file(conn: socket.socket, path: str = None, filepath: str = None) -> str:
    """
    接收文件
    :param conn: socket 连接
    :param path: 文件存放目录
    :return: 文件存放路径
    """
    filename = recv_string(conn)
    if filepath is None:
        # 读取文件名
        filepath = os.path.normcase(os.path.join("" if path is None else path, filename))
    else:
        filepath = os.path.normcase(filepath)
    save_dir = os.path.dirname(filepath)
    if save_dir and not os.path.isdir(save_dir):
        print("路径不存在，自动创建")
        os.makedirs(save_dir)
    # 读取写入文件
    with open(filepath, "wb") as fp:
        buff_size = 1024
        # 获取文件字节长度
        filesize = recv_number(conn)  # 文件总大小
        recv_size = 0  # 已读取大小
        print(f"读取文件: {filename}({filesize})")
        while recv_size < filesize:
            # 判断未读取的大小是否大于默认读取大小，大于按默认读取，小于按剩余读取
            if filesize - recv_size > buff_size:
                recv_tmp = conn.recv(buff_size)
            else:
                recv_tmp = conn.recv(filesize - recv_size)

            recv_size += len(recv_tmp)
            fp.write(recv_tmp)
        print(f"读取文件成功: {filepath}({recv_size}/{filesize})")
        return filepath
