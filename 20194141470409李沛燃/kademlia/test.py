import init
import node
import message
from socket import *
import re

def joinIn(): #加入网络
    this.updateRouteTable(this.getID(init.sip,init.sport),init.sip,init.sport)
    this.socket.sendto(message.findNodeMsg(this.ID,this.ID).encode(),(init.sip,init.sport))
    this.socket.settimeout(2)
    count=1
    temp=list()
    while True:
        try:
            msg,addr=this.socket.recvfrom(1024)
            msg=msg.decode()
            print(msg)
            bmsg=re.match(r'.*ID:(.*),DesID:(.*),Ip:(.*),Port:(.*)',msg)
            this.updateRouteTable(bmsg.group(1),addr[0],addr[1])
            this.updateRouteTable(bmsg.group(2),bmsg.group(3),int(bmsg.group(4)))
            print(2)
            temp.append({'id':bmsg.group(2),'ip':bmsg.group(3),'port':int(bmsg.group(4))})
            if(count==5):
                break
        except:
            if(len(temp)==0):
                break
            for i in temp:
                this.socket.sendto(message.findNodeMsg(this.ID,this.ID).encode(),(i['ip'],i['port']))
            count=count+1
            temp=list()
    this.socket.settimeout(None)

this=node.node(init.sip,0)
print(this.socket.getsockname()[1])
joinIn()


while True:
    this.socket.settimeout(10)
    try:
        msg,addr=this.socket.recvfrom(1024)
        msg=msg.decode()
        bmsg=re.match(r'Mode:(.*?),.*',msg)
        if(bmsg.group(1)=='Ping'):
            this.socket.sendto(message.backPingMsg().encode(),addr)
            bmsg=re.match(r'.*ID:(.*)',msg)
            this.updateRouteTable(bmsg.group(1),addr[0],addr[1]) 
        elif(bmsg.group(1)=='bPing'):
            bmsg=re.match(r'.*ID:(.*)',msg)
            this.updateRouteTable(bmsg.group(1),addr[0],addr[1])
        elif(bmsg.group(1)=='findNode'):
            bmsg=re.match(r'.*ID:(.*),DesID:(.*)',msg)
            this.updateRouteTable(bmsg.group(1),addr[0],addr[1])
            nodelist=this.findNode(bmsg.group(2))
            print(nodelist)
            for i in nodelist:
                this.socket.sendto(message.backFindNodeMsg(this.ID,i['id'],i['ip'],i['port']).encode(),addr)
        elif(bmsg.group(1)=='bFindNode'):
            bmsg=re.match(r'.*ID:(.*),DesID:(.*),Ip:(.*),Port:(.*)',msg)
            this.updateRouteTable(bmsg.group(1),addr[0],addr[1])
            this.updateRouteTable(bmsg.group(2),bmsg(3),int(bmsg(4)))
    except:
        print(this.routeTable)