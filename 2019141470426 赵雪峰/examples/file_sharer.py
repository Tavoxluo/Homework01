import os.path
import socket
import warnings
from typing import Optional

import kademlia.network as network
import asyncio
import cmd
import random
import yaml
import logging

handler = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
log = logging.getLogger('kademlia')
log.addHandler(handler)
log.setLevel(logging.DEBUG)

splitter_hor = "----------------------------- * -----------------------------"
splitter_half = "-------------------------"
splitter_hor_all = "-------------------------------------------------------------"

server = network.Server()

host_addr = socket.gethostbyname(socket.gethostname())

welcome_intro = splitter_hor + "\n" \
                + "  RETR - Download a file through a seed file. \ne.g. retr loveinpractice.seed" + "\n" + splitter_hor_all \
                + "\n  CONN - Connect to a node in I3I\\I\\TWORK. \ne.g. conn 192.168.1.1(ip) 13331(port)\n If no " \
                  "args, " \
                  "then bootstrap a new node without a connection to I3I\\I\\TWORK" + "\n" + splitter_hor_all \
                + "\n  JOIN - Join in a I3I\\I\\TWORK through a node known. \ne.g. join 5.64.1.2(ip) 46548(port) " \
                + "\n  CLOSE - Connect to I3I\\I\\TWORK." + "\n" + splitter_hor_all \
                + "\n  UPLOAD - Publish a file to I3I\\I\\TWORK. \ne.g. UPLOAD practicelove.avi \nThen a seed file " \
                  "will be generated. " + "\n" + splitter_hor_all \
                + "\n  exit - Exit." + "\n" + splitter_hor_all \
                + "\n  To get help info please input help" + "\n" \
                + splitter_hor

not_running_prompt = "Not Running > "
running_prompt = "Running > "


# 控制台类，产生一个控制台
class BMTConsole(cmd.Cmd):
    intro = welcome_intro
    prompt = not_running_prompt

    def do_help(self, arg: str) -> Optional[bool]:
        print("Here's not for help document")
        print("Here's for my beloved one")
        print("A man so called BMT")

    def do_retr(self, arg):
        args = arg_parser(arg)
        if len(args) > 1:
            print("Too many args.")
            return False
        print("Retriving from ...")
        ret = read_seed(args[0])
        retrive_from_nodes(ret[0], ret[1])

    def do_conn(self, arg):
        args = arg_parser(arg)
        if len(args) > 1:
            print("Connecting %s ..." % (args[0]))
            if len(args) == 2:
                connect_to_bootstrapped_node(args[1], args[0])
            elif len(args) == 3:
                connect_to_bootstrapped_node(args[1], args[0], args[2])
            else:
                print("Too many Args.")
                return False
        else:
            print("Bootstrapping a new node...")
            if len(arg) != 0:
                bootstrap(arg)
            else:
                bootstrap()

    def do_close(self, arg):
        print("Closing...")
        server.stop()

    def do_upload(self, arg):
        args = arg_parser(arg)
        if len(args) > 1:
            print("Too many args.")
            return False
        print("Uploading your file...")
        publish_file(args[0])

    def do_join(self, arg):
        args = arg_parser(arg)
        return join_in(args[1], args[0])

    def do_exit(self, arg):
        return True

    def postcmd(self, stop: bool, line: str) -> bool:
        try:
            if server.is_online():
                self.prompt = running_prompt
            else:
                self.prompt = not_running_prompt
            return False

        except KeyboardInterrupt:
            return True


# 获取用于启动一个server需要的loop
def _get_loop_and_debug():
    loop = asyncio.get_event_loop()
    loop.set_debug(False)
    return loop


def arg_parser(arg: str):
    return arg.split(' ')


# 初始化一个节点服务
def bootstrap(port=16331):
    loop = _get_loop_and_debug()
    try:
        print("Running on %s:%s" % (host_addr, port))
        loop.run_until_complete(server.listen(int(port), host_addr))
    except OSError:
        print("Can't bootstrap twice!")
    finally:
        pass


# 将本节点启动并连接到指定的节点上
def connect_to_bootstrapped_node(port, interface, self_port=16331):
    loop = _get_loop_and_debug()
    addr = socket.gethostbyname(socket.gethostname())
    loop.run_until_complete(server.listen(int(self_port), addr))

    known = (interface, int(port))
    loop.run_until_complete(server.bootstrap([known]))


# 本节点加入网络
def join_in(port, interface):
    try:
        loop = _get_loop_and_debug()
        known = (interface, int(port))
        loop.run_until_complete(server.bootstrap([known]))
    except TypeError:
        print("NO NODE WORKING ON THAT HOST, JOIN FAILED!")
    finally:
        return False


# 用于发布文件前的文件分割
def split_file(filename):
    file = open(filename, 'rb')
    buffer = file.read()
    pak_cnt = int(len(buffer) / 128) + 1
    result = []
    for i in range(pak_cnt):
        result.append(buffer[i * 128:(i + 1) * 128 - 1])
    filename_true = os.path.split(filename)
    return result, filename_true[1]


# 产生用于存储的键值对，为每一个小文件分配一个随机的key
def generate_key_value_dict(data, filename):
    result = {}
    for value in data:
        result[str(random.random() * 1000)] = value
    seedbase = dict(zip(range(len(data)), result.keys()))
    seed = [filename, seedbase]
    f = open(pure_name(filename) + '.seed', 'w')
    yaml.safe_dump(seed, f, encoding='utf-8', allow_unicode=True, default_flow_style=False)
    f.close()
    return result


# 发布文件
def publish_file(filepath):
    a = generate_key_value_dict(split_file(filepath)[0], split_file(filepath)[1])
    for _in in a.keys():
        loop = _get_loop_and_debug()
        loop.run_until_complete(server.set(_in, a[_in]))


# 读取种子文件
def read_seed(filepath):
    f = open(filepath)
    _in = yaml.load(f)
    filename = _in[0]
    key_info = _in[1]
    return filename, key_info


# 从网络上凭借种子文件获取一个文件
def retrive_from_nodes(filename, key_info: dict):
    tasks = []
    for k in key_info.keys():
        tasks[int(k)] = server.get(key_info[k])
    data = asyncio.gather(*tasks)
    out = open(filename, 'wb+')
    for d in data.result():
        out.write(d)
    out.close()


# 用于获取一个文件除去后缀与前面的内容后的名字
def pure_name(filename: str):
    a = filename.split('.')[0]
    return a


if __name__ == "__main__":
    console_1 = BMTConsole()
    console_1.cmdloop()
