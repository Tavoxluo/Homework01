#节点间的RPC信息定义
def PingMsg(ID):
    return 'Mode:Ping,ID:'+ID

def backPingMsg(ID):
    return 'Mode:bPing,ID:'+ID

def findNodeMsg(ID,desID):
    return 'Mode:findNode,ID:'+ID+',DesID:'+desID

def backFindNodeMsg(ID,desID,ip,port):
    return 'Mode:bFindNode,ID:'+ID+',DesID:'+desID+',Ip:'+ip+',Port:'+str(port)