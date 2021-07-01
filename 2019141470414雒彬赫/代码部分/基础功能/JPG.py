#!/usr/bin/env python3  
#coding: utf-8  
import smtplib  
from email.mime.multipart import MIMEMultipart  
from email.mime.text import MIMEText  
from email.mime.image import MIMEImage  
  
sender = '***'  
receiver = '***'  
subject = 'python email test'  
smtpserver = 'smtp.163.com'  
username = '***'  
password = '***'  
  
msgRoot = MIMEMultipart('related')  
msgRoot['Subject'] = 'test message'  
  
msgText = MIMEText('<b>Some <i>HTML</i> text</b> and an image.<br><img src="cid:image1"><br>good!','html','utf-8')  
msgRoot.attach(msgText)  
  
fp = open('h:\\python\\1.jpg', 'rb')  
msgImage = MIMEImage(fp.read())  
fp.close()  
  
msgImage.add_header('Content-ID', '<image1>')  
msgRoot.attach(msgImage)  
  
smtp = smtplib.SMTP()  
smtp.connect('smtp.163.com')  
smtp.login(username, password)  
smtp.sendmail(sender, receiver, msgRoot.as_string())  
smtp.quit()  