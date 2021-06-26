from flask import Flask, request, redirect, url_for, render_template, jsonify  # ,abort,Response,session
import pymysql
from datetime import datetime
import re
import configparser

# 创建Flask实例
app = Flask(__name__)


class ControlSQL(object):
    # 构造方法
    def __init__(self, conn):
        self.conn = conn
        self.cur = conn.cursor()

    # 登录信息记录
    def logon_record(self, logkind, user_id, user_ip):
        self.log_record_id = int(datetime.today().microsecond)
        sql = "call insert_log_record(%d,'%s','%s','%s');" % (self.log_record_id, logkind, user_id, user_ip)
        self.cur.execute(sql)

    # 检查账户正确性
    def check_account(self, username, password):
        username_new = str(username)
        password_new = str(password)
        select_sqli = "select acc_power from web_account where username='%s' and web_password='%s';" % (
            username_new,
            password_new,
        )
        # print(select_sqli)
        self.cur.execute(select_sqli)
        try:
            res_count = self.cur.fetchone()[0]
            return res_count
        except Exception as e:
            # print(e)
            return None

    # 关联银行卡
    def connect(self, username, bank_card_id, card_password):
        username = str(username)
        bank_card_id = str(bank_card_id)
        card_password = str(card_password)
        sql = "call connect_web_bank('%s','%s','%s',@x);" % (username, bank_card_id, card_password)
        # print(sql)
        self.cur.execute(sql)
        sql2 = "select @x;"
        self.cur.execute(sql2)
        res_count = self.cur.fetchone()
        return res_count

    # 解除关联
    def deconnect(self, username):
        self.oper_record_id = int(datetime.today().microsecond)
        sql = "call deconnect_web_bank(%d,'%s',@x);" % (self.oper_record_id, username)
        sql2 = "select @x;"
        self.cur.execute(sql)
        self.cur.execute(sql2)
        status = self.cur.fetchone()[0]
        if status is None:
            return False
        else:
            return True

    # 把money从source_id转到target_id
    def transfer(self, username, target_id, money):
        sql1 = "select bank_card_id from web_associ_bank where username='%s';" % username
        # print(sql1)
        self.cur.execute(sql1)
        do_card_id = self.cur.fetchone()[0]
        self.oper_record_id = int(datetime.today().microsecond)
        if do_card_id == target_id:
            sql2 = "call deposit(%d,'%s',%f)" % (self.oper_record_id, target_id, money)
        else:
            sql2 = "call transfer_money(%d,'%s','%s',%f);" % (self.oper_record_id, do_card_id, target_id, money)
        self.cur.execute(sql2)
        finish_status = self.cur.fetchone()[0]
        return finish_status

    # 注册账户
    def registor_account(self, username, password, id_num, location, telephone, client_name):
        """判断帐号是否存在， 传递的参数是银行卡号的id"""
        check_exists = self.check_account(username, password)
        if check_exists is None:
            select_sqli = "call create_new_web_acc('%s','%s','%s','%s','%s','%s');" % (
                username,
                password,
                id_num,
                location,
                telephone,
                client_name,
            )
            # print(select_sqli)
            self.cur.execute(select_sqli)
            check_exists2 = self.check_account(username, password)
            if check_exists2 is not None:
                return "success"  # '注册成功'
            else:
                return render_template("registor_failed.html")
        else:
            return render_template("registor_exists.html")

    # 获得账户余额
    def get_money(self, username):
        sql = "select bank_card_id from bank_account natural join web_associ_bank where username='%s';" % username
        # print(sql)
        self.cur.execute(sql)
        card_id = self.cur.fetchone()
        if card_id:
            nextsql = "select getmoney('%s');" % card_id
            self.cur.execute(nextsql)
            left_money = self.cur.fetchone()
            return [left_money, card_id]
        else:
            return None

    # 返回结果
    def return_result(self, username):
        sql1 = "select bank_card_id from web_associ_bank where username='%s';" % username
        self.cur.execute(sql1)
        do_card_id = self.cur.fetchone()[0]
        sql = (
            "select oper_date,oper_value from acc_oper_record where oper_kind='deposit' and do_oper='%s'\
             order by oper_date;"
            % do_card_id
        )
        self.cur.execute(sql)
        rv = self.cur.fetchall()
        return rv

    # 析构方法
    def __del__(self):
        self.cur.close()
        self.conn.close()


def get_value(str, target):
    namelist = re.split(r'[=&\s]\s*', str)
    for i in range(len(namelist)):
        if namelist[i] == target:
            return namelist[i+1]


# 用户访问到端口号重定向到登录页面
@app.route("/")
def index():
    return redirect(url_for("login"))


# 返回登录HTML网页
@app.route("/login")
def login():
    return render_template("login.html")  # fin


# 返回请求html(添加cookie)
@app.route("/static/<cookie>/<filename>")
def find_file(cookie, filename):
    return render_template(filename, cookie=cookie)


# 返回请求html
@app.route("/static/<filename>")
def static_file(filename):
    return render_template(filename)


