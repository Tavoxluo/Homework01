# -*- coding: utf-8 -*-

# 写信模块

import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QFileDialog, QWidget
from UIEditor import TextEditor
from emailSender import *
from re import compile
from threading import Thread
from PyQt5.QtCore import Qt


class emailWriter(object):
    def __init__(self, content=None, tmail=None, subject=None):
        self.file = []
        self.uploadfile = []
        self.filepath = {}
        self.filecount = 0
        self.texteditor = TextEditor()

        self.subject = subject
        self.to = tmail
        self.content = content
        self.fmail = ''
        self.password = ''
        self.sender = 'SCUer'
        self.reciever = 'reciever'
        self.pathlist = list(self.filepath.values())
        self.edcan = None

        self.sendfunc2 = None
        self.sendfailfunc = None

    def setupUi(self, Form):
        # 创建写信界面
        Form.setObjectName("Form")
        Form.resize(1004, 709)
        Form.setWindowIcon(QtGui.QIcon('img/logo.png'))  # 设置窗口图标
        # 设置窗口背景图片
        self.backpath = 'img/background.jpg'
        window_pale = QtGui.QPalette()
        window_pale.setBrush(Form.backgroundRole(), QtGui.QBrush(QtGui.QPixmap(self.backpath)))
        Form.setPalette(window_pale)
        Form.setWindowOpacity(0.98)
        self.gridLayout_2 = QtWidgets.QGridLayout(Form)
        self.gridLayout_2.setObjectName("gridLayout_2")

        self.ReceiverLayout = QtWidgets.QHBoxLayout()
        self.ReceiverLayout.setObjectName("ReceiverLayout")
        self.Receiver_label = QtWidgets.QLabel(Form)
        self.Receiver_label.setObjectName("Receiver_label")
        self.ReceiverLayout.addWidget(self.Receiver_label)
        self.Receiver_edit = QtWidgets.QLineEdit(Form)
        self.Receiver_edit.setObjectName("Receiver_edit")
        self.ReceiverLayout.addWidget(self.Receiver_edit)

        self.SenderLayout = QtWidgets.QHBoxLayout()
        self.SenderLayout.setObjectName("SenderLayout")
        self.Sender_label = QtWidgets.QLabel(Form)
        self.Sender_label.setObjectName("Sender_label")
        self.SenderLayout.addWidget(self.Sender_label)
        self.Sender_edit = QtWidgets.QLineEdit(Form)
        self.Sender_edit.setObjectName('Sender_edit')
        self.SenderLayout.addWidget(self.Sender_edit)

        self.SenderNameLayout = QtWidgets.QHBoxLayout()
        self.SenderNameLayout.setObjectName("SenderNameLayout")
        self.SenderName_label = QtWidgets.QLabel(Form)
        self.SenderName_label.setObjectName("SenderName_label")
        self.SenderNameLayout.addWidget(self.SenderName_label)
        self.SenderName_edit = QtWidgets.QLineEdit(Form)
        self.SenderName_edit.setObjectName('SenderName_edit')
        self.SenderNameLayout.addWidget(self.SenderName_edit)

        self.PassWordLayout = QtWidgets.QHBoxLayout()
        self.PassWordLayout.setObjectName("PassWordLayout")
        self.PassWord_label = QtWidgets.QLabel(Form)
        self.PassWord_label.setObjectName("PassWord_label")
        self.PassWordLayout.addWidget(self.PassWord_label)
        self.PassWord_edit = QtWidgets.QLineEdit(Form)
        self.PassWord_edit.setObjectName('PassWord_edit')
        self.PassWord_edit.setEchoMode(QtWidgets.QLineEdit.Password)
        self.PassWordLayout.addWidget(self.PassWord_edit)

        self.gridLayout_2.addLayout(self.PassWordLayout, 0, 2, 1, 1)
        self.gridLayout_2.addLayout(self.SenderNameLayout, 0, 0, 1, 1)
        self.gridLayout_2.addLayout(self.SenderLayout, 0, 1, 1, 1)
        self.gridLayout_2.addLayout(self.ReceiverLayout, 0, 3, 1, 1)

        self.SubjectLayout = QtWidgets.QHBoxLayout()
        self.SubjectLayout.setObjectName("SubjectLayout")
        self.Subject_label = QtWidgets.QLabel(Form)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.Subject_label.sizePolicy().hasHeightForWidth())
        self.Subject_label.setSizePolicy(sizePolicy)
        self.Subject_label.setObjectName("Subject_label")
        self.SubjectLayout.addWidget(self.Subject_label)
        self.Subject_edit = QtWidgets.QLineEdit(Form)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.Subject_edit.sizePolicy().hasHeightForWidth())
        self.Subject_edit.setSizePolicy(sizePolicy)
        self.Subject_edit.setObjectName("Subject_edit")
        self.SubjectLayout.addWidget(self.Subject_edit)
        self.gridLayout_2.addLayout(self.SubjectLayout, 1, 0, 1, 4)
        self.Text_label = QtWidgets.QLabel(Form)
        self.Text_label.setObjectName("Text_label")
        self.gridLayout_2.addWidget(self.Text_label, 2, 0, 1, 1)

        self.Writing = QtWidgets.QMdiArea()
        self.Writing.setObjectName("Writing")
        self.edcan = QtWidgets.QWidget()
        self.texteditor.setupUi(self.edcan)
        subwindow = self.Writing.addSubWindow(self.edcan)
        subwindow.setWindowFlags(Qt.FramelessWindowHint)
        self.edcan.showMaximized()
        self.gridLayout_2.addWidget(self.Writing, 2, 0, 2, 4)

        spacerItem = QtWidgets.QSpacerItem(20, 178, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout_2.addItem(spacerItem, 3, 0, 1, 1)
        self.filepart = QtWidgets.QHBoxLayout()
        self.filepart.setObjectName("FilelLayout")
        self.File_label = QtWidgets.QLabel(Form)
        self.File_label.setMaximumSize(QtCore.QSize(16777215, 30))
        self.File_label.setObjectName("File_label")
        self.filepart.addWidget(self.File_label)
        self.bappendfile = QtWidgets.QPushButton(Form)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.bappendfile.sizePolicy().hasHeightForWidth())
        self.bappendfile.setSizePolicy(sizePolicy)
        self.bappendfile.setMaximumSize(QtCore.QSize(100, 30))
        self.bappendfile.setObjectName("bappendfile")
        self.bappendfile.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.bappendfile.clicked.connect(self.bappendfileClicked)
        self.filepart.addWidget(self.bappendfile)
        self.gridLayout_2.addLayout(self.filepart, 4, 1, 1, 3)
        self.line = QtWidgets.QFrame(Form)
        self.line.setFrameShape(QtWidgets.QFrame.HLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.gridLayout_2.addWidget(self.line, 5, 1, 1, 3)
        self.filepart = QtWidgets.QHBoxLayout()
        self.filepart.setObjectName("FilesLayout")
        self.gridLayout_2.addLayout(self.filepart, 4, 2, 2, 1)
        self.SendLayout = QtWidgets.QHBoxLayout()
        self.SendLayout.setObjectName("SendLayout")
        self.bsend = QtWidgets.QPushButton(Form)
        self.bsend.setMaximumSize(QtCore.QSize(100, 30))
        self.bsend.setObjectName("Send_button")
        self.bsend.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.bsend.clicked.connect(self.bsendClicked)
        self.SendLayout.addWidget(self.bsend)
        self.gridLayout_2.addLayout(self.SendLayout, 7, 3, 2, 1)
        spacerItem2 = QtWidgets.QSpacerItem(240, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout_2.addItem(spacerItem2, 8, 3, 1, 1)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)
        self.File_label.setText('')

        if self.sender:
            self.SenderName_edit.setText(self.sender)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "MailClient"))
        self.Receiver_label.setText(_translate("Form", "收件人:"))
        self.Sender_label.setText(_translate("Form", "发件人:"))
        self.SenderName_label.setText(_translate("Form", "发件人名称:"))
        self.PassWord_label.setText(_translate("Form", "授权码:"))
        self.Subject_label.setText(_translate("Form", "主题:  "))
        self.Text_label.setText(_translate("Form", "正文"))
        self.File_label.setText(_translate("Form", "附件"))
        self.bappendfile.setText(_translate("Form", "添加附件"))
        self.bsend.setText(_translate("Form", "发送"))

    def bappendfileClicked(self):
        # 添加附件的类型
        filetype = "All Files (*);;Text Files (*.txt);;Jpeg (*.jpg);;Png (*.png);;Doc Files(*.doc);;Pdf Files(*.pdf)"
        msgBox = QtWidgets.QWidget()
        files, ok1 = QFileDialog.getOpenFileNames(msgBox, "多文件选择", "C:/", filetype)
        for path in files:
            self.bappendfileClickedOne(path)

    def bappendfileClickedOne(self, path):
        # 选择需要发送的附件
        path = path
        name = path.split('/')[-1]
        try:
            fp = open(path, 'rb')
            fp.close()
        except:
            try:
                fp = open(path + '\\' + name, 'rb')
                path = path + '\\' + name
                fp.close()
            except:
                msgBox = QtWidgets.QMessageBox()
                msgBox.setWindowIcon(QtGui.QIcon('img/logo.ico'))
                msgBox.setWindowTitle('添加附件')
                msgBox.setText('该附件不存在')
                msgBox.exec()
                return
        self.addFileButton(name, path)
        self.showFileButton()
        self.File_label.setText('附件')

    def addFileButton(self, filename, filepath):
        if filename not in self.filepath.keys():
            self.file.append(QtWidgets.QPushButton())
            self.file[-1].setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
            self.file[-1].setFlat(True)
            self.file[-1].setObjectName("file" + str(len(self.file)))
            self.file[-1].setText(filename)
            self.file[-1].setCheckable(True)
            self.file[-1].setChecked(True)
            self.filepath[filename] = filepath
            self.uploadfile.append(filename)
            self.file[-1].toggled.connect(self.fileButtonPress)
            self.filecount += 1

    def fileButtonPress(self):
        # 添加附件Button被点击，就选择自己想发送的附件
        for fb in self.file:
            if fb.isChecked():
                if fb.text() in self.uploadfile:
                    pass
                else:
                    self.uploadfile.append(fb.text())
            else:
                try:
                    fb.close()
                    self.uploadfile.remove(fb.text())
                    self.filepath.pop(fb.text())
                    self.filecount -= 1
                except:
                    pass
                try:
                    self.file.remove(fb)
                except:
                    pass
        if self.uploadfile == []:
            self.File_label.setText('')

    def showFileButton(self):
        # 将添加的附加以Button形式显示在下方
        layout = QtWidgets.QGridLayout()
        layout.setSizeConstraint(QtWidgets.QLayout.SetFixedSize)
        n = 0
        m = 0
        maxbutton = 10 if len(self.file) < 20 else 20
        for fb in self.file:
            layout.addWidget(fb, m, n)
            n += 1
            if n % maxbutton == 0:
                m += 1
                n = 0
        self.filepart.addLayout(layout)

    def bsendClicked(self):
        self.subject = self.Subject_edit.text()
        self.to = self.Receiver_edit.text()
        self.fmail = self.Sender_edit.text()
        self.sender = self.SenderName_edit.text()
        self.password = self.PassWord_edit.text()
        if self.fmail == '':
            self.caution(text='记得填写收件人    ')
            return
        if self.to == '':
            self.caution(text='记得填写收件人    ')
            return
        if self.to[-1] != ';':
            self.to += ';'
        self.content = self.texteditor.textEdit.toHtml()
        delp = """<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.0//EN" "http://www.w3.org/TR/REC-html40/strict.dtd">"""
        reps = """<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" 
        "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">"""
        self.content = self.content.replace(delp, reps)
        self.pathlist = list(self.filepath.values())
        email_regex = compile(r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)")
        if not email_regex.findall(self.fmail):
            self.caution(text='发件人邮箱格式不正确呢  ')
            return
        for tmail in self.to.split(';'):
            if tmail == '':
                continue
            if not email_regex.findall(tmail):
                self.caution(text='收件人邮箱格式不正确呢  ')
                return
        tmail_list = self.to.split(';')
        tmail_list.pop(-1)
        msg = createEmail(self.subject, self.content, self.fmail, self.sender, tmail_list, self.pathlist)
        sendthread = SendEmailThread(self.fmail, self.password, tmail_list, msg)
        sendthread.finfunc = self.sendfunc2
        sendthread.failfunc = self.sendfailfunc
        success = sendthread.run()
        self.caution(title='稍等', text='邮件正在发送...    ')
        if not success:
            self.caution(title='抱歉', text='邮件发送失败，原因可能是\n①网络连接断开\n②发件账户或密码错误（点击设置可以修改）\n③该账户未开通SMTP服务')

    def click(self, button, i):
        button.clicked.connect(lambda: self.shows(i))

    def doubleclick(self, button, i):
        button.doubleclick = lambda: self.oneshow(i)

    def caution(self, title='啊哦', text='稍等'):
        msgBox = QtWidgets.QMessageBox(QtWidgets.QMessageBox.NoIcon, title, text)
        msgBox.setWindowIcon(QtGui.QIcon('img/logo.ico'))
        msgBox.setWindowFlags(QtCore.Qt.SubWindow)
        msgBox.setWindowOpacity(0.8)
        msgBox.exec()


class SendEmailThread(Thread):
    def __init__(self, fmail, password, tmail_list, msg, finfunc=None, failfunc=None):
        super().__init__()
        self.fmail = fmail
        self.password = password
        self.tmail_list = tmail_list
        self.msg = msg

        self.finfunc = finfunc
        self.failfunc = failfunc

    def run(self):
        mailstate = sendEmailSMTP(self.fmail, self.password, self.tmail_list, self.msg)
        if '失败' in mailstate:
            if self.failfunc:
                self.failfunc()
            return False
        else:
            if self.finfunc:
                self.finfunc()
            return True
