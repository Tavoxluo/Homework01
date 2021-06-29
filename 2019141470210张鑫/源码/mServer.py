import socket
import threading
import sqlite3
import random
import configparser

# init database
from time import sleep


def init_database():
    # connect to the database
    database = sqlite3.connect('data.db')
    c = database.cursor()
    # create a table to store uer information, the primary key is id
    c.execute('''
            create table if not exists user_info( date timestamp not null default (datetime('now','localtime')),
            user_name text,
            user_id int(5) not null,
            password varchar(10) ,
            primary key (user_id))
            ''')
    # create a table to store the friendship-connection
    c.execute('''
            create table if not exists user_friends(holder_id int(5),
            holder_name text,
            friend_id int(5),
            friend_name text)
            ''')
    # create a table to store the cheating history, the primary key is the date
    c.execute('''
            create table if not exists history
            (date timestamp not null default (datetime('now','localtime')),
            sender_id int(5),
            receiver_id int(5),message text(1024),
            primary key(date,sender_id,receiver_id))
            ''')
    # create a table to store the information of the current users
    # flush the table

    c.execute('''
            drop table if exists states
            ''')
    c.execute('''
            create table if not exists states
            (id int(5),
            state int(1),
             address text,
             primary key(id)
             )
            ''')
    database.commit()
    database.close()


# warning to the sender
def send_msg(addr, msg:str,header = 'sendt'):
    connection = get_key(address_dict,addr)
    msg = header + msg
    print(':',msg)
    connection.send(msg.encode())


def broadcast(addr,msg:str):
    try:
        d = sqlite3.connect('data.db')
        id = client_dict[addr]
        sql = 'select user_name from user_info where user_id = ' + id
        name = d.execute(sql).fetchone()
        msg = str(name[0])+':'+msg[5:]
        print(name[0])
        for address in client_dict:
            send_msg(address,msg)
    except:
        print('error!')
        send_msg(address,'error!')
    finally:
        d.close()


# 显示所有在线用户的函数
def show_online(addr):
    d = sqlite3.connect('data.db')
    msg = ''
    ids = []
    print(client_dict)
    for ad in client_dict:
        key = client_dict[ad]
        ids.append(key)
    for id in ids:
        print(id)
        sql = 'select user_name from user_info where user_id = ' + id
        name = str(d.execute(sql).fetchone()[0])

        while len(name) < 5:
            name+= ' '

        msg+= str(name) + str(id)
    print(msg)
    send_msg(addr,msg,'shonl')


# register, check out the account if legal return successful, else return failure.
def register(addr,msg:str):
    try:
        d = sqlite3.connect('data.db')
        u_name = msg[0:5]
        u_password = msg[5:]
        sql = 'select user_id from user_info'
        id_exist = d.execute(sql).fetchall()

        u_id = random.randint(10000,99999)
        # find a not distinct id
        while u_id in id_exist:
            u_id = random.randint(10000, 99999)

        sql = "insert into user_info(user_name,user_id,password) values (?,?,?)"
        v = (u_name,u_id,u_password)
        d.execute(sql,v)
        d.commit()
        print('register successfully!',
              'id =',u_id,
              'name = ',u_name,
              'password = ',u_password)
        # conn.send

        send_msg(addr,'register successfully,id ='+str(u_id))

    except sqlite3.DatabaseError:
        print('register fail!')
        # conn.send
        send_msg(addr,'register fail,database error')
    except:
        send_msg(addr,'register fail,unknown error')
    finally:
        d.close()


# 登录函数，消息的前五个字符为帐号，后面为密码
def login(addr,msg:str) :
    try:
        d =sqlite3.connect('data.db')
        u_id = (msg[0:5])
        u_password = msg[5:]
        sql = 'select password from user_info where user_id  = '
        password = str(d.execute(sql+u_id).fetchone()[0])
        print('user id entered:',u_id)
        print('password entered:',u_password)
        print('password wanted:',password)
        if u_password == password:
            sql = 'select id from states'
            id_list = d.execute(sql).fetchall()
            if (int(u_id),) in id_list:
                print('!!!!!!!!!!!!!!!!!!!')
                sql = 'update states set state = 1 where id = '+u_id
                d.execute(sql)
            else:
                sql = 'insert into states values (?,?,?)'
                v = (u_id,1,str(addr))
                d.execute(sql,v)
            d.commit()

            print('successfully sign in!')
            send_msg(addr, '~login successfully!')
            # add to the dict
            client_dict[addr] = u_id
        else:
            print('failed to login')
            send_msg(addr, '~login failed, please check out ur account and password!')
    except sqlite3.DatabaseError as e:
        print('!!!!!!!!!!!database failed!')
        print(e)
        send_msg(addr, 'fail to login! ur enter is illegal')
    except:
        send_msg(addr,'fail to login! ur enter is illegal')
    finally:
        d.close()


