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