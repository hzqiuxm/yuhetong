# -*- coding: utf-8 -*-
import smtplib, logging
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.header import Header
from yunapp.instance import configs
from yunapp.orm import model, engine
from yunapp.app_tasks.cel_app import cel_app

app_logger = logging.getLogger('yunapp')
biz_logger = logging.getLogger('business')

@cel_app.task
def add(x, y):
    return x + y


@cel_app.task
def send_mail(e_content, e_subject, e_to, e_from=configs.EMAIL_CONFIG['MAIL_SENDER']):
    """
    :author:seanwu
    :param e_content: email content
    :param e_from: sender
    :param e_to: receiver
    :param e_subject: subject
    :return:True/False
    """
    msg = MIMEMultipart('alternative')
    # msg = MIMEText('http://www.baidu.com')
    msg["Accept-Language"] = configs.EMAIL_CONFIG['Accept-Language']
    msg["Accept-Charset"] = configs.EMAIL_CONFIG['Accept-Charset']
    msg['Subject'] = Header(e_subject, configs.EMAIL_CONFIG['Header_encode'])
    msg['From'] = e_from
    msg['To'] = e_to
    # part2 = MIMEText(text, _subtype='plain', _charset='utf-8')
    part1 = MIMEText(e_content, _subtype=configs.EMAIL_CONFIG['MIME_subtype'],
                     _charset=configs.EMAIL_CONFIG['MIME_encode'])
    # msg.attach(part2)
    msg.attach(part1)
    s = smtplib.SMTP(configs.EMAIL_CONFIG['MAIL_GUN_SERVER'], 587)
    try:
        s.login(configs.EMAIL_CONFIG['MAIL_GUN_POSTER'],
                configs.EMAIL_CONFIG['MAIL_GUN_KEY'])
        s.sendmail(msg['From'], msg['To'], msg.as_string())
        with engine.with_session() as ss:
            new_email = model.LxEmail(eTo=msg['To'],
                                      eFrom=msg['From'],
                                      eSubject=e_subject,
                                      eContent=e_content)
            ss.add(new_email)
    except smtplib.SMTPHeloError, smtplib.SMTPAuthenticationError:
        app_logger.exception('Smtp login Error')
    except smtplib.SMTPRecipientsRefused, smtplib.SMTPSenderRefused:
        app_logger.exception('Smtp send Error')
    except smtplib.SMTPDataError, smtplib.SMTPException:
        app_logger.exception('Smtp Error')

    s.quit()
    # business_logger.info('/n send email: /n To'+e_to+'/n
    # From'+e_from+'/n content'+e_content+'/n subject:'+e_subject)
    return True
