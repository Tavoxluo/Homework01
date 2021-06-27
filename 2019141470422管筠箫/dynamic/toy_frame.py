import re
import dynamic.pydb
import urllib.parse


URL_DICT = dict()
""" 
完成请求的url 与函数指针的映射
URL_DICT = {
    "/index.py": index,
    "/center.py": center
}
"""


def route(url):
    def set_func(func):
        # URL_DICT[/index.py] = index
        URL_DICT[url] = func
        def call_func(*args, **kwargs):  # 这里能够传递所有index函数所需要的参数
            # 这里执行页面对应函数的功能
            return func(*args, **kwargs)
        return call_func
    return set_func


def fetchall_sql(sql):
    mysqlfunc = dynamic.pydb.MysqlFunc()
    mysqlfunc.execute_sql(sql)
    my_stock_info = mysqlfunc.cs.fetchall()
    mysqlfunc.close()
    return my_stock_info


def fetchone_sql(sql):
    mysqlfunc = dynamic.pydb.MysqlFunc()
    mysqlfunc.execute_sql(sql)
    my_stock_info = mysqlfunc.cs.fetchone()
    mysqlfunc.close()

    return my_stock_info


def needcommit_sql(sql):
    mysqlfunc = dynamic.pydb.MysqlFunc()
    mysqlfunc.execute_sql(sql)
    mysqlfunc.conn.commit()
    mysqlfunc.close()


@route(r"/register.html\?username=(.*)\&password=(.*)\&confirm=(.*)")
def register(ret):
    username = ret.group(1)
    password = ret.group(2)
    confirm = ret.group(3)
    if password != confirm:
        return "两次密码输入不一致"
    else:
        sql_select = """select * from stock_user where name ='%s';""" % username
        if fetchone_sql(sql_select):
            return "该用户名已存在,请重新注册"
        else:
            sql_insert = """insert into stock_user values ('%s', AES_ENCRYPT('%s','key'))""" %(username, password)
            needcommit_sql(sql_insert)
            with open("./templates/login.html", encoding='utf-8') as f:
                content = f.read()
            return content



@route(r"/login.html")
def login(ret):
    with open("./templates/login.html", encoding='utf-8') as f:
        content = f.read()
    return content


@route(r"/loginsuccess.html\?username=(.*)\&password=(.*)")
def login_success(ret):
    username = ret.group(1)
    password = ret.group(2)
    # 密码加密存储
    sql = """select cast(AES_DECRYPT(pwd,'key') as binary) from stock_user where name = '%s';""" % username
    pwd_tuple = fetchone_sql(sql)
    if not pwd_tuple:
        return "该用户名不存在"
    # print(pwd_tuple)
    # pwd = pwd_tuple[0]
    pwd = pwd_tuple[0].decode("utf-8")
    if pwd and pwd == password:
        if username == 'root':
            return index(ret)
        else:
            return userindex(ret)
    else:
        return "账户名或密码错误"


@route(r"/userindex.html")
# 带有参数的装饰器传参给最外层，由最外层函数返回值作为装饰器
# 然后执行装饰器功能index = set_func(index)
def userindex(ret):
    with open("./templates/userindex.html", encoding='utf-8') as f:
        content = f.read()
    # 连接数据库
    sql = "select * from information;"
    my_stock_info = fetchall_sql(sql)

    # button对象是一个Input元素，故html页面js代码可以执行
    #  $("input[name='toAdd']").each(function()
    tr_template = """
        <tr>
            <td>%s</td>
            <td>%s</td>
            <td>%s</td>
            <td>%s</td>
            <td>%s</td>
            <td>%s</td>
            <td>%s</td>
            <td>%s</td>
        </tr>
        """

    html = ""
    for line_info in my_stock_info:
        html += tr_template % (line_info[0], line_info[1], line_info[2], line_info[3], line_info[4], line_info[5], line_info[6],
                               line_info[7])
    # 从html文件中读出来的content 对其中的部分数据进行替换
    content = re.sub(r"\{%content%\}", html, content)

    return content


