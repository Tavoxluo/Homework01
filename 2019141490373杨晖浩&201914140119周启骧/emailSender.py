# coding=utf-8

import smtplib
import imaplib
import email.mime.multipart
import email.message
import os


def createEmail(subject, content, fmail, sender, tmail_list, pathlist=None):
    """
    :param subject:邮件主题
    :param content: 邮件内容
    :param fmail: 发件人地址
    :param sender: 发件人名称
    :param tmail_list: 收件人列表
    :param pathlist: 附件路径列表(默认没有)
    :return msg: 构造完成的邮件
    """
    # 创建邮件
    msg = email.message.EmailMessage()
    msg['subject'] = subject
    msg['from'] = sender + '<' + fmail + '>'
    msg['to'] = ','.join(tmail_list)
    msg['date'] = email.utils.formatdate(None, True, True)
    msg['Content-Type'] = 'text/html'
    msg.set_payload(content, charset='utf8')
    # 有附件列表则添加附件
    if pathlist and pathlist != []:
        subfile = email.mime.multipart.MIMEMultipart()
        subfile['Content-Type'] = 'multipart/related'
        for path in pathlist:
            try:
                data = open(path, 'rb')
            except:
                return '附件不存在或为文件夹\n'
            filetype = path.split('.')[-1]
            datafile = email.mime.multipart.MIMEBase(filetype, filetype)
            datafile.set_payload(data.read())
            data.close()
            email.encoders.encode_base64(datafile)
            basename = os.path.basename(path)
            datafile.add_header('Content-Disposition', 'attachment', filename=basename)
            subfile.attach(datafile)
        fullmessage = email.mime.multipart.MIMEMultipart()
        fullmessage['subject'] = subject
        fullmessage['from'] = sender + '<' + fmail + '>'
        fullmessage['date'] = email.utils.formatdate(None, True, True)
        fullmessage['Content-Type'] = 'multipart/mixed'
        fullmessage.attach(msg)
        fullmessage.attach(subfile)
        return fullmessage
    else:
        return msg


def sendEmailSMTP(fmail, password, tmail_list, message):
    """
    :param fmail: 发件账户地址
    :param password: 发件账户密码
    :param tmail_list: 收件人列表
    :param message: 结构化邮件消息
    :return mailstate: 发件结果
    """
    mail_host = 'smtp.' + fmail.split('@')[-1]
    try:
        smtpObj = smtplib.SMTP_SSL(mail_host, 465)
        smtpObj.login(fmail, password)
        smtpObj.sendmail(fmail, tmail_list, message.as_string())
        mailstate = '邮件发送成功\n'
        smtpObj.close()
    except:
        mailstate = '邮件发送失败\n'
    return mailstate
