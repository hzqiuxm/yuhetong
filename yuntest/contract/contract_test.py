# -*- coding: utf-8 -*-
__author__ = 'Seanwu'

import unittest, json, time, hashlib, tempfile
from docx import Document
from yunapp import app, config

app.config['WTF_CSRF_ENABLED'] = False


class TestContract(unittest.TestCase):
    __testuid = 0
    __test_user = {'username': str(int(time.time())) + '@qq.com',
                   'password': 'test', 'email': 'wuxuewen_hz@163.com',
                   'type': '0', 'real_name': 'seanwu', 'phone': '123456789'}

    __take_passwd__ = ''
    __contract_id__ = ''
    __auth_passwd__ = ''

    @classmethod
    def setUpClass(cls):
        app.config['TESTING'] = True
        # Wrong key:
        # app.config['CSRF_ENABLED'] = False
        # Right key:
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['WTF_CSRF_ENABLED'] = False

        cls.app = app.test_client()

        # rv = cls.app.post('/api/user/register', data=dict(
        # username=cls.__test_user['username'],
        # password=cls.__test_user['password'],
        # email=cls.__test_user['email']
        # ), follow_redirects=True)
        # if 'true' in rv.data:
        # c_user = json.loads(rv.data)
        # cls.__testuid = int(c_user['uid'])
        # else:
        # raise AssertionError

    def setUp(self):
        # self.app.post('/api/user/login', data=dict(
        # username=self.__test_user['username'],
        # password=self.__test_user['password']
        # ), follow_redirects=True)
        self.app.post('/api/user/login', data=dict(
            username='lxTest@yunhetong.com',
            password='lxTest'
        ), follow_redirects=True)

    def tearDown(self):
        pass

    def doc_create(self, data):
        return self.app.post('/contract/aaa.docx', data=dict(data=data))

    # def test_doc_create(self):
    # rv = self.doc_create('<h1>aaaa<h1>
    # <p>bbbbbb<span>ccc</span>bbbb</p><li>ddddd</li>')
    # test_document = Document(rv.stream)
    # pls = test_document.paragraphs
    # pass

    def add_contract(self, data):
        return self.app.post('/api/contract/', data=data)

    def update_contract(self, cid, data):
        return self.app.put('/api/contract/' + cid, data=data)

    def save_draft(self, cid, data):
        return self.app.post('/api/contract/save_draft/' + cid, data=data)

    def owner_confirm_contract(self, cid, data):
        return self.app.get('/api/contract/owner_confirm_contract/' + cid, data=data)

    def del_contract(self, cid, passwrod):
        return self.app.delete('/api/contract/' + cid + '?passwd=' + passwrod)

    def part_read_contract(self, cid, take_passwd):
        return self.app.post('/api/contract/part_read_contract/' + cid, data=dict(take_passwd=take_passwd))

    def part_take_contract(self, cid, take_passwd):
        return self.app.post('/api/contract/part_take_contract/' + cid, data=dict(take_passwd=take_passwd))

    def part_reject_contract(self, cid, take_passwd):
        return self.app.post('/api/contract/part_reject_contract/' + cid, data=dict(take_passwd=take_passwd))

    def auth_contract(self, cid, data):
        return self.app.post('/api/contract/auth_contract/' + cid, data=data)

    def take_auth(self, auth_url, auth_passwd):
        print auth_url
        return self.app.post(auth_url, data=dict(auth_passwd=auth_passwd))

    def get_contract(self, cid):
        return self.app.get('/api/contract/' + cid)

    def get_contracts(self):
        return self.app.get('/api/contract/')

    def sign_contract(self, cid):
        return self.app.post('/api/contract/sign_contract/' + cid)

    def test_other(self):
        data = {}
        #test user error
        self.app.post('/api/user/login', data=dict(
            username='lxTest2@yunhetong.com',
            password='lxTest'
        ), follow_redirects=True)
        rv = self.owner_confirm_contract('28', data)
        assert 'false' in rv.data
        self.app.post('/api/user/login', data=dict(
            username='lxTest@yunhetong.com',
            password='lxTest'
        ), follow_redirects=True)
        # test comfirm contract
        rv = self.owner_confirm_contract('28', data)
        assert 'true' in rv.data
        contrace = json.loads(rv.data)
        self.__take_passwd__ = contrace['data']['take_passwd']

        # test  read contract
        rv = self.part_read_contract('28', take_passwd=self.__take_passwd__)
        assert 'true' in rv.data

        # test  read contract
        rv = self.part_take_contract('28', take_passwd=self.__take_passwd__)
        print rv.data
        assert 'true' in rv.data

        # test  read contract
        rv = self.part_reject_contract('28', take_passwd=self.__take_passwd__)
        assert 'true' in rv.data

        # test produce auth_contract
        auth_data = dict()
        auth_data['read_perm'] = 0
        auth_data['write_perm'] = 0
        auth_data['sign_perm'] = 1
        auth_data['expire_days'] = 10
        auth_data['sub_user_id'] = ''
        rv = self.auth_contract('28', auth_data)
        assert 'true' in rv.data
        auth = json.loads(rv.data)
        self.__auth_passwd__ = auth['data']['auth_passwd']
        auth_url = auth['data']['auth_url']

        #test receive auth
        rv = self.take_auth(auth_url, auth_passwd=self.__auth_passwd__)
        assert 'true' in rv.data

        #test get contract
        rv = self.get_contract('28')
        assert 'true' in rv.data

        #test get contracts
        rv = self.get_contracts()
        assert 'true' in rv.data

        #test sign contracts
        rv = self.sign_contract('28')
        assert 'true' in rv.data


    def test_contrct_crud(self):
        data = dict()
        '''
            add contract
        '''
        data['contract_content'] = 'this is a test new content'
        data['appendix'] = '1,2,3'
        data['part_num'] = '2'
        # test no contract name
        rv = self.add_contract(data)
        assert 'false' in rv.data
        # test successful case
        data['contract_name'] = 'newname'
        rv = self.add_contract(data)
        assert 'true' in rv.data
        contrace = json.loads(rv.data)
        self.__contract_id__ = str(contrace['data'])

        '''
            save draft
        '''
        #test no contract_content
        data['contract_content']=''
        rv = self.save_draft(self.__contract_id__, data)
        print rv.data
        assert 'false' in rv.data
        data['contract_content'] = 'this is a draft~~ this is a draft~~'
        # test successful case
        rv = self.save_draft(self.__contract_id__, data)
        assert 'true' in rv.data

        '''
            test update
        '''
        data['contract_name'] = 'newname'
        data['contract_content'] = 'this is a update  update'
        data['appendix'] = '4,5,6'

        # test new_vresion is False
        data['new_version'] = False
        rv = self.update_contract(self.__contract_id__, data)
        assert 'true' in rv.data

        # test new_vresion is true
        data['new_version'] = True
        rv = self.update_contract(cid=self.__contract_id__, data=data)
        assert 'true' in rv.data

        # test delete
        rv = self.del_contract(cid=self.__contract_id__, passwrod='lxTest')
        assert 'true' in rv.data

        # def test_delete(self):
        # rv = self.app.delete('api/contract/2?x=xx', data={'x': 'xx'})
        # print rv


if __name__ == '__main__':
    unittest.main()