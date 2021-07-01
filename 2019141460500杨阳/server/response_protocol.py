from config import *

class ResponseProtocol(object):

    # 静态处理
    @staticmethod
    def response_login_result(result, nickname, username):

        # 返回生成用户登录的结果字符串
        # result：0表示失败 1表示成功
        return DELIMITER.join([RESPONSE_LOGIN_RESULT, result, nickname, username])

    @staticmethod
    def response_chat(nickname, messages):

        # messages:消息正文
        return DELIMITER.join([RESPONSE_CHAT, nickname, messages])

    @staticmethod
    def send_member(nickname, username):

        # 返回在线的人的昵称和用户名
        return DELIMITER.join([REQUEST_MEMBER, nickname, username])

    @staticmethod
    def send_delmember(nickname, username):

        # 返回在线的人的昵称和用户名
        return DELIMITER.join([RESPONSE_DELMEMBER, nickname, username])

    @staticmethod
    def send_msg(result, userlist):

        # 返回聊天记录
        return DELIMITER.join(([RESPONSE_MSG, result, userlist]))

    @staticmethod
    def send_search_msg(result):

        # 返回查询结果
        return DELIMITER.join([RESPONSE_MSG_SEARCH, result])

    @staticmethod
    def send_member_msg(result):

        # 返回成员信息
        return DELIMITER.join([RESPONSE_MEMBER_MSG, result])

    @staticmethod
    def send_member_edit_password(is_right):

        # 返回密码是否正确
        return DELIMITER.join([RESPONSE_MEMBER_EDIT, is_right])

    @staticmethod
    def send_register(username, nickname):

        # 返回注册信息
        return DELIMITER.join([RESPONSE_MEMBER_REGISTER, username, nickname])
