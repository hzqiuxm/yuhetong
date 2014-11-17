# -*- coding: utf-8 -*-
import unittest, time

from yunapp.app_tasks.cel_tasks import send_mail


class TestCelAppMail(unittest.TestCase):

    def test_send_mail(self):
        m_content = 'Test from lvxun xudb.'
        m_subject = 'Test from lvxun xudb.'
        m_to = 'micheal.xudb@foxmail.com'
        send_result = send_mail.delay(m_content, m_subject, m_to)
        print send_result.ready()
        time.sleep(15)
        sned_result = send_result.get()
        print sned_result


if __name__ == '__main__':
    unittest.main()