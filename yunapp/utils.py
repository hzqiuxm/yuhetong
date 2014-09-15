# -*- coding: utf-8 -*-
# # Common function  or comman constans
import cgi, hashlib, time
# 下面这三句是发邮件的
import smtplib, logging
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.header import Header
from yunapp.orm import model, engine


app_logger = logging.getLogger('yunapp')
business_logger = logging.getLogger('business')


def show_site_map(rules, prefix=None):
    links = []
    support_method = set(['GET', 'POST', 'PUT', 'DELETE'])

    for rule in rules:
        method = support_method & rule.methods
        links.append((rule.rule, method.pop(), rule.endpoint))

    s = []
    s.append('<h2>Site Map</h2><table width="800"><tr><td width="20%"><b>Method</b>')
    s.append('</td><td><b>URI</b></td><td><b>Function</b></td></tr>')

    links = sorted(links, key=lambda link: (link[0], link[1]))
    if prefix is None:
        prefix = ''
    for url, method, name in links:
        s.append('<tr><td>[%s]</td><td><a href="%s" target="_blank">%s</a>'
                 '</td><td>%s</td></tr>'
                 % (method, prefix + url, cgi.escape(url), name))

    s.append('</table>')
    return ''.join(s)


def sent_mail(e_content, e_from, e_to, e_subject):
    """
    :author:seanwu
    :param content: 邮件内容
    :param e_from: 发件人
    :param e_to: 收件人
    :param e_subject:邮件主题
    :return:True/False
    """
    msg = MIMEMultipart('alternative')
    # msg = MIMEText('http://www.baidu.com')
    subject = '激活邮件'
    msg["Accept-Language"] = "zh-CN"
    msg["Accept-Charset"] = "ISO-8859-1,utf-8"
    msg['Subject'] = Header(e_subject, 'utf-8')
    msg['From'] = e_from
    msg['To'] = e_to
    # part2 = MIMEText(text, _subtype='plain', _charset='utf-8')
    part1 = MIMEText(e_content, _subtype='html', _charset='utf-8')
    # msg.attach(part2)
    msg.attach(part1)
    s = smtplib.SMTP('smtp.mailgun.org', 587)
    s.login('postmaster@sandboxc264adea79684d24b0fa4e884e7167de.mailgun.org',
            '9ef4b057eb214a991e5e24fc1b4814e2')
    s.sendmail(msg['From'], msg['To'], msg.as_string())
    with engine.with_session() as ss:
        new_email = model.LxEmail(eTo=msg['To'],
                                  eFrom=msg['From'],
                                  eSubject=e_subject,
                                  eContent=e_content)
        ss.add(new_email)
    s.quit()
    # business_logger.info('/n send email: /n To'+e_to+'/n
    # From'+e_from+'/n content'+e_content+'/n subject:'+e_subject)
    return True


def get_int_page_num(page_num):
    if page_num.isdigit():
        page_num = int(page_num)
    else:
        page_num = 1
    return page_num