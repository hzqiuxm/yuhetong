# -*- coding: utf-8 -*-
__author__ = 'Seanwu'

import unittest, json, time, hashlib, tempfile
from docx import Document
from yunapp import app, config

app.config['WTF_CSRF_ENABLED'] = False


class TestContract(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()

    def tearDown(self):
        pass

    def doc_create(self, data):
        return self.app.post('/contract/aaa.docx', data=dict(data=data))

    # def test_doc_create(self):
    #     rv = self.doc_create('<h1>aaaa<h1><p>bbbbbb<span>ccc</span>bbbb</p><li>ddddd</li>')
    #     test_document = Document(rv.stream)
    #     pls = test_document.paragraphs
    #     pass

    def test_delete(self):
        rv = self.app.delete('api/contract/2?x=xx', data = {'x': 'xx'})
        print rv

if __name__ == '__main__':
    unittest.main()