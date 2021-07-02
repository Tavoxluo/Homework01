from PyQt5 import QtWidgets
import UDP_1,TCP_1
import socket
import sys

class MainWindow(UDP_1.UDPLogic,TCP_1.TCPLogic):
    def __init__(self, num):
        super(MainWindow,self).__init__(num)
        self.client_socket_list = list()
        self.another = None
        self.link = False
        self.click_get_ip()

    def connect(self,):
        super(MainWindow,self).connect()
        self.pushButton_link.clicked.connect(self.click_link)
        self.pushButton_unlink.clicked.connect(self.click_unlink)
        self.pushButton_get_ip.clicked.connect(self.click_get_ip)
        self.pushButton_clear.clicked.connect(self.click_clear)
        self.pushButton_send.clicked.connect(self.send)
        self.pushButton_dir.clicked.connect(self.click_dir)
        self.pushButton_exit.clicked.connect(self.close)
        self.pushButton_else.clicked.connect(self.another_windows)

    def click_link(self):
        if self.comboBox_tcp.currentIndex() == 0:
            self.tcp_server_start()
        if self.comboBox_tcp.currentIndex() == 1:
            self.tcp_client_start()
        if self.comboBox_tcp.currentIndex() == 2:
            self.udp_server_start()
        if self.comboBox_tcp.currentIndex() == 3:
            self.udp_client_start()
        self.link = True
        self.pushButton_unlink.setEnabled(True)
        self.pushButton_link.setEnabled(False)

    def click_unlink(self):
        self.close_all()
        self.link = False
        self.pushButton_unlink.setEnabled(False)
        self.pushButton_link.setEnabled(True)

    def click_get_ip(self):
        self.lineEdit_ip_local.clear()
        my_addr = socket.gethostbyname(socket.gethostname())
        self.lineEdit_ip_local.setText(str(my_addr))

    def send(self):
        if self.comboBox_tcp.currentIndex() == 0 or self.comboBox_tcp.currentIndex() == 1:
            self.tcp_send()
        if self.comboBox_tcp.currentIndex() == 2 or self.comboBox_tcp.currentIndex() == 3:
            self.udp_send()

    def click_clear(self):
        self.textBrowser_recv.clear()

    def click_dir(self):
        self.web_get_dir()

    def close_all(self):
        if self.comboBox_tcp.currentIndex() == 0 or self.comboBox_tcp.currentIndex() == 1:
            self.tcp_close()
        if self.comboBox_tcp.currentIndex() == 2 or self.comboBox_tcp.currentIndex() == 3:
            self.udp_close()

    def reset(self):
        self.link = False
        self.client_socket_list = list()
        self.pushButton_unlink.setEnabled(False)
        self.pushButton_link.setEnabled(True)

    def another_windows(self):
        QtWidgets.QMessageBox.warning(self,'hhh','xxx',QtWidgets.QMessageBox.Yes)
        self.num = self.num + 1
        self.another = MainWindow(self.num)
        self.another.show()

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    ui = MainWindow(1)
    ui.show()
    sys.exit(app.exec_())
