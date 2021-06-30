import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import Qt, QPoint
from PyQt5.QtGui import QCursor, QMouseEvent
from PyQt5.QtWidgets import QWidget, QApplication, QMainWindow

class Ui_Form(QMainWindow):
    _startPos = None
    _endPos = None
    _isTracking = False

    def __init__(self):
        super().__init__()
        self.setupUi()

    def setupUi(self):
        self.setFixedSize(QSize(780, 579))
        self.setWindowFlags(Qt.FramelessWindowHint)  # 无边框
        self.setStyleSheet("background-color: rgb(232, 232, 232);")

        self.textBrowser_4 = QtWidgets.QTextBrowser(self)
        self.textBrowser_4.setGeometry(QtCore.QRect(0, 40, 531, 391))
        self.textBrowser_4.setStyleSheet("background-color: rgb(255, 255, 255);font: 10pt \"Arial\";")
        self.textBrowser_4.setObjectName("textBrowser_4")
        self.textBrowser_6 = QtWidgets.QTextBrowser(self)
        self.textBrowser_6.setGeometry(QtCore.QRect(0, 0, 531, 391))
        self.textBrowser_6.setStyleSheet("background-color: rgb(255, 255, 255);font: 10pt \"Arial\";")
        self.textBrowser_6.setObjectName("textBrowser_6")
        self.textBrowser_6.hide()
        self.textBrowser_5 = QtWidgets.QTextBrowser(self)
        self.textBrowser_5.setGeometry(QtCore.QRect(530, 120, 250, 459))
        self.textBrowser_5.setStyleSheet("background-color: rgb(255, 255, 255);font: 10pt \"Arial\";")
        self.textBrowser_5.setObjectName("textBrowser_5")
        self.pushButton = QtWidgets.QPushButton(self)
        self.pushButton.setGeometry(QtCore.QRect(420, 530, 81, 31))
        self.pushButton.setStyleSheet('''QPushButton{background:rgb(18,183,245);border-radius:4px;color:#ffffff;}
        QPushButton:hover{background:rgb(71,200,248);border-radius:4px;color:#ffffff}''')
        self.pushButton.setObjectName("pushButton")
        self.pushButton_2 = QtWidgets.QPushButton(self)
        self.pushButton_2.setGeometry(QtCore.QRect(320, 530, 81, 31))
        self.pushButton_2.setStyleSheet('''QPushButton{background:rgb(238, 238, 238);border-radius:4px;}
        QPushButton:hover{background:rgb(217, 217, 217);border-radius:4px;}''')
        self.pushButton_2.setObjectName("pushButton_2")
        self.textBrowser = QtWidgets.QTextBrowser(self)
        self.textBrowser.setGeometry(QtCore.QRect(0, 420, 531, 161))
        self.textBrowser.setStyleSheet("background-color: rgb(255, 255, 255);border-color:rgb(235,235,235);")
        self.textBrowser.setObjectName("textBrowser")
        self.textBrowser_2 = QtWidgets.QTextBrowser(self)
        self.textBrowser_2.setGeometry(QtCore.QRect(530, 40, 256, 541))
        self.textBrowser_2.setStyleSheet("background-color: rgb(255, 255, 255);border-color:rgb(235,235,235);")
        self.textBrowser_2.setObjectName("textBrowser_2")
        self.label = QtWidgets.QLabel(self)
        self.label.setGeometry(QtCore.QRect(540, 50, 111, 21))
        self.label.setStyleSheet("background-color: rgb(255, 255, 255);\n"
                                 "font: 11pt \"黑体\";")
        self.label.setObjectName("label")
        self.textEdit = QtWidgets.QTextEdit(self)
        self.textEdit.setGeometry(QtCore.QRect(20, 440, 511, 81))
        self.textEdit.setStyleSheet("background-color: rgb(255, 255, 255);font: 11pt \"等线\";\n"
                                    "border:0px;")
        self.textEdit.setObjectName("textEdit")
        self.label_2 = QtWidgets.QLabel(self)
        self.label_2.setGeometry(QtCore.QRect(0, 0, 781, 41))
        self.label_2.setStyleSheet("background-color: rgb(58, 167, 253);\n"
                                   "background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:0, stop:0 rgba(76,140,254, 255), stop:1 rgba(31,210,255, 255));")
        self.label_2.setText("")
        self.label_2.setObjectName("label_2")
        self.lineEdit = QtWidgets.QLineEdit(self)
        self.lineEdit.setGeometry(QtCore.QRect(570, 80, 201, 21))
        self.lineEdit.setStyleSheet("background-color: rgb(255, 255, 255); border-color:rgba(235,235,235,0.1);")
        self.lineEdit.setObjectName("lineEdit")
        self.graphicsView = QtWidgets.QGraphicsView(self)
        self.graphicsView.setGeometry(QtCore.QRect(540, 80, 16, 16))
        self.graphicsView.setStyleSheet("background-image: url(:/搜索.png);\n"
                                        "background-color: rgb(255, 255, 255);\n"
                                        "border:0px")
        self.graphicsView.setObjectName("graphicsView")
        self.pushButton_3 = QtWidgets.QPushButton(self)
        self.pushButton_3.setGeometry(QtCore.QRect(700, 1, 38, 38))

        self.pushButton_3.setStyleSheet('''QPushButton{image: url(./最小化1.png);background-color: rgb(35,203,255);border:0px;}
        QPushButton:hover{image: url(./最小化1.png);background-color: rgb(79,217,255);border:0px;}''')
        self.pushButton_3.setText("")
        self.pushButton_3.setObjectName("pushButton_3")
        self.pushButton_3.clicked.connect(lambda: self.minBtn())
        self.pushButton_4 = QtWidgets.QPushButton(self)
        self.pushButton_4.setGeometry(QtCore.QRect(740, 1, 38, 38))
        self.pushButton_4.setStyleSheet('''QPushButton{image: url(./关闭1.png);background-color: rgb(35,203,255);border:0px;}
        QPushButton:hover{image: url(./关闭1.png);background-color: rgb(254,84,57);border:0px;}''')
        self.pushButton_5 = QtWidgets.QPushButton(self)
        self.pushButton_5.setGeometry(QtCore.QRect(490, 385, 31, 31))
        self.pushButton_5.setStyleSheet('''QPushButton{background-image: url(./时钟.png);background-color: rgb(255, 255, 255);border: 0px;}
        QPushButton:hover{background-image: url(./时钟.png);background-color: rgb(220, 220, 220);border: 0px;}''')
        self.pushButton_5.setText("")
        self.pushButton_5.setObjectName("pushButton_5")
        self.label_2.raise_()
        self.pushButton_4.setText("")
        self.pushButton_4.setObjectName("pushButton_4")
        self.textBrowser.raise_()
        self.pushButton.raise_()
        self.pushButton_2.raise_()
        self.textBrowser_2.raise_()
        self.label.raise_()
        self.textEdit.raise_()
        self.lineEdit.raise_()
        self.graphicsView.raise_()
        self.pushButton_3.raise_()
        self.pushButton_4.raise_()
        self.textBrowser_5.raise_()
        self.pushButton_5.raise_()
        self.retranslateUi()
        self.hide()

    def retranslateUi(self):
        _translate = QtCore.QCoreApplication.translate
        self.pushButton.setText("发送")
        self.pushButton_2.setText("关闭")
        self.label.setText("群成员")
        self.lineEdit.setPlaceholderText("搜索成员")
        self.lineEdit.hide()

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


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Ui_Form()
    sys.exit(app.exec_())
