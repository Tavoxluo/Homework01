from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import Qt, QPoint
from PyQt5.QtGui import QCursor, QMouseEvent
from PyQt5.QtWidgets import QWidget, QApplication, QMainWindow
from client_sock import ClientSocket
from request_protocol import RequestProtocol
from config import *
import sys


class Example(QMainWindow):
    _startPos = None
    _endPos = None
    _isTracking = False

    def __init__(self):
        super().__init__()
        self._initUI()

    def _initUI(self):
        self.setFixedSize(QSize(600, 359))
        self.setWindowFlags(Qt.FramelessWindowHint)  # 无边框
        self.setStyleSheet("background-color: rgb(247,245,241);")

        self.label1 = QLabel(self)
        self.label1.setGeometry(QtCore.QRect(420, 110, 190, 31))
        self.label1.setStyleSheet("font: 9pt \"楷体\"; color: red;")
        self.label1.setObjectName("label")
        self.label1.setText('-账号或密码不正确-')
        self.label1.hide()

        self.label2 = QLabel(self)
        self.label2.setGeometry(QtCore.QRect(440, 110, 190, 31))
        self.label2.setStyleSheet("font: 9pt \"楷体\"; color: red;")
        self.label2.setObjectName("label")
        self.label2.setText('-该账号已登录-')
        self.label2.hide()

        self.label3 = QLabel(self)
        self.label3.setGeometry(QtCore.QRect(380, 110, 220, 31))
        self.label3.setStyleSheet("font: 9pt \"楷体\"; color: red;")
        self.label3.setObjectName("label")
        self.label3.setText('--')
        self.label3.hide()

        self.label = QLabel(self)
        self.label.setGeometry(QtCore.QRect(430, 60, 131, 31))
        self.label.setStyleSheet("font: 10pt \"楷体\";")
        self.label.setObjectName("label")
        self.graphicsView_3 = QGraphicsView(self)
        self.graphicsView_3.setGeometry(QtCore.QRect(-10, 0, 371, 361))
        self.graphicsView_3.setStyleSheet("border-image: url(./img.png);")
        self.graphicsView_3.setObjectName("graphicsView_3")

        self.graphicsView = QGraphicsView(self)
        self.graphicsView.setGeometry(QtCore.QRect(370, 133, 31, 31))
        self.graphicsView.setStyleSheet("border-image:url(./登录.png);")
        self.graphicsView.setObjectName("graphicsView")

        self.lineEdit = QLineEdit(self)
        self.lineEdit.setGeometry(QtCore.QRect(410, 133, 171, 31))
        self.lineEdit.setStyleSheet("QLineEdit\n"
                                    "{\n"
                                    "border-radius: 15px;  border: 2px groove gray;\n"
                                    "border-style: outset;\n"
                                    "}")
        self.lineEdit.setText("")
        self.lineEdit.setMaxLength(30)
        self.lineEdit.setObjectName("lineEdit")
        self.textBrowser_6 = QtWidgets.QTextBrowser(self)
        self.textBrowser_6.setGeometry(QtCore.QRect(0, 0, 531, 391))
        self.textBrowser_6.setStyleSheet("background-color: rgb(255, 255, 255);font: 10pt \"Arial\";")
        self.textBrowser_6.setObjectName("textBrowser_6")
        self.textBrowser_6.hide()
        self.textBrowser_7 = QtWidgets.QTextBrowser(self)
        self.textBrowser_7.setGeometry(QtCore.QRect(0, 0, 531, 391))
        self.textBrowser_7.setStyleSheet("")
        self.textBrowser_7.setObjectName("textBrowser_6")
        self.textBrowser_7.hide()
        self.graphicsView_2 = QGraphicsView(self)
        self.graphicsView_2.setGeometry(QtCore.QRect(370, 193, 31, 31))
        self.graphicsView_2.setStyleSheet("border-image: url(./密码.png);")
        self.graphicsView_2.setObjectName("graphicsView_2")
        self.pushButton = QPushButton(self)
        self.pushButton.setGeometry(QtCore.QRect(550, 20, 24, 24))
        self.pushButton.setStyleSheet("image: url(./关闭.png);""border:none;")
        self.pushButton.setText("")
        self.pushButton.setObjectName("pushButton")
        self.pushButton_2 = QPushButton(self)
        self.pushButton_2.setGeometry(QtCore.QRect(510, 20, 24, 24))
        self.pushButton_2.setStyleSheet("image: url(./最小化.png);""border:none;")
        self.pushButton_2.setText("")
        self.pushButton_2.setObjectName("pushButton_2")
        self.pushButton_2.clicked.connect(lambda: self.minBtn())
        self.lineEdit_2 = QLineEdit(self)
        self.lineEdit_2.setGeometry(QtCore.QRect(410, 193, 171, 31))
        self.lineEdit_2.setStyleSheet("QLineEdit\n"
                                      "{\n"
                                      "border-radius: 15px;  border: 2px groove gray;\n"
                                      "border-style: outset;\n"
                                      "}")
        self.lineEdit_2.setText("")
        self.lineEdit_2.setMaxLength(30)
        self.lineEdit_2.setEchoMode(QtWidgets.QLineEdit.Password)
        self.lineEdit_2.setObjectName("lineEdit_2")
        self.lineEdit_2.setPlaceholderText("        密码")
        self.lineEdit.setPlaceholderText("        账号")
        self.login = QPushButton(self)
        self.login.setGeometry(QtCore.QRect(440, 250, 101, 31))
        self.login.setMouseTracking(False)
        self.login.setStyleSheet("QPushButton\n"
                                 "{\n"
                                 "background-color: rgb(50,98,246);\n"
                                 "color: white;\n"
                                 "border-radius: 15px;  border: 2px groove gray;\n"
                                 "border-style: outset;\n"
                                 "}")
        icon = QtGui.QIcon.fromTheme("登录")
        self.login.setIcon(icon)
        self.login.setAutoExclusive(False)
        self.login.setObjectName("login")
        self.login.setText("登录")
        self.denglu = QtWidgets.QRadioButton(self)
        self.denglu.setGeometry(QtCore.QRect(410, 90, 115, 19))
        self.denglu.setObjectName("denglu")
        self.zhuce = QtWidgets.QRadioButton(self)
        self.zhuce.setGeometry(QtCore.QRect(500, 90, 115, 19))
        self.zhuce.setObjectName("zhuce")
        self.setWindowTitle('Absolute')
        self.denglu.setText("登录")
        self.denglu.setChecked(True)
        self.zhuce.setText("注册")
        self.buttonGroup = QtWidgets.QButtonGroup(self)
        self.buttonGroup.setObjectName("buttonGroup")
        self.buttonGroup.addButton(self.zhuce)
        self.buttonGroup.addButton(self.denglu)
        self.buttonGroup.buttonClicked.connect(lambda :self.handleButtonClicked())
        self.show()

    def handleButtonClicked(self):
        print(self.buttonGroup.checkedButton().text())

    def mouseMoveEvent(self, e: QMouseEvent):  # 重写移动事件
        self._endPos = e.pos() - self._startPos
        self.move(self.pos() + self._endPos)

    def mousePressEvent(self, e: QMouseEvent):
        if e.button() == Qt.LeftButton:
            self._isTracking = True
            self._startPos = QPoint(e.x(), e.y())

    def mouseReleaseEvent(self, e: QMouseEvent):
        if e.button() == Qt.LeftButton:
            self._isTracking = False
            self._startPos = None
            self._endPos = None

    def check(self):
        self.lineEdit_2.close()
        self.lineEdit.close()
        self.pushButton.close()
        self.pushButton_2.close()
        self.login.close()
        self.graphicsView.close()
        self.graphicsView_2.close()
        self.graphicsView_3.close()
        self.label.close()
        self.setGeometry(100, 100, 700, 700)
        self.label1.show()

    def minBtn(self):
        self.showMinimized()


    def log(self):
        username = self.lineEdit.text()
        password = self.lineEdit_2.text()
        print(username, password)
        log = RequestProtocol.request_login_result(username, password)
        self.conn.send_data(log)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())