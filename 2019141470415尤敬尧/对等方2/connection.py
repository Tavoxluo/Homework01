 
# -*- coding: utf-8 -*-
import configparser
import ipaddress
import os
import socket
import threading
import os
import struct
import zipfile
import time
import json
import md5
import sys
SEND_BUF_SIZE = 256
 
RECV_BUF_SIZE = 256
class Connection:
    #config.ini里的本地节点的属性
    __ip_addr=None
    __port_number=None
    __share_dir=None
    __peer_ID=None
    __peer_addr=None
    __peer_ports=None
    __query_res = dict()
    __path_list = dict()
    __state = 0 # 如果为1，表示正在发送或者是转发信息
    



    def set_ip(self, ip_addr):
    		self.__ip_addr = ip_addr

    def set_port(self, port):
		    self.__port_number = int(port)

    def set_peer_ip(self, peer_addr):
		    self.__peer_addr = peer_addr

    def set_ports(self, peer_ports):
		    self.__peer_ports= peer_ports

    def set_share_dir(self, share_dir):
		    self.__share_dir = share_dir

    def set_state(self, state):
		    self.__state = state
    __source_ip = '127.0.0.1'#源ip及源端口
    __source_port = None
    # 服务器端收到的命令
    __cmd = []


    def tcp_handler(self, client, addr):
            while True:
                try:
                    res=client.recv(1024)

                    if not res:
                        continue
                    else:
                        self.__cmd=res.decode('utf-8').split()
                        if self.__cmd[0]=='get':
                            res = self.update_ttl(res)
                            self.__source_ip = self.__cmd[2]#
                            self.__source_port = self.__cmd[3]#在client所发的请求中，我们将client的端口号和ip以及ttl一同发送至server
                            self.__query_res[self.__cmd[1]]= 0#初始化该值为0
                            self.query(self.__share_dir, self.__cmd[1])
                            if self.__query_res[self.__cmd[1]] == 1:#本地服务器查找到对应的文件
                                print("Server: (%s,%s)have already found the target file:%s"%(self.__ip_addr,self.__port_number,self.__cmd[1]))
                                print("Now the server begin to send the file to the source host!")
                               # self.__send(client,self.__cmd[1])
                                print("The target file has been already sent to the source_port:%s,source_ip:%s"%(self.__source_port,self.__source_ip))

                                msg = "request %s %s %s " % (self.__cmd[1], self.__ip_addr, self.__port_number)#打印的值有问题
                                #print(msg)
                                self.tcp_client_notice(self.__source_ip, self.__source_port, msg)#利用找到文件对等方的客户端向源节点的服务器建立连接。
       
                                #self.__save(client)
                                print("The sourec_port:(%s,%s) have received the file already!"%(self.cmd[2],self.cmd[3]))    
                                
                            if self.__query_res[self.__cmd[1]] == 0:
                                if int(self.__cmd[-1])<=0:
                                    print("over ttl! Traceback!")
                                    self.tcp_client_notice(self.__source_ip,self.__source_port,"超越查询范围，查询失败！")
                                else:
                                    print("localhost does not find the file,querying the neighbor:")
                                    for i in range(0,len(self.__peer_addr)):
                                        if self.__peer_ports[i]==self.__source_port:#不能给请求资源的主机发送查询文件的请求
                                            continue
                                        else:
                                            print("send query-request to %s "%self.__peer_addr[i])
                                            self.tcp_client_notice(self.__peer_addr[i],self.__peer_ports[i],res)
                                            
                            else:
                                print("网络中没有对应文件！")
                        #elif self.__cmd[0]=='request':  
                        elif self.__cmd[0]=="request":#收到request请求
                            client.send("ready".encode('utf-8'))#通知发送方可以发送文件
                            print("源地址已通知发送方发送文件！")
                            print("开始接收文件····")
                            self.__save(client)#上面四行需要在查询主机保留，在其余对等方注释掉！！！
                       
                        else:#
                            
                            self.__cmd[0]=='exit'
                            print("退出")
                        
                except:
                    pass
                                    

                                

    def tcp_server(self):
            #创建socket
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                server_addr=(self.__ip_addr,self.__port_number)

            #绑定ip与服务器端口号
                print("starting listen on ip %s, port %s" % server_addr)
                sock.bind((self.__ip_addr, self.__port_number)) 
            #设置新的缓冲区大小
                sock.setsockopt(socket.SOL_SOCKET, socket.SO_SNDBUF, SEND_BUF_SIZE)
                sock.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF, RECV_BUF_SIZE)

            #获得新的缓冲区大小
                s_send_buffer_size = sock.getsockopt(socket.SOL_SOCKET, socket.SO_SNDBUF)
                s_recv_buffer_size = sock.getsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF)
                print("socket send buffer size[new] is %d" % s_send_buffer_size)
                print("socket receive buffer size[new] is %d" % s_recv_buffer_size)
                print("The server is listening······")
                sock.listen(5)#最多1个排队等候的线程
                while True:
                    try:
                        client,addr=sock.accept()
                        #源节点与远程服务器已连接，本地服务器用来接收数据
                       
                            
                        print("Tcp_Server (%s,%s) is working:"%(self.__ip_addr,self.__port_number))
                        
                    except ConnectionAbortedError:
                        print("server except")
                        continue
                    t = threading.Thread(target=self.tcp_handler, args=(client, addr))
                    t.start()
                
        
            