@route(r"/usercenter.html")
def usercenter(ret):
    with open("./templates/usercenter.html", encoding='utf-8') as f:
        content = f.read()

    sql = """select i.code,i.name,i.amplitude,i.turnover,i.price,i.high,f.note_info
     from information as i join focus as f on i.id=f.info_id;"""
    stock_infos = fetchall_sql(sql)
    # button对象是一个Input元素，故html页面js代码可以执行
    #  $("input[name='toDel']").each(function()
    tr_template = """
            <tr>
                <td>%s</td>
                <td>%s</td>
                <td>%s</td>
                <td>%s</td>
                <td>%s</td>
                <td>%s</td>
                <td>%s</td>
                <td>
                    <a type="button" class="btn btn-default btn-xs" href="/usershow/%s.html">查看走势</a>
                </td>
            </tr>
        """

    html = ""
    for line_info in stock_infos:
        html += tr_template % (
        line_info[0], line_info[1], line_info[2], line_info[3], line_info[4], line_info[5], line_info[6],line_info[0])

    # 从html文件中读出来的content 对其中的部分数据进行替换
    content = re.sub(r"\{%content%\}", html, content)

    return content


@route(r"/index.html")
# 带有参数的装饰器传参给最外层，由最外层函数返回值作为装饰器
# 然后执行装饰器功能index = set_func(index)
def index(ret):
    with open("./templates/index.html", encoding='utf-8') as f:
        content = f.read()
    # 连接数据库
    sql = "select * from information;"
    my_stock_info = fetchall_sql(sql)
    # button对象是一个Input元素，故html页面js代码可以执行
    #  $("input[name='toAdd']").each(function()
    tr_template = """
        <tr>
            <td>%s</td>
            <td>%s</td>
            <td>%s</td>
            <td>%s</td>
            <td>%s</td>
            <td>%s</td>
            <td>%s</td>
            <td>%s</td>
            <td>
                <input type="button" value="添加" id="toAdd" name="toAdd" systemidvalue="%s">
            </td>
        </tr>
        """

    html = ""
    for line_info in my_stock_info:
        html += tr_template % (line_info[0], line_info[1], line_info[2], line_info[3], line_info[4], line_info[5], line_info[6],
                               line_info[7], line_info[1])
    # 从html文件中读出来的content 对其中的部分数据进行替换
    content = re.sub(r"\{%content%\}", html, content)

    return content


@route(r"/center.html")
def center(ret):
    with open("./templates/center.html", encoding='utf-8') as f:
        content = f.read()

    sql = """select i.code,i.name,i.amplitude,i.turnover,i.price,i.high,f.note_info
         from information as i join focus as f on i.id=f.info_id;"""
    stock_infos = fetchall_sql(sql)
    # button对象是一个Input元素，故html页面js代码可以执行
    #  $("input[name='toDel']").each(function()
    tr_template = """
            <tr>
                <td>%s</td>
                <td>%s</td>
                <td>%s</td>
                <td>%s</td>
                <td>%s</td>
                <td>%s</td>
                <td>%s</td>
                <td>
                    <a type="button" class="btn btn-default btn-xs" href="/update/%s.html">修改</a>
                </td>
                <td>
                    <a type="button" class="btn btn-default btn-xs" href="/show/%s.html">查看走势</a>
                </td>
                <td>
                    <input type="button" value="删除" id="toDel" name="toDel" systemidvalue="%s">
                </td>
            </tr>
        """

    html = ""
    for line_info in stock_infos:
        html += tr_template % (
        line_info[0], line_info[1], line_info[2], line_info[3], line_info[4], line_info[5], line_info[6], line_info[0],
        line_info[0], line_info[0])

    # content = re.sub(r"\{%content%\}", str(stock_infos), content)
    # 从html文件中读出来的content 对其中的部分数据进行替换
    content = re.sub(r"\{%content%\}", html, content)

    return content


# 页面上很多按钮的请求的html文件虽然url不同，但route的函数是相同的，故需要采用正则
@route(r"/add/(\d+)\.html")
def add_focus(ret):

    # 获取股票代码
    # 传来的参数ret的分组是html页面内的js代码$.get("/add/" + code + ".html"）中的code
    stock_code = ret.group(1)

    # $.get("/add/" + code + ".html", function(data, status){
    # 						//function的参数data status是由浏览器自动传回的
    # 						//发送一个get请求并在页面上执行alert提示
    #                             alert("数据: " + data + "\n状态: " + status);
    #                         });
    # 上述js代码实现的仅仅是get请求并route到这个函数执行一些功能以及alert提示，并不会执行页面跳转，故显示的还是原来页面

    # 判断试下是否有这个股票代码
    sql = """select * from information where code=%s;""" % stock_code
    stock_tuple = fetchone_sql(sql)
    # 如果要是没有这个股票代码，那么就认为是非法的请求
    if not stock_tuple:
        return "没有这支股票"

    # 判断以下是否已经关注过
    sql = " select * from information as i inner join focus as f on i.id=f.info_id where i.code=%s;" % stock_code
    stock_tuple = fetchone_sql(sql)
    # 如果查出来了，那么表示已经关注过
    if stock_tuple:
        return "已关注，请勿重复关注"

    # 添加关注
    sql = "insert into focus (info_id) select id from information where code=%s;" % stock_code
    needcommit_sql(sql)

    return "关注成功"


