from config import *


class RequestProtocol(object):

    @staticmethod
    def request_login_result(username, password):
        # 0001|user|pass
        return DELIMITER.join([REQUEST_LOGIN, username, password])

    @staticmethod
    def request_chat(username, message):
        # 0002|user|msg
        return DELIMITER.join([REQUEST_CHAT, username, message])

    @staticmethod
    def request_member(username, nickname):
        # 0003|user
        return DELIMITER.join([REQUEST_MEMBER, username, nickname])

    @staticmethod
    def request_delete(id):
        # 0004|id
        return DELIMITER.join([REQUEST_DELETE_MSG, id])

    @staticmethod
    def request_search(id, start, end, msg):
        # 0006|id|start_time|end_time|msg
        return DELIMITER.join([REQUEST_MSG_SEARCH, id, start, end, msg])

    @staticmethod
    def request_edit(type, msg, username):
        # 0009|type|msg
        return DELIMITER.join([REQUEST_MEMBER_EDIT, type, msg, username])

    @staticmethod
    def request_register(nickname, password):

        # 0010|nickname|password
        return DELIMITER.join([REQUEST_MEMBER_REGISTER, nickname, password])

    @staticmethod
    def request_member_delete(username):

        # 0008|username
        return DELIMITER.join([REQUEST_MEMBER_DELETE, username])