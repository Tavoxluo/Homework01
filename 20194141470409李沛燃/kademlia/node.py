import hashlib
import init
import message
from socket import *
import math

class node:
    def __init__(self,ip,port):
        self.ID=self.getID(ip,port)  #十进制形式sha1加密结果
        self.ip=ip
        self.port=port
        self.routeTable=self.initRouteTable()
        self.socket=socket(AF_INET, SOCK_DGRAM)
        self.socket.bind((ip,port))
        
    def getID(self,ip,port):  #以ip+port字符串来生成sha1十六进制加密，得到160bit结果
        sha=hashlib.sha1()
        msg=ip+str(port)
        sha.update(msg.encode('UTF-8'))
        return sha.hexdigest()

    def initRouteTable(self): #初始化路由表(k桶)
        k_bucket=list()
        for i in range(0,160):
            k_bucket.append(list())
        return k_bucket
        
    def updateRouteTable(self,desID,ip,port):
        distance=int(self.ID,16)^int(desID,16)
        print(distance)
        if(distance==0):
            return
        k_num=math.floor(math.log(distance,2))
        for i in self.routeTable[k_num]:
            if(i['id']==desID):
                self.routeTable[k_num].remove(i)
                self.routeTable[k_num].append(i)
                return
        if(len(self.routeTable[k_num])<init.ksize):
            self.routeTable[k_num].append({'id':desID,'ip':ip,'port':port})
        else:
            firstnode=self.routeTable[k_num][0]
            self.Ping(firstnode['ip'],firstnode['port'])
            self.socket.settimeout(2)
            try:
                self.socket.recv(1024)
                self.routeTable[k_num].remove(firstnode)
                self.routeTable[k_num].append(firstnode)
                self.socket.settimeout(None)
                return
            except:
                self.routeTable[k_num].remove(firstnode)
                self.routeTable[k_num].append({'id':desID,'ip':ip,'port':port})
                return 


    def findNode(self,desID):
        distance=int(self.ID,16)^int(desID,16)
        k_num=math.floor(math.log(distance,2))
        nodelist=list()
        for i in self.routeTable[k_num]:
            nodelist.append(i)
        if(len(nodelist)<init.ksize):
            left=k_num-1
            right=k_num+1
            while True:
                if(left<0 and right >159):
                    return nodelist
                elif(left>=0  and right>159):
                    if(len(self.routeTable[left])==0):
                        left=left-1
                    for i in self.routeTable[left]:
                        nodelist.append(i)
                        if(len(nodelist)==init.ksize):
                            return nodelist
                        else:
                            left=left-1
                elif(left<0 and right<=159):
                    if(len(self.routeTable[right])==0):
                        right=right+1
                    for i in self.routeTable[right]:
                        nodelist.append(i)
                        if(len(nodelist)==init.ksize):
                            return nodelist
                        else:
                            right=right+1
                elif(left>=0 and right<=159):
                    if(len(self.routeTable[left])==0):
                        left=left-1
                    if(len(self.routeTable[right])==0):
                        right=right+1
                    for i in self.routeTable[left]:
                        nodelist.append(i)
                        if(len(nodelist)==init.ksize):
                            return nodelist
                        else:
                            left=left-1
                    for j in self.routeTable[right]:
                        nodelist.append(j)
                        if(len(nodelist)==init.ksize):
                            return nodelist
                        else:
                            right=right+1
        else:
            return nodelist


    def ping(self,ip,port):
        msg=message.PingMsg(self.ID)
        self.socket.sendto(msg.encode(),(ip,port))