#!/usr/bin/env python3  
#coding: utf-8  
import smtplib  
from email.mime.multipart import MIMEMultipart  
from email.mime.text import MIMEText  
from email.mime.image import MIMEImage  
  
sender = 'luobinhe_vip@163.com'         #sender
receiver = '783505585@qq.com'           #receiver
subject = 'python email test'           #主题
smtpserver = 'smtp.163.com'             #smtp   
username = 'luobinhe_vip@163.com'       #用户名
password = '**************'           #授权码
  
# 创建消息容器
msg = MIMEMultipart('alternative')  
msg['Subject'] = "计网课设"             #这里修改邮件主题
  
#  正文部分修改
text = "你好\n这是计网邮箱程序测试\n你现在可以查看:\nhttp://www.python.org"  
html = """\ 
<html> 
  <head></head> 
  <body> 
    <p>你好<br> 
       这是计网邮箱程序测试<br> 
       你可以查看 <a href="http://www.python.org">python官网</a>. 
    </p> 
  </body> 
</html> 
"""  
  
# 记录这两部分的MIME类型-text/plain和text/html。
part1 = MIMEText(text, 'plain')  
part2 = MIMEText(html, 'html')  
  
# 将部件连接到消息容器中。 

msg.attach(part1)  
msg.attach(part2)  
#构造附件  本处用照片举例
att = MIMEText(open('D:\\python\\mmscc\\1.jpg', 'rb').read(), 'base64', 'utf-8')  #索引部分是//不是/ 一开始记错了
att["Content-Type"] = 'application/octet-stream'  
att["Content-Disposition"] = 'attachment; filename="1.jpg"'  
msg.attach(att)  
#smtp构件     
smtp = smtplib.SMTP()  
smtp.connect('smtp.163.com')  
smtp.login(username, password)  
smtp.sendmail(sender, receiver, msg.as_string())  
smtp.quit()  