# sign out
def sign_out(addr):
    try:
        d = sqlite3.connect('data.db')
        id = client_dict[addr]
        sql = 'update states set state = 0 where id = ' + id
        d.execute(sql)
        d.commit()
        print('!sign out:',id)

        send_msg(addr,'sign out successfully!')
    except sqlite3.DatabaseError as e:
        print('database error',e)
        send_msg(addr,'error')
    finally:
        d.close()


# get the cheating history, and send it to the receiver
def check_history(addr,msg:str):
   try:
    d = sqlite3.connect('data.db')
    send_id = client_dict[addr]
    recv_id = msg[0:5]

    sql = 'select user_name from user_info where user_id = ' + send_id
    send_name = d.execute(sql).fetchone()
    sql = 'select user_name from user_info where user_id = ' + recv_id
    recv_name = d.execute(sql).fetchone()
    sql = 'select date,sender_id,message from history where (sender_id = ' + send_id + ' and receiver_id = ' + recv_id + ') ' + 'or (sender_id = ' + recv_id + ' and receiver_id = ' + send_id + ')'

    out = d.execute(sql)
    text = out.fetchone()
    while text:
        sleep(0.1)
        if str(text[1]) == str(send_id):
            message = str(text[0]) + ' ' + str(send_name[0]) + ': ' + str(text[2])
            print(message)
            send_msg(addr, message)
        if str(text[1]) == str(recv_id):
            message = str(text[0]) + ' ' + str(recv_name[0]) + ': ' + str(text[2])
            print(message)
            send_msg(addr, message)
        text = out.fetchone()
   except:
       send_msg(addr,'error!!!!')
   finally:
       d.close()


# delete history
def delete_history(addr, msg:str):
    try:
        d = sqlite3.connect('data.db')
        send_name =msg[0:5]
        date = msg[5:]
        sql = 'select user_id from user_info where user_name = '+ '\''+str(send_name).rstrip()+'\''
        send_id = d.execute(sql).fetchone()[0]

        print(send_id)
        sql = 'delete  from history where date = '+'\'' + str(date) +'\'' +' and sender_id = '+str(send_id)
        d.execute(sql)
        d.commit()
        print('delete successfully')
        send_msg(addr,'delete successfully')
    except IOError as e:
        print('database error',e)
        send_msg(addr,'delete fail!')
    finally:
        d.close()


# add friends
def add_friend(addr, msg:str):
    try:
        d = sqlite3.connect('data.db')
        holder_id = msg[0:5]
        friend_id = msg[5:10]
        sql = 'select user_name from user_info where user_id ='+holder_id
        holder_name = d.execute(sql).fetchone()[0]
        sql = 'select user_name from user_info where user_id ='+friend_id
        friend_name = d.execute(sql).fetchone()[0]
        print(friend_name)
        sql = 'insert into user_friends values(?,?,?,?)'
        v = (holder_id,holder_name,friend_id,friend_name)
        d.execute(sql,v)
        v = (friend_id,friend_name,holder_id,holder_name)
        d.execute(sql,v)
        d.commit()
        print('add friend successfully!!')

        send_msg(addr, '~add friend successfully!')
    except sqlite3.DatabaseError as e:
        print('database error!',e)
        send_msg(addr, '~add friend failed')
    except:
        send_msg(addr,'~no such id!',header='adder')
    finally:
        d.close()


def delete_friend(addr, msg:str):
    try:
        d = sqlite3.connect('data.db')
        holder_id = msg[0:5]
        friend_id = msg[5:10]
        sql = 'delete from user_friends where (holder_id ='+holder_id+' and friend_id = '+ friend_id+') '+'or (holder_id = '+friend_id +' and friend_id = '+holder_id+')'
        d.execute(sql)
        d.commit()
        print('delete successfully!!!')
        send_msg(addr,'delete successfully!!!')
    except sqlite3.DatabaseError as e:
        print('database error!',e)
        send_msg(addr,'error')
    except:
        send_msg(addr,'erro')
    finally:
        d.close()


# this method used to send the message to the specify receiver
# addr is the address of the sender
# msg format:sender_id(5)+receiver_id(5)+message_to_send(1024)
def send_to(addr, msg:str):
    try:
        d = sqlite3.connect('data.db')
        sender_id = msg[0:5]
        receiver_id = msg[5:10]
        sql = 'select state from states where id = '+receiver_id
        state = d.execute(sql).fetchone()
        # if the receiver is not online, fail to send
        if  not state or ((0,) in state):
            print('~fail to send to',receiver_id,'because not exist or not online! ')
            send_msg(addr,'sorry! the receiver not exist or not online!')
            return
        sql = 'select user_name from user_info where user_id = '
        sender_name = d.execute(sql+sender_id).fetchone()
        sender_addr = get_key(client_dict,sender_id)
        receiver_addr = get_key(client_dict,receiver_id)
        print('sender, addr:',sender_id,sender_addr)
        print('receiver, addr:',receiver_id,receiver_addr)
        message_to_send = str(sender_name)[2:len(sender_name)-4]+':'+msg[10:]
        # insert into the database
        sql = 'insert into history (sender_id,receiver_id,message) values(?,?,?)'
        v = (sender_id,receiver_id,msg[10:])
        d.execute(sql,v)
        d.commit()
        # 提醒用户查收消息
        send_msg(receiver_addr,str(sender_id),'highl')

        for ad in (receiver_addr,sender_addr):
            send_msg(ad,message_to_send)
    except sqlite3.DatabaseError as e :
        print('database error',e)
        send_msg(addr,'error!')
    finally:
        d.close()


