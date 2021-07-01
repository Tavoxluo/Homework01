import init
import node
import message
from socket import *
import re

this=node.node(init.sip,init.sport)

while True:
    this.socket.settimeout(10)
    try:
        msg,addr=this.socket.recvfrom(1024)
        msg=msg.decode()
        bmsg=re.match(r'Mode:(.*?),.*',msg)
        if(bmsg.group(1)=='Ping'):
            this.socket.sendto(message.backPingMsg(this.ID).encode(),addr)
            bmsg=re.match(r'.*ID:(.*)',msg)
            this.updateRouteTable(bmsg.group(1),addr[0],addr[1]) 
        elif(bmsg.group(1)=='bPing'):
            bmsg=re.match(r'.*ID:(.*)',msg)
            this.updateRouteTable(bmsg.group(1),addr[0],addr[1])
        elif(bmsg.group(1)=='findNode'):
            bmsg=re.match(r'.*ID:(.*),DesID:(.*)',msg)
            this.updateRouteTable(bmsg.group(1),addr[0],addr[1])
            nodelist=this.findNode(bmsg.group(2))
            for i in nodelist:
                this.socket.sendto(message.backFindNodeMsg(this.ID,i['id'],i['ip'],i['port']).encode(),addr)
        elif(bmsg.group(1)=='bFindNode'):
            bmsg=re.match(r'.*ID:(.*),DesID:(.*),Ip:(.*),Port:(.*)',msg)
            this.updateRouteTable(bmsg.group(1),addr[0],addr[1])
            this.updateRouteTable(bmsg.group(2),bmsg(3),int(bmsg(4)))
    except:
        print(this.routeTable)


