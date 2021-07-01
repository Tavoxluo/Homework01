#利用json格式化交互信息便于在client和server传输及处理

import struct
import json

maxBuffSize = 1024
#服务器
SERVEIP = "0.0.0.0"
SERVEPORT = 8888
#客户端
SERVERIP = "127.0.0.1"
SERVERPORT = 8888
#文件发送接收
FILEIP = "0.0.0.0"
FILEPORT  = 1031

def pack(data):
    return struct.pack('>H', len(data)) + data


def send(socket, data_dict):
    socket.send(pack(json.dumps(data_dict).encode('utf-8')))


def recv(socket):
    try:
        data = b''
        #循环接收完整数据
        surplus = struct.unpack('>H', socket.recv(2))[0]
        socket.settimeout(5)#非阻塞
        while surplus:
            recv_data = socket.recv(maxBuffSize if surplus > maxBuffSize else surplus)
            data += recv_data
            surplus -= len(recv_data)
        socket.settimeout(None)#阻塞
        return json.loads(data)
    except:
        pass