def change_name(addr, msg:str):
    try:
        d = sqlite3.connect('data.db')
        id = msg[0:5]
        name = msg[5:]
        sql = 'update  user_info set user_name = '+'\''+name+'\''+' where user_id = '+id
        d.execute(sql)
        sql = 'update user_friends set holder_name = '+'\''+name+'\''+'where holder_id = '+ id
        d.execute(sql)
        sql = 'update user_friends set friend_name = '+'\''+name+'\''+'where friend_id = '+ id
        d.execute(sql)
        d.commit()
        print('update name successfully!')
        send_msg('ur name has been changed!')
        send_msg('hi! '+name)

    except sqlite3.DatabaseError as e:
        print('database fail',e)
    finally:
        d.close()


def change_password(addr,msg:str):
    try:
        d = sqlite3.connect('data.db')
        id = msg[0:5]
        new_password = msg[5:]
        sql = 'update user_info set password = '+'\''+new_password+'\''+'where user_id = '+id
        d.execute(sql)
        d.commit()
        print('successfully changed password!')
        send_msg(addr, '~successfully changed password!')
    except sqlite3.DatabaseError as e:
        print('database error',e)
        send_msg(addr, '~failed to change password!')
    finally:
        d.close()


# get the name  of a specify id
def get_name(id:int):
    try:
        d = sqlite3.connect('data.db')
        sql = 'select user_name from user_info where user_id = '+id
        name = d.execute(sql).fetchone()
        return name
    except sqlite3.DatabaseError as e:
        print('error',e)
    finally:
        d.close()


# 展示好友列表
def show_friends(addr,msg):
    try:
        id = msg
        d =sqlite3.connect('data.db')
        sql = 'select friend_name, friend_id from user_friends where holder_id = '+str(id)
        friends = d.execute(sql).fetchall()
        for friend in friends:
            print(friend)
            friend = str(friend[1])+' '+str(friend[0])
            send_msg(addr,friend,'frien')
            sleep(0.1)
    except:
        print('error!')
        send_msg(addr,'error!')


# distinguish the kind of  request by the first five character
def get_request(addr, msg:str):
    header = msg[0:5]
    print('header',header)
    message = msg[5:]
    print('message:',message)
    # login
    if header == 'login':
        print('~request:login')
        login(addr,message)
    # sign out
    if header == 'signo':
        print('~request:signo')
        sign_out(addr)
    # register
    if header == 'regis':
        print('~request:register')
        register(addr,message)
    # delete friend
    if header == 'delfr':
        print('~request:delete friend')
        delete_friend(addr, message)
    # add friend
    if header == 'addfr':
        print('~request:add friend')
        add_friend(addr, message)
    # send to
    if header == 'sendt':
        print('~request:send message')
        send_to(addr, message)
    # check history
    if header == 'chehs':
        print('~request:check history')
        check_history(addr,message)
    # delete history
    if header == 'delhs':
        print('~request:delete history')
        delete_history(addr, message)
    # change name
    if header == 'chana':
        print('~change name')
        change_name(addr, message)
    # broadcast to everyone
    if header == 'broad':
        print('~broadcast to everyone')
        broadcast(addr, message)
    # change password
    if header == 'chapa':
        print('~change password')
        change_password(addr,message)
    # show friends
    if header == 'shofr':
        print('~show friends')
        show_friends(addr,message)
    # show online users
    if header == 'shonl':
        print('~show online users')
        show_online(addr)


# get the key from a dict where its values is value
def get_key(dictionary: dict, value):
    print('~~get key~~')
    for d in dictionary:
        if dictionary[d] == value:
            return d
    return ''


# Build the connection between the client and the server
def build_connect(connection, address_port):
    try:
        while True:
            msg = connection.recv(1024).decode()
            if len(msg)<= 0:
                raise Exception
            if msg != '':
                get_request(address_port, msg)
                print('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')
    except:
        print(connection,address_port,client_dict[address_port],'has quit!')
        print('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')
        # 从字典中移除
        address_dict.pop(connection)
        client_dict.pop(address_port)


if __name__ == '__main__':
    conf = configparser.ConfigParser()
    conf.read('server.ini')
    host = conf.get('address','host')
    port = int(conf.get('address','port'))
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((host, port))
    # address : id
    client_dict = {}
    # connection : address
    address_dict = {}
    # the max listen number
    maxListen = 10
    s.listen(maxListen)

    print('the server is on!')
    init_database()
    while True:
        # continue to accepting the connection from the clients
        conn, address = s.accept()
        address_dict[conn] = address
        print('~',address, 'connected!')
        threading.Thread(target=build_connect, args=(conn, address)).start()




