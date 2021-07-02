from PyQt5 import QtWidgets,QtCore,QtGui
from PyQt5.QtWidgets import QApplication,QDialog,QHBoxLayout,QVBoxLayout
import sys

class ToolsUi(QDialog):

    signal_write_msg = QtCore.pyqtSignal(str)

    def __init__(self,num):
        super(ToolsUi,self).__init__()
        self.num = num
        self._translate = QtCore.QCoreApplication.translate

        self.setObjectName("TCP-UDP")
        self.resize(640,480)
        self.setAcceptDrops(False)
        self.setSizeGripEnabled(False)

        self.pushButton_get_ip = QtWidgets.QPushButton()
        self.pushButton_link = QtWidgets.QPushButton()
        self.pushButton_unlink = QtWidgets.QPushButton()
        self.pushButton_clear = QtWidgets.QPushButton()
        self.pushButton_exit = QtWidgets.QPushButton()
        self.pushButton_send = QtWidgets.QPushButton()
        self.pushButton_dir = QtWidgets.QPushButton()
        self.pushButton_else = QtWidgets.QPushButton()
        self.label_port = QtWidgets.QLabel()
        self.label_ip = QtWidgets.QLabel()
        self.label_rev = QtWidgets.QLabel()
        self.label_send = QtWidgets.QLabel()
        self.label_sendto = QtWidgets.QLabel()
        self.label_dir = QtWidgets.QLabel()
        self.label_written = QtWidgets.QLabel()
        self.lineEdit_port = QtWidgets.QLineEdit()
        self.lineEdit_ip_send = QtWidgets.QLineEdit()
        self.lineEdit_ip_local = QtWidgets.QLineEdit()
        self.textEdit_send = QtWidgets.QTextEdit()
        self.textBrowser_recv = QtWidgets.QTextBrowser()
        self.comboBox_tcp = QtWidgets.QComboBox()

        self.h_box_1 = QHBoxLayout()
        self.h_box_2 = QHBoxLayout()
        self.h_box_3 = QHBoxLayout()
        self.h_box_4 = QHBoxLayout()
        self.h_box_recv = QHBoxLayout()
        self.h_box_exit = QHBoxLayout()
        self.h_box_all = QHBoxLayout()
        self.v_box_set = QVBoxLayout()
        self.v_box_send = QVBoxLayout()
        self.v_box_web = QVBoxLayout()
        self.v_box_exit = QVBoxLayout()
        self.v_box_right = QVBoxLayout()
        self.v_box_left = QVBoxLayout()

        self.comboBox_tcp.addItem("")
        self.comboBox_tcp.addItem("")
        self.comboBox_tcp.addItem("")
        self.comboBox_tcp.addItem("")
        self.comboBox_tcp.addItem("")

        font = QtGui.QFont()
        font.setFamily("Yuppy TC")
        font.setPointSize(20)
        font.setBold(True)
        font.setItalic(False)
        font.setUnderline(True)
        font.setWeight(75)
        font.setStrikeOut(False)
        self.label_rev.setFont(font)
        self.label_send.setFont(font)

        self.label_dir.hide()
        self.label_sendto.hide()
        self.pushButton_dir.hide()
        self.lineEdit_ip_send.hide()
        self.label_dir.setWordWrap(True)
        self.pushButton_unlink.setEnabled(False)
        self.textBrowser_recv.insertPlainText("这是窗口-%s\n" % self.num)

        self.layout_ui()
        self.ui_translate()
        self.connect()



    def layout_ui(self):
        self.h_box_1.addWidget(self.label_ip)
        self.h_box_1.addWidget(self.lineEdit_ip_local)
        self.h_box_1.addWidget(self.pushButton_get_ip)
        self.h_box_2.addWidget(self.label_port)
        self.h_box_2.addWidget(self.lineEdit_port)
        self.h_box_2.addWidget(self.pushButton_else)
        self.h_box_3.addWidget(self.label_sendto)
        self.h_box_3.addWidget(self.lineEdit_ip_send)
        self.h_box_4.addWidget(self.comboBox_tcp)
        self.h_box_4.addWidget(self.pushButton_link)
        self.h_box_4.addWidget(self.pushButton_unlink)
        self.v_box_set.addLayout(self.h_box_1)
        self.v_box_set.addLayout(self.h_box_2)
        self.v_box_set.addLayout(self.h_box_3)
        self.v_box_set.addLayout(self.h_box_4)
        self.v_box_web.addWidget(self.label_dir)
        self.v_box_web.addWidget(self.pushButton_dir)
        self.v_box_send.addWidget(self.label_send)
        self.v_box_send.addWidget(self.textEdit_send)
        self.v_box_send.addLayout(self.v_box_web)
        self.v_box_exit.addWidget(self.pushButton_send)
        self.v_box_exit.addWidget(self.pushButton_exit)
        self.h_box_exit.addWidget(self.label_written)
        self.h_box_exit.addLayout(self.v_box_exit)
        self.v_box_left.addLayout(self.v_box_set)
        self.v_box_left.addLayout(self.v_box_send)
        self.v_box_left.addLayout(self.h_box_exit)

        # 右侧布局添加
        self.h_box_recv.addWidget(self.label_rev)
        self.h_box_recv.addWidget(self.pushButton_clear)
        self.v_box_right.addLayout(self.h_box_recv)
        self.v_box_right.addWidget(self.textBrowser_recv)

        # 将左右布局添加到窗体布局
        self.h_box_all.addLayout(self.v_box_left)
        self.h_box_all.addLayout(self.v_box_right)

        # 设置窗体布局到窗体
        self.setLayout(self.h_box_all)


    def ui_translate(self):
        self.setWindowTitle(self._translate("TCP-UDP", "TCP/UDP网络测试工具-窗口%s" % self.num))
        self.comboBox_tcp.setItemText(0, self._translate("TCP-UDP", "TCP服务端"))
        self.comboBox_tcp.setItemText(1, self._translate("TCP-UDP", "TCP客户端"))
        self.comboBox_tcp.setItemText(2, self._translate("TCP-UDP", "UDP服务端"))
        self.comboBox_tcp.setItemText(3, self._translate("TCP-UDP", "UDP客户端"))
        self.pushButton_link.setText(self._translate("TCP-UDP", "连接网络"))
        self.pushButton_unlink.setText(self._translate("TCP-UDP", "断开网络"))
        self.pushButton_get_ip.setText(self._translate("TCP-UDP", "重新获取IP"))
        self.pushButton_clear.setText(self._translate("TCP-UDP", "清除消息"))
        self.pushButton_send.setText(self._translate("TCP-UDP", "发送"))
        self.pushButton_exit.setText(self._translate("TCP-UDP", "退出系统"))
        self.pushButton_else.setText(self._translate("TCP-UDP", "窗口多开another"))
        self.label_ip.setText(self._translate("TCP-UDP", "本机IP:"))
        self.label_port.setText(self._translate("TCP-UDP", "端口号:"))
        self.label_sendto.setText(self._translate("TCP-UDP", "目标IP:"))
        self.label_rev.setText(self._translate("TCP-UDP", "接收区域"))
        self.label_send.setText(self._translate("TCP-UDP", "发送区域"))
        self.label_written.setText(self._translate("TCP-UDP", "Written by LSL"))

    def connect(self):
        self.signal_write_msg.connect(self.write_msg)
        self.comboBox_tcp.currentIndexChanged.connect(self.combobox_change)

    def combobox_change(self):
        self.close_all()
        if self.comboBox_tcp.currentIndex() == 0 or self.comboBox_tcp.currentIndex() == 2:
            self.label_sendto.hide()
            self.label_dir.hide()
            self.pushButton_dir.hide()
            self.pushButton_send.show()
            self.lineEdit_ip_send.hide()
            self.textEdit_send.show()
            self.label_port.setText(self._translate("TCP-UDP", "端口号:"))

        if self.comboBox_tcp.currentIndex() == 1 or self.comboBox_tcp.currentIndex() == 3:
            self.label_sendto.show()
            self.label_dir.hide()
            self.pushButton_dir.hide()
            self.pushButton_send.show()
            self.lineEdit_ip_send.show()
            self.textEdit_send.show()
            self.label_port.setText(self._translate("TCP-UDP", "目标端口:"))



    def write_msg(self,msg):
        self.textBrowser_recv.insertPlainText(msg)
        self.textBrowser_recv.moveCursor(QtGui.QTextCursor.End)

    def closeEvent(self,event):
        self.close_all()

    def close_all(self):
        pass
    

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ui = ToolsUi(1)
    ui.show()
    sys.exit(app.exec_())

    



