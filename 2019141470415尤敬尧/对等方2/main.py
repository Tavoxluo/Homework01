
# -*- coding: utf-8 -*-

import socket
import sys
import struct
import threading
import configparser
import config
import time
import connection
import configparser
import os
if __name__ == '__main__':
    
    print(    "Welcome to the qurey_flooding_system:"    )
    print("*********************************************")  
    print("*                                           *")
    print("*                                           *")
    print("*   Query-Flooding-based-resource-sharer    *")
    print("*                                           *")
    print("*                              YJY          *")
    print("*                           2019141470415   *")  
    print("*********************************************")

    #从config.ini中获得本地属性信息
    peer=config.Config()
    peer_info=peer.get_attr()
    print(peer_info)
    i=0
    str=peer_info['peer_addr']
    mydir=peer_info['share_dir']
    print(str)
    i=len(str)
    print(i)#i作为之后client的对等方的值
     #建立服务器
    peer_server =connection.Connection()
    peer_server.set_ip(peer_info['ip_addr'])
    peer_server.set_port(peer_info['port_number'])#设置本地端口号，ini文件中读取的
    peer_server.set_share_dir(peer_info['share_dir'])
    peer_server.set_peer_ip(peer_info['peer_addr'])
    peer_server.set_ports(peer_info['peer_ports'])#设置邻接对等方的ip地址及端口号
    p1=threading.Thread(target=peer_server.tcp_server)
    p1.start()#启动本地服务器
    
  

    while True:
        print("\n option:\n1:get filename \n2.exit \n3.help")
        opt = input(">>>>>>>>>>Please enter your option(if you don't known the option:please print help)<<<<<<<<<<<:")
        print()
        try:
            opt0= opt.split()[0]
        except:
            continue
        if opt0 =='get':
            #执行get filname的操作
            route_0=os.path.dirname(os.path.realpath(__file__))
            print(route_0)
            dir=peer_info["share_dir"]
            print(dir)
            str=dir.split("/")[0]#获得文件夹的1的名字1
            filepath=route_0+"\\"+str#获得文件夹的绝对路径
            a=0          
            #p2=threading.Thread(target=peer_client.tcp_server)
            #p2.start()#再次启动本地server
          
            for i in range(0,len(str)):
                for file in os.listdir(filepath):
                    if opt.split()[1]==file:
                        print("该文件已在本地！")
                        a=1
                        continue
                    if a==1:
                        break
                #向本地client维护的所有对等方发送消息
                    peer_server.tcp_client_notice(peer_info['peer_addr'][i],peer_info['peer_ports'][i],"get %s %s %s %s"%(opt.split()[1],peer_info['ip_addr'],peer_info['port_number'],peer_info['ttl']))

            time.sleep(2)#等待2s
           
        elif opt0=='config':
            print("以下为本节点的信息：")
            print("IP")
            print(peer_info["ip_addr"])
            print("端口号")
            print(peer_info["port_number"])
            print("邻接对等方IP")
            print(peer_info["peer_addr"])
            print("临界对等方端口号")
            print(peer_info["peer_ports"])
            print("本地文件夹")
            print(peer_info["share_dir"])
            print("TTL")
            print(peer_info["ttl"])
        elif opt0=='exit':
            print("退出")
            break
            exit()
        elif opt0=='help':
            print("输入config查看当前节点信息")
            print("如果你想得到文件“1.txt，请输入1.txt")
            print("如果你想得到文件“2.txt，请输入2.txt")
            print("如果你想得到文件“3.txt，请输入3.txt")

        else:
            print("不合法的输入，请重新获取请求：")
  