#ttl-1
#send函数简化了文件头和md5加密的操作
    def tcp_client_notice(self, ip, port, msg):
        tcp_client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        
        try: # 如果对方未启动，则不会正常连接
            tcp_client.connect((ip, int(port)))
         
            if msg.split()[0]=='request':
                tcp_client.send(msg.encode('utf-8'))
                if tcp_client.recv(1024).decode('utf-8')=="ready":
                    self.__send(tcp_client,msg.split()[1]) 
            print("连接成功！！！")
            tcp_client.send(msg.encode())#将此消息传播给其邻接对等方
            tcp_client.shutdown(2)
            tcp_client.close()#客户端一旦发送完即关闭
        except Exception as e:
            print(e)
            print("TCP connection  of get (%s,%s) connecting to (ip: %s , port:%s ) is failed! "%(self.__ip_addr,self.__port_number,ip,port))
            pass

    def __send(self, conn, filename):
       
        route_0=os.path.dirname(os.path.realpath(__file__))
        print(route_0)
        dir=self.__share_dir
        str=dir.split("/")[0]#获得文件夹的1的名字1
        filepath=route_0+"\\"+str+"\\"+filename#得到文件的绝对路径
        print(filepath)
        filesize_bytes=os.path.getsize(filepath)#绝对路径的文件名
        with open(filepath, 'rb') as f:
            data=f.read()
        data1=data.decode('utf-8')
        
        header_dic = {
			'filename': filename,
			'md5': md5.get_file_md5(filepath),
            'body':data1
        }#已测试filename及filesize_bytes是正确的
        print("header_dic size:")
        print(sys.getsizeof(header_dic))
        print(header_dic)
        header_json = json.dumps(header_dic)#字典转化为字符串
        
        print(header_json)#打印头部内容
        header_bytes=header_json.encode('utf-8')#encode头部
     #发送头的长度
        print("header_bytes size:")
        print(sys.getsizeof(header_bytes))
        conn.send(header_bytes)
		# 发送数据    
       
        print("主机:%s 已将文件传输至端口号:%s"%(self.__ip_addr,conn))
    #send正确
    
        
    def __save(self,conn):
        obj = conn.recv(1024)#接收报头的长度
        print(sys.getsizeof(obj))
        if obj:
            print('等待接收数据````')
        head_info=obj.decode('utf-8')
        print(head_info)
        
        head_dic = json.loads(head_info)
        print(head_dic)#字典msg
        
    
        filename =head_dic['filename']
        print(filename)
        data=head_dic['body']
        data2=data.encode('utf-8')
           # 接收数据
           #进入该对等方的文件夹
        route_0=os.path.dirname(os.path.realpath(__file__))
        dir=self.__share_dir
        str=dir.split("/")[0]#获得文件夹的1的名字1
        filepath=route_0+"\\"+str#得到文件的绝对路径
        os.chdir(filepath)
        f =open(filename,'wb')
        f.write(data2)
        f.close()
        print("文件已写完！")
        
          
    
        #true_name = filename
        #filepath = self.__path_list[filename]

        
        
        
        
  


    def update_ttl(self,msg):
        msg = msg.decode().split()
        msg[-1] = str(int(msg[-1]) - 1)
        new_msg = " ".join(msg) 
        return new_msg
    def query(self, root, filename):


            items = os.listdir(root)
            for item in items:
                path = os.path.join(root, item)
                if path.split('\\')[-1] == filename or path.split('/')[-1] == filename:
                    self.__query_res[filename] = 1
                    self.__path_list[filename] = path.replace('\\', '/')
                elif os.path.isdir(path):
                    self.query(path.replace('\\', '/'), filename)