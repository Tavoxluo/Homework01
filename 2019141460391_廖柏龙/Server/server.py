import socket
from threading import Thread

client_dict = {}
account_dict = {}
name={}

#广播数据，但凡存在用户发送的数据，都会对所有用户进行广播
def brodcast(msg,nikename = ''):
    #print('rignt')
    if nikename == '':
        for khd_socket in client_dict.values():
            khd_socket.send(bytes('E:'.encode('gbk'))+msg+ b'\n')
    else:
        for khd_socket in client_dict.values():
            khd_socket.send(bytes(('M:'+nikename).encode('gbk'))+msg+ b'\n')

def loadData():
    with open('data.dat','r') as f:
        for data in f:
            data_split = data.split(' ')
            account_dict[data_split[0]] = data_split[1].split('\n')[0]
    print('用户数据加载完成:',account_dict)

def writeData(account,password):

    account_dict[account] = password
    with open('data.dat','a') as f:
        f.write(account+' '+password+'\n')


#服务器基于用户的管理函数（线程级别），
#对于每个进入交流的用户分配一个子线程，用于管理用户的输入输出
#输入参数 socket 进程标识符，唯一标识某个用户
def process(khd_socket:socket.socket,label):
    try:
        #print("进入线程")
        while True:
            information = khd_socket.recv(1024).decode('gbk')
            #print(information)
            note = information[0:1]
            msg = information[2:]
            #print('note',note)
            #print('msg',msg)
            if note == 'A':
                link(khd_socket,msg)
            elif note == 'N':
                newAccount(khd_socket,msg)
            elif note == 'L':
                root(label,msg,khd_socket)
            elif note == 'M':
                #("in")
                brodcast(bytes(f'{msg}'.encode('gbk')), name[label]+':')
    except:
        #接受数据或广播数据出错时断开连接，并向全部用户进行广播
        #print("登陆失败")
        #khd_socket.send(bytes('false'.encode('gbk')))
        khd_socket.close()
        if label in name:
            print(name[label] + '客户端断开连接')
            del client_dict[name[label]]
            brodcast(f'\n用户##{name[label]}##离开聊天室\n'.encode('gbk'))
            del name[label]

def link(khd_socket:socket.socket,msg):
    i = msg.split('\n')
    if i[0] in account_dict:
        # print(account_dict[i[0]],i[1])
        if account_dict[i[0]] == i[1]:
            # print(f'{i[0]}登陆成功')
            khd_socket.send(bytes('true'.encode('gbk')))
            return True
        else:
            # print(f'{i[0]}登陆失败')
            khd_socket.send(bytes('false'.encode('gbk')))
            return False
    else:
        # print(f'{i[0]}登陆失败')
        khd_socket.send(bytes('false'.encode('gbk')))
        return False

#新建账户函数
def newAccount(khd_socket:socket.socket,msg):
    i = msg.split('\n')
    if i[0] in account_dict:
        khd_socket.send(bytes('false'.encode('gbk')))
    else:
        account_dict[i[0]] = i[1]
        writeData(i[0],i[1])
        khd_socket.send(bytes('true'.encode('gbk')))
        # return

#进行匿名设置
def root(label,nikename,khd:socket.socket):
    try:
        if nikename in client_dict:
            # 用户名存在则发出警告
            khd.send(bytes('false'.encode('gbk')))
            #print('用户名重复')
            return False
        # 否则创建将键值对加入到client_dict中，即生成匿名用户
        else:
            name[label] = nikename
            khd.send(bytes('true'.encode('gbk')))
            welcome = f'\n欢迎用户##{nikename}##加入聊天室\n'
            brodcast(welcome.encode('gbk'))
            client_dict[nikename] = khd
            #print(client_dict)
            return True
    except:
        #khd_socket.send(bytes('false'.encode('gbk')))
        return  False

if __name__ == '__main__':

    #服务器主函数，进行tcp连接和端口绑定
    tcp = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    tcp.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,True)
    #进行端口绑定
    tcp.bind(("",8080))
    loadData()
    print(f'服务器已开启，正在等待用户进入...')
    #
    label = 0
    tcp.listen(127)
    while True:
        try:
            khd_socket, ip = tcp.accept()
            print(f'{ip}连接成功!')
            #khd_socket.send('欢迎加入聊天室，输入昵称开始聊天\n'.encode('gbk'))
            khd_thread = Thread(target=process,args=(khd_socket,label,))
            khd_thread.daemon = True
            khd_thread.start()
            label+=1
        except:
            print('服务器端断开连接')
    tcp.close()