# 登录事务
@app.route("/do_log?<argss>", methods=["get"])
def do_log(argss):
    username = get_value(argss, 'username')
    password = get_value(argss, 'password')
    user_ip = '192.168.100.1'
    power = administor_control.check_account(username, password)
    if power == 1:
        '''
        temp =   # fin
        response = make_response(temp)
        response.set_cookie("username", username, max_age=3600)'''
        administor_control.logon_record("log_on", username, user_ip)
        return render_template("hello_administor.html", username=username, cookie=username)
    elif power == 0:
        '''
        temp =   # fin
        response = make_response(temp)
        response.set_cookie("username", username, max_age=3600)'''
        administor_control.logon_record("log_on", username, user_ip)
        return render_template("hellio_client.html", username=username, cookie=username)
    else:
        return redirect(url_for("login"))


# 返回注册页面
@app.route("/regist")
def regist():
    return render_template("registor.html")  # fin


# 注册事务
@app.route("/registor?<argss>", methods=["get"])
def registor(argss):
    username = get_value(argss, "username")
    password = get_value(argss, "password")
    id_num = get_value(argss, "id_num")
    location = get_value(argss, "location")
    telephone = get_value(argss, "telephone")
    client_name = get_value(argss, "client_name")
    return_message = administor_control.registor_account(username, password, id_num, location, telephone, client_name)
    user_ip = '192.168.100.1'

    if return_message == "success":
        '''
        temp = 
        response = make_response(temp)
        response.set_cookie(username, password, max_age=3600)'''
        administor_control.logon_record("log_on", username, user_ip)
        return render_template("hellio_client.html", username=username, cookie=username)
    else:
        return return_message


# 用户主界面显示
@app.route("/client/<cookie>")
def client(cookie):
    username = cookie
    # print(username)
    left_money = administor_control.get_money(username)
    if left_money is None:
        return render_template(
            "client.html", username=username, cookie=cookie, left_money="unknown", conn_status="False",
            bank_card_id="unknown"
        )
    else:
        return render_template(
            "client.html", username=username, cookie=cookie, left_money=left_money[0], conn_status="账户已连接",
            bank_card_id=left_money[1]
        )  # fin


# 交易事务
@app.route("/trade/<cookie>?<argss>", methods=["get"])
def trade(cookie, argss):
    username = cookie
    target_username = get_value(argss, "target_username")
    value = get_value(argss, "value")
    return_mess = administor_control.transfer(username, target_username, float(value))
    if return_mess:
        return render_template("transfer_finish.html", username=target_username, cookie=cookie, value=value)  # fin
    else:
        return render_template("failtotransfer.html", username=target_username, cookie=cookie, value=value)  # fin


# 绘制存钱折线图的获取数据函数
@app.route("/deposit_trade_record/<cookie>", methods=["get"])  # ?get
def deposit_trade_record(cookie):
    username = cookie
    rcv = administor_control.return_result(username)
    # print(rcv)
    return jsonify(oper_date=[x[0] for x in rcv], oper_value=[str(x[1]) for x in rcv])


# 交易记录查看事务
@app.route("/trade_record/<cookie>")
def trade_record(cookie):
    return render_template("trade_record.html", cookie=cookie)


# 关联银行卡事务
@app.route("/bank_account/<cookie>?<argss>", methods=["get"])
def bank_account(cookie, argss):
    bank_card_id = get_value(argss, "bank_card_id")
    card_password = get_value(argss, "bank_password")
    username = cookie
    if_suc = administor_control.connect(username, bank_card_id, card_password)
    if if_suc:
        left_money = administor_control.get_money(username)
        # print(left_money)
        return render_template(
            "client.html", username=username, cookie=cookie, left_money=left_money[0], conn_status="账户已连接",
            bank_card_id=left_money[1]
        )  # fin
    else:
        return render_template("bank_connect.html", cookie=cookie)  # fin -------pre cookie------


# 解除关联
@app.route("/deconnect/<cookie>")
def deconnect(cookie):
    username = cookie
    status = administor_control.deconnect(username)
    if status:
        return render_template("deconnect_success.html", cookie=cookie)
    else:
        return render_template("fail_deconnect.html", cookie=cookie)


# 管理员主界面
@app.route("/administor")
def administor():
    username = request.cookies.get("username")
    return render_template("administor.html", username=username)  # fin


# 登出事务
@app.route("/logout/<cookie>")
def logout(cookie):
    username = cookie
    user_ip = '192.168.100.1'
    administor_control.logon_record("log_out", username, user_ip)
    return render_template("logout.html", username=username)  # fin


config = configparser.ConfigParser()
config.read('config.ini', encoding='utf-8')
host = config.get("mysqlconfig", "host")
user = config.get("mysqlconfig", "user")
password = config.get("mysqlconfig", "passwd")
port = config.getint("mysqlconfig", "port")
db = config.get("mysqlconfig", "db")
# 数据库最高控制权限
administor_conn = pymysql.connect(
    host=host,  # 连接名称，默认127.0.0.1
    user=user,  # 用户名
    passwd=password,  # 密码
    port=port,  # 端口，默认为3306
    db=db,  # 数据库名称
    charset="utf8",
    autocommit=True,
)
# 实例
administor_control = ControlSQL(administor_conn)
flask_app = app.wsgi_app
