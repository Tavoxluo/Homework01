from PyQt5 import QtWidgets
import UI_1
import socket
import threading
import sys 
import stopThreading

class TCPLogic(UI_1.ToolsUi):
    def __init__(self, num):
        super(TCPLogic,self).__init__(num)
        self.tcp_socket = None
        self.server_th = None
        self.client_th = None
        self.client_socket_list = list()

        self.link = False

    def tcp_server_start(self):
        self.tcp_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.tcp_socket.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
        self.tcp_socket.setblocking(False)
        try:
            port = int(self.lineEdit_port.text())
            self.tcp_socket.bind(('',port))
        except Exception as ret:
            msg = '请检查端口号\n'
            self.signal_write_msg.emit(msg)
        else:
            self.tcp_socket.listen()
            self.server_th = threading.Thread(target = self.tcp_server_concurency)
            self.server_th.start()
            msg = 'TCP服务正在监听端口:%s\n' % str(port)
            self.signal_write_msg.emit(msg)
    
    def tcp_server_concurency(self):
        while True:
            try:
                client_socket,client_address = self.tcp_socket.accept()
            except Exception as ret:
                pass
            else:
                client_socket.setblocking(False)
                self.client_socket_list.append((client_socket,client_address))
                msg = 'TCP服务端已连接IP:%s端口:%s\n' % client_address
                self.signal_write_msg.emit(msg)
            for client,address in self.client_socket_list:
                try:
                    recv_msg = client.recv(1024)
                except Exception as ret:
                    pass
                else:
                    if recv_msg:
                        msg = recv_msg.decode('utf-8')
                        msg = '来自IP:{}端口:{}:\n{}\n'.format(address[0],address[1],msg)
                        self.signal_write_msg.emit(msg)
                    else:
                        self.tcp_socket.close()
                        self.reset()
                        mag = '从服务器断开连接\n'
                        self.signal_write_msg.emit(msg)
                        break
                

    def tcp_client_start(self):
        self.tcp_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        try:
            address = (str(self.lineEdit_ip_send.text()),int(self.lineEdit_port.text()))
        except Exception as ret:
            msg = '请检查目标IP，目标端口\n'
            self.signal_write_msg.emit(msg)
        else:
            try:
                msg = '正在连接目标服务器\n'
                self.signal_write_msg.emit(msg)
                self.tcp_socket.connect(address)
            except Exception as ret:
                msg = '无法连接服务器\n'
                self.signal_write_msg.emit(msg)
            else:
                self.client_th = threading.Thread(target=self.tcp_client_concurency,args=(address,))
                self.client_th.start()
                msg = 'TCP客户端已连接IP:{}%s端口:%s\n' % address
                self.signal_write_msg.emit(msg)


    def tcp_client_concurency(self,address):
        while True:
            recv_msg = self.tcp_socket.recv(1024)
            if recv_msg:
                msg = recv_msg.decode('utf-8')
                msg = '来自IP:{}端口:{}:\n{}\n'.format(address[0],address[1],msg)
                self.signal_write_msg.emit(msg)
            else:
                self.tcp_socket.close()
                self.reset()
                msg = '从服务器断开连接\n'
                self.signal_write_msg.emit(msg)
                break

    def tcp_send(self):
        if self.link is False:
             msg = '请选择服务，并点击连接网络\n'
             self.signal_write_msg.emit(msg)
        else:
            try:
                send_msg = (str(self.textEdit_send.toPlainText())).encode('utf-8')
                if self.comboBox_tcp.currentIndex() == 0:
                    for client,address in self.client_socket_list:
                        client.send(send_msg)
                    msg = 'TCP服务端已发送\n'
                    self.signal_write_msg.emit(msg)
                if self.comboBox_tcp.currentIndex == 1:
                    self.tcp_socket.send(send_msg)
                    msg = 'TCP客户端已发送\n'
                    self.signal_write_msg.emit(msg)
            except Exception as ret:
                msg = '发送失败\n'
                self.signal_write_msg.emit(msg)

            

        

    def tcp_close(self):

        if self.comboBox_tcp.currentIndex == 0:
            try:
                for client,address in self.client_socket_list:
                    client.close()
                if self.link is True:
                    msg = '已断开网络\n'
                    self.signal_write_msg.emit(msg)
            except Exception as ret:
                pass

        if self.comboBox_tcp.currentIndex == 1:
            try:
                self.tcp_socket.close()
                if self.link is True:
                    msg = '已断开网络连接\n'
                    self.signal_write_msg.emit(msg)
            except Exception as ret:
                pass

        try:
            stopThreading.stop_thread(self.server_th)
        except Exception:
            pass

        try:
            stopThreading.stop_thread(self.client_th)
        except Exception:
            pass

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    ui = TCPLogic(1)
    ui.show()
    sys.exit(app.exec_())

    