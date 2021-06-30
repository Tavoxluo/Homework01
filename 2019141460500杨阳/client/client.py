import os
import datetime
import sys
import threading
from threading import Thread
from time import strftime, localtime, time

from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication, QMessageBox, QTableWidgetItem

from chat_UI import Ui_Form
from client_sock import ClientSocket
from config import *
from request_protocol import RequestProtocol
from log_UI import Example
from record_UI import Ui_MainWindow


class Client(object):

    def __init__(self):
        self.ischat = False
        self.delmember = ''
        self.member = {}
        self.username = ''
        self.nickname = ''
        self.ismanage = False
        self.running = True
        self.conn = ClientSocket()
        # Thread(target=self.response_handle).start()
        self.chat = Ui_Form()

        self.user_msg = Ui_MainWindow()
        self.user_msg.delete_2.clicked.connect(self.delete_1)
        self.user_msg.shuaxin.clicked.connect(self.update_)
        self.user_msg.sousuo.clicked.connect(self.search)
        self.user_msg.yonghuxinxi.clicked.connect(self.check_to_user)
        self.user_msg.pushButton.clicked.connect(self.check_to_msg)
        self.user_msg.nicheng.clicked.connect(self.edit_nickname)
        self.user_msg.nichengshuru.returnPressed.connect(self.edit_nickname)
        self.user_msg.mima.clicked.connect(self.edit_password)
        self.user_msg.xinmima.returnPressed.connect(self.edit_password)
        self.user_msg.zhuxiao.clicked.connect(self.zhuxiao)

        self.chat.pushButton_2.clicked.connect(self.clsBtn)
        self.chat.pushButton_4.clicked.connect(self.clsBtn)
        self.chat.pushButton.clicked.connect(self.sendmsg)
        self.chat.pushButton_5.clicked.connect(self.openmsg)

        self.chat.textEdit.textChanged.connect(self.text_changed)
        self.chat.textBrowser_6.textChanged.connect(self.deleme)

        self.log = Example()
        self.log.lineEdit_2.returnPressed.connect(self.sendata)
        self.log.login.clicked.connect(self.sendata)
        self.log.pushButton.clicked.connect(self.clsBtn1)
        self.log.buttonGroup.buttonClicked.connect(self.handleButtonClicked)
        self.log.textBrowser_6.textChanged.connect(self.deleme2)
        self.log.textBrowser_7.textChanged.connect(self.deleme3)
        Thread(target=self.response_handle).start()
        print('初始化完成')
        # 创建套接字

    def zhuxiao(self):
        choice = QMessageBox.question(
            self.user_msg,
            '确认',
            '确定要注销这个账号吗？')

        if choice == QMessageBox.Yes:
            msg = RequestProtocol.request_member_delete(self.username)
            self.conn.send_data(msg)
        if choice == QMessageBox.No:
            pass

    def handleButtonClicked(self):
        text = self.log.buttonGroup.checkedButton().text()
        if text == '登录':
            self.log.lineEdit.setPlaceholderText("        账号")
            self.log.login.setText("登录")
        elif text == '注册':
            self.log.lineEdit.setPlaceholderText("        昵称")
            self.log.login.setText("注册")

    def edit_password(self):

        # 修改密码
        old_password = self.user_msg.yuanmima.text()
        new_password = self.user_msg.xinmima.text()
        password = old_password + DELIMITER + new_password
        send_data = RequestProtocol.request_edit('password', password, self.username)
        self.conn.send_data(send_data)

    def edit_nickname(self):

        # 修改昵称
        nickname = self.user_msg.nichengshuru.text()
        send_data = RequestProtocol.request_edit('nickname', nickname, self.username)
        self.conn.send_data(send_data)

    def check_to_msg(self):
        self.user_msg.shuaxin.show()
        self.user_msg.msg.show()
        self.user_msg.delete_2.show()
        self.user_msg.dateTimeEdit.show()
        self.user_msg.dateTimeEdit1.show()
        self.user_msg.comboBox.show()
        self.user_msg.sousuo.show()
        self.user_msg.lineEdit.show()
        self.user_msg.label.show()
        self.user_msg.mima.hide()
        self.user_msg.user.hide()
        self.user_msg.nicheng.hide()
        self.user_msg.label_2.hide()
        self.user_msg.label_3.hide()
        self.user_msg.zhuxiao.hide()
        self.user_msg.xinmima.hide()
        self.user_msg.yuanmima.hide()
        self.user_msg.nichengshuru.hide()

    def check_to_user(self):
        self.user_msg.shuaxin.hide()
        self.user_msg.msg.hide()
        self.user_msg.delete_2.hide()
        self.user_msg.dateTimeEdit.hide()
        self.user_msg.dateTimeEdit1.hide()
        self.user_msg.comboBox.hide()
        self.user_msg.sousuo.hide()
        self.user_msg.lineEdit.hide()
        self.user_msg.label.hide()
        self.user_msg.mima.show()
        self.user_msg.user.show()
        self.user_msg.nicheng.show()
        self.user_msg.label_2.show()
        self.user_msg.label_3.show()
        self.user_msg.zhuxiao.show()
        self.user_msg.xinmima.show()
        self.user_msg.yuanmima.show()
        self.user_msg.nichengshuru.show()
        self.update_2()

    def search(self):

        # 搜索
        method = self.user_msg.comboBox.currentText()
        if method == '全部':
            user = method
            pass
        else:
            lens = len(method)
            start = 0
            for index in range(lens):
                if method[index] == '(':
                    start = index
            start = start + 1
            a = method[start:-1]
            user = str(a)
        print(user)
        start_time = self.user_msg.dateTimeEdit1.dateTime()
        start_time1 = start_time.toString("yyyy-MM-dd hh:mm")
        end_time = self.user_msg.dateTimeEdit.dateTime()
        end_time1 = end_time.toString("yyyy-MM-dd hh:mm")
        msg = self.user_msg.lineEdit.text()
        send = RequestProtocol.request_search(user, start_time1, end_time1, msg)
        self.conn.send_data(send)

    def delete_1(self):
        currentrow = self.user_msg.msg.currentRow()
        print(currentrow)
        if currentrow < 0:
            QMessageBox.critical(
                self.user_msg,
                '错误',
                '请选中要删除的记录！')
            return
        if self.ismanage:
            id = self.user_msg.msg.item(currentrow, 4).text()
            choice = QMessageBox.question(
                self.user_msg,
                '确认',
                '确定要删除该条记录吗？')
            if choice == QMessageBox.Yes:
                send_msg = RequestProtocol.request_delete(id)
                self.conn.send_data(send_msg)
                # sql = "DELETE FROM msg WHERE id = %s" % id
                # self.db.delete_one(sql)
            if choice == QMessageBox.No:
                pass
        else:
            username = self.user_msg.msg.item(currentrow, 0).text()
            if username != self.username:
                QMessageBox.critical(
                    self.user_msg,
                    '错误',
                    '不能删除其他用户的消息记录！')
                return
            send_time_str = self.user_msg.msg.item(currentrow, 2).text()
            send_time = datetime.datetime.strptime(send_time_str, "%Y-%m-%d %H:%M:%S")
            now_time = strftime('%Y-%m-%d %H:%M:%S', localtime(time()))
            send_time += datetime.timedelta(minutes=2)
            if str(send_time) < str(now_time):
                QMessageBox.critical(
                    self.user_msg,
                    '错误',
                    '超过两分钟不能删除！')
                return
            id = self.user_msg.msg.item(currentrow, 4).text()
            print(username)
            print(self.username)
            choice = QMessageBox.question(
                self.user_msg,
                '确认',
                '确定要删除该条记录吗？')

            if choice == QMessageBox.Yes:
                send_msg = RequestProtocol.request_delete(id)
                self.conn.send_data(send_msg)
                # sql = "DELETE FROM msg WHERE id = %s" % id
                # self.db.delete_one(sql)
            if choice == QMessageBox.No:
                pass

    def update_(self):
        self.conn.send_data(REQUEST_CHAT_MSG)

    def update_2(self):
        self.conn.send_data(REQUEST_MEMBER_MSG)

    def openmsg(self):
        self.user_msg.show()
        self.update_()

    def deleme2(self):
        self.log.close()
        self.chat.show()
        print('显示成功')

    def deleme3(self):
        self.log.close()
        self.user_msg.yonghuxinxi.hide()
        self.user_msg.pushButton.hide()
        self.user_msg.show()
        self.update_()

    def deleme(self):
        del self.member[self.delmember]
        print(self.member)
        self.chat.textBrowser_5.clear()
        for u_name, info in self.member.items():
            print(u_name)
            self.chat.textBrowser_5.append(info + '(' + u_name + ')')

    def text_changed(self):
        msg = self.chat.textEdit.toPlainText()  # 首先在这里拿到文本框内容
        if '\n' in msg:
            # 做一个判断，textedit默认按回车换行，本质是在后面加了一个\n，那我们判断换行的根据就是判断\n是否在我那本框中，如果在，OK，那下一步
            msg = msg.replace('\n', '')  # 将文本框的\n清除掉
            self.chat.textEdit.setText(msg)  # 将处理后的内容重新放入文本框
            self.sendmsg()

    def clsBtn(self):
        self.running = False
        self.chat.close()
        os._exit(0)

    def clsBtn1(self):
        self.running = False
        self.log.close()
        os._exit(0)

    def sendmsg(self):
        send_time = strftime('%Y-%m-%d %H:%M:%S', localtime(time()))
        msg = self.chat.textEdit.toPlainText().strip()
        send_msg = RequestProtocol.request_chat(self.username, msg)
        print('123')
        self.conn.send_data(send_msg)
        self.chat.textEdit.clear()
        self.chat.textBrowser_4.append('我' + '  ' + send_time)
        self.chat.textBrowser_4.append(' ' + msg)
        self.chat.textBrowser_4.ensureCursorVisible()

    def sendata(self):
        text = self.log.buttonGroup.checkedButton().text()
        if text == '登录':
            username = self.log.lineEdit.text().strip()
            password = self.log.lineEdit_2.text().strip()
            log = RequestProtocol.request_login_result(username, password)
            self.conn.send_data(log)

        elif text == '注册':
            nickname = self.log.lineEdit.text().strip()
            password = self.log.lineEdit_2.text().strip()
            register = RequestProtocol.request_register(nickname, password)
            self.conn.send_data(register)

    def sendlog(self):
        username = self.username
        nickname = self.nickname
        msg = RequestProtocol.request_member(username, nickname)
        self.conn.send_data(msg)

    def response_handle(self):
        while self.running:
            recv_data = self.conn.recv_data()
            print('接收消息' + recv_data)
            response_data_list = recv_data.split(DELIMITER)
            response_data = dict()
            response_data['response_id'] = response_data_list[0]

            if response_data['response_id'] == RESPONSE_LOGIN_RESULT:
                response_data['result'] = response_data_list[1]
                response_data['nickname'] = response_data_list[2]
                response_data['username'] = response_data_list[3]
                print(response_data)
                if response_data['result'] == '0':
                    print("登陆失败")
                    self.log.label1.show()
                    self.log.lineEdit.clear()
                    self.log.lineEdit_2.clear()
                    timer = threading.Timer(3, self.fun_timer1)
                    timer.start()

                elif response_data['result'] == '2':
                    print('已登录')
                    self.log.label2.show()
                    self.log.lineEdit.clear()
                    self.log.lineEdit_2.clear()
                    timer = threading.Timer(3, self.fun_timer2)
                    timer.start()

                elif response_data['result'] == '1':
                    print(response_data['nickname'] + '登陆成功')
                    self.username = response_data['username']
                    print(self.username)
                    self.nickname = response_data['nickname']
                    self.log.textBrowser_6.append('|')
                    self.sendlog()

                elif response_data['result'] == '3':
                    print(response_data['nickname'] + '登陆成功')
                    self.ismanage = True
                    self.log.textBrowser_7.append('|')


            elif response_data['response_id'] == RESPONSE_CHAT:
                response_data['nickname'] = response_data_list[1]
                response_data['message'] = response_data_list[2]
                send_time = strftime('%Y-%m-%d %H:%M:%S', localtime(time()))
                self.chat.textBrowser_4.append(response_data['nickname'] + '  ' + send_time)
                self.chat.textBrowser_4.append(' ' + response_data['message'])
                self.chat.textBrowser_4.ensureCursorVisible()

            elif response_data['response_id'] == REQUEST_MEMBER:
                response_data_member_list = recv_data.split('@')
                print(response_data_member_list)
                for a in response_data_member_list:
                    if a == '':
                        break
                    response_member_list = a.split(DELIMITER)
                    self.member[response_member_list[2]] = response_member_list[1]
                    self.chat.textBrowser_5.append(response_member_list[1] + '(' + response_member_list[2] + ')')
                    a = self.chat.textBrowser_5.toPlainText()
                    print(a)

            elif response_data['response_id'] == RESPONSE_DELMEMBER:
                # print('1')
                # response_data['nickname'] = response_data_list[1]
                # response_data['username'] = response_data_list[2]
                # print(self.member)
                # del self.member[response_data['username']]
                # print(self.member)
                # self.chat.textBrowser_4.clear()
                # # self.chat.textBrowser_5.clear()
                # # for u_name, info in self.member.items():
                # #     self.chat.textBrowser_5.append(info + '(' + u_name + ')')
                # print('12333')
                self.chat.textBrowser_6.append('|')
                self.delmember = response_data_list[2]

            elif response_data['response_id'] == RESPONSE_MSG:
                # print(response_data_list[1])
                self.set_msg(response_data_list[1])
                print(response_data_list[2])
                userlist_result = eval(response_data_list[2])
                userlist = len(userlist_result)
                self.user_msg.comboBox.clear()
                self.user_msg.comboBox.addItem('全部')
                for i in range(userlist):
                    user = str(userlist_result[i][1]) + '(' + str(userlist_result[i][0]) + ')'
                    self.user_msg.comboBox.addItem(user)
                self.user_msg.comboBox.setCurrentIndex(0)

            elif response_data['response_id'] == RESPONSE_DELMSG:
                print('删除完成')
                self.update_()

            elif response_data['response_id'] == RESPONSE_MSG_SEARCH:
                self.set_msg(response_data_list[1])

            elif response_data['response_id'] == RESPONSE_MEMBER_MSG:
                self.set_member_msg(response_data_list[1])

            elif response_data['response_id'] == RESPONSE_MEMBER_EDIT:
                if response_data_list[1] == '2':
                    print('修改成功')
                    self.user_msg.label_4.show()
                    timer = threading.Timer(3, self.fun_timer_5)
                    timer.start()

                    self.update_2()
                elif response_data_list[1] == '0':
                    print('原密码错误')
                    self.user_msg.label_5.setText("密码错误")
                    self.user_msg.label_5.show()
                    timer = threading.Timer(3, self.fun_timer_6)
                    timer.start()

                elif response_data_list[1] == '1':
                    print('修改成功')
                    self.user_msg.label_5.setText("修改成功")
                    self.user_msg.label_5.show()
                    timer = threading.Timer(3, self.fun_timer_6)
                    timer.start()

            elif response_data['response_id'] == RESPONSE_MEMBER_REGISTER:
                print(response_data_list[1])
                text = "-注册成功！您的账号为：" + response_data_list[1] + "-"
                print(text)
                self.log.label3.setText(text)
                self.log.label3.show()
                self.log.lineEdit.clear()
                self.log.lineEdit_2.clear()
                timer = threading.Timer(3, self.fun_timer4)
                timer.start()

    def fun_timer_5(self):
        self.user_msg.label_4.hide()

    def fun_timer_6(self):
        self.user_msg.label_5.hide()

    def fun_timer4(self):
        self.log.label3.hide()

    def set_member_msg(self, str1):
        result = eval(str1)
        row = len(result)
        self.user_msg.user.setRowCount(row)
        self.user_msg.user.clearContents()
        for i in range(row):
            for j in range(2):
                temp_data = result[i][j]
                data = QTableWidgetItem(str(temp_data))
                self.user_msg.user.setItem(i, j, data)

    def set_msg(self, str1):
        result = eval(str1)
        row = len(result)
        self.user_msg.msg.setRowCount(row)
        self.user_msg.msg.clearContents()
        for i in range(row):
            for j in range(5):
                temp_data = result[i][j]
                data = QTableWidgetItem(str(temp_data))
                self.user_msg.msg.setItem(i, j, data)

    def fun_timer1(self):
        self.log.label1.hide()

    def fun_timer2(self):
        self.log.label2.hide()

    def fun_timer3(self):
        pass

    def check(self):
        self.log.close()
        self.chat.show()
        print('显示成功')
        # timer = threading.Timer(0.5, self.fun_timer3)
        # timer.start()
        # print('123')


if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setWindowIcon(QIcon('登录1.png'))
    ex = Client()
    sys.exit(app.exec_())
