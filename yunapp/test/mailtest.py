# -*- coding: utf-8 -*-
# encoding: utf-8
#!/FlaskTest/
__author__ = 'Seanwu'
import requests
import smtplib
import os


# def send_simple_message():
#     return requests.post(
#         "https://api.mailgun.net/v2/samples.mailgun.org/messages",
#         auth=("api", "key-3412c17133fae9d668bb275089a3890c"),
#         data={"from": "SeanWu<postmaster@sandboxc264adea79684d24b0fa4e884e7167de.mailgun.org>",
#               "to": ["wuxuewen_hz@qq.com", "wuxuewen_hz@qq.com"],
#               "subject": "Hello World",
#               "text": "Testing some Mailgun awesomness!"})
# send_simple_message()

import smtplib
from email.mime.text import MIMEText

msg = MIMEText('Testing some Mailgun awesomness')
msg['Subject'] = "Hello"
msg['From'] = "seanwu@yunhetong.net"
msg['To'] = "304967415@qq.com"

s = smtplib.SMTP('smtp.mailgun.org', 587)

s.login('postmaster@sandboxc264adea79684d24b0fa4e884e7167de.mailgun.org', '9ef4b057eb214a991e5e24fc1b4814e2')
s.sendmail(msg['From'], msg['To'], msg.as_string())
s.quit()