@route(r"/del/(\d+)\.html")
def del_focus(ret):

    #  获取股票代码
    stock_code = ret.group(1)

    # 判断试下是否有这个股票代码
    sql = """select * from information where code=%s;""" % stock_code
    stock_tuple = fetchone_sql(sql)
    # 如果要是没有这个股票代码，那么就认为是非法的请求
    if not stock_tuple:
        return "没有这支股票"

    # 判断以下是否已经关注过
    sql = " select * from information as i inner join focus as f on i.id=f.info_id where i.code=%s;" % stock_code
    stock_tuple = fetchone_sql(sql)
    # 如果没有关注过，那么表示非法的请求
    if not stock_tuple:
        return "%s 之前未关注，请勿取消关注" % stock_code

    # 取消关注
    sql = "delete from focus where info_id = (select id from information where code=%s);" % stock_code
    needcommit_sql(sql)
    return "取消关注成功"


@route(r"/update/(\d+)\.html")
def show_update_page(ret):
    """显示修改的那个页面"""
    # 获取股票代码
    stock_code = ret.group(1)

    # 打开模板
    with open("./templates/update.html", encoding='utf8') as f:
        content = f.read()

    # 根据股票代码查询相关的备注信息
    # select f.note_info from focus as f inner join information as i on i.id=f.info_id where i.code=callcode;
    mysqlfunc = dynamic.pydb.MysqlFunc()
    cs = mysqlfunc.conn.cursor()
    cs.callproc("callproc_note", args=(stock_code,))

    stock_infos = cs.fetchone()
    note_info = stock_infos[0]  # 获取这个股票对应的备注信息
    mysqlfunc.close()

    content = re.sub(r"\{%note_info%\}", note_info, content)
    content = re.sub(r"\{%code%\}", stock_code, content)

    return content


@route(r"/update/(\d+)/(.*)\.html")
def save_update_page(ret):
    """"保存修改的信息"""
    stock_code = ret.group(1)
    comment = ret.group(2)
    # 解决浏览器Url的编码问题, url会将特殊字符编码，故需要将comment解码为原来的字符
    # 另外浏览器在显示空格时多个空格只显示一个，除非使用&nbsp
    comment = urllib.parse.unquote(comment)

    sql = """update focus set note_info='%s' where info_id = (select id from information where code=%s);""" % (comment, stock_code)
    needcommit_sql(sql)

    return "修改成功"


@route(r"/show/(\d+)\.html")
def show_update_page(ret):
    """显示股票走势"""
    return showall(ret, "show")


@route(r"/usershow/(\d+)\.html")
def usershow_update_page(ret):
    """显示股票走势"""
    return showall(ret, "usershow")


def showall(ret, show):
    """显示股票走势"""
    # 获取股票代码
    stock_code = ret.group(1)

    # 打开模板
    with open("./templates/%s.html" % show, encoding='utf8') as f:
        content = f.read()
        # 从html文件中读出来的content 对其中的部分数据进行替换
        content = re.sub(r"\{%code%\}", stock_code, content)
        try:
            open("./static/imags/%s.png" % stock_code)
            f.close()
        except Exception:
            return "该股票历年数据尚未获得"
    return content


def application(env, set_response_header):
    # 'Content-Type:text/html;charset=utf8'这个header不能少，否则无法识别文件类型
    # 这里的charset编码实际上就是connection_socket稍后发送将采用的编码，需要保持一致
    # windows下不指定Content-Type默认就要采用GBK
    set_response_header("200 OK", [('Content-Type', 'text/html;charset=utf8')])
    file_name = env['PATH_INFO']

    try:
        for regular_url, func in URL_DICT.items():
            # {
            #   r"/index.html":index,
            #   r"/center.html":center,
            #   r"/add/\d+\.html":add_focus
            # }
            ret = re.match(regular_url, file_name)
            # 匹配成功说明传递过来的file_name即url 有对应的正则表达式url去路由
            if ret:
                return func(ret)
                # func传入参数是为了正则表达式的分组使用，以便一个func对应多个url使用
            # 这边不能出现else判断 因为字典中只会正则匹配一个成功的url

        # for循环之后再进行else判断
        else:
            return "请求的url(%s)服务器没有对应文件" % file_name
    except Exception as e:
        return "产生了异常：%s" % e
