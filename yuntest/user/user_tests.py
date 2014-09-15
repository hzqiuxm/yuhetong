import unittest, json, time, hashlib, tempfile

from yunapp import app, config


class TestUser(unittest.TestCase):
    __testuid = 0
    __test_user = {'username': str(int(time.time())) + '@qq.com',
                   'password': 'test', 'email': 'wuxuewen_hz@163.com',
                   'type': '0','real_name': 'seanwu', 'phone': '123456789'}

    @classmethod
    def setUpClass(cls):
        app.config['TESTING'] = True
        # Wrong key:
        # app.config['CSRF_ENABLED'] = False
        # Right key:
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['WTF_CSRF_ENABLED'] = False

        cls.app = app.test_client()

        rv = cls.app.post('/api/user/register', data=dict(
            username=cls.__test_user['username'],
            password=cls.__test_user['password'],
            email=cls.__test_user['email']
        ), follow_redirects=True)
        if 'true' in rv.data:
            c_user = json.loads(rv.data)
            cls.__testuid = int(c_user['uid'])
        else:
            raise AssertionError

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def register(self, username, password, email):
        return self.app.post('/api/user/register', data=dict(
            username=username,
            password=password,
            email=email
        ), follow_redirects=True)

    def login(self, username, password):
        return self.app.post('/api/user/login', data=dict(
            username=username,
            password=password
        ), follow_redirects=True)

    def logout(self):
        return self.app.get('/api/user/logout', follow_redirects=True)

    def deluser(self, uid, password):
        print password
        return self.app.delete('/api/user/del/' + str(uid) +
                               '?password=' + password, follow_redirects=True)

    def update_user(self, uid, password='', utype='', real_name='', phone=''):
        return self.app.put('/api/user/update', data=dict(
            uid=uid,
            password=password,
            type=utype,
            real_name=real_name,
            phone=phone), follow_redirects=True)

    def active(self, active_code):
        return self.app.post('/api/user/active/' +
                             active_code, follow_redirects=True)

    def add_sub_user(self):
        test_data = dict(username=str(int(time.time())) + 'a@qq.com',
                         type='0', password='test', email='ttt@test.com',
                         phone='123456789', idCardNo='330327200505050033',
                         idCardimg1='12', idCardimg2='13',
                         authorizationimg='14')
        return self.app.post('/api/user/addsubuser',
                             data=test_data, follow_redirects=True)

    def resert_password(self):
        self.login(TestUser.__test_user['username'],
                   TestUser.__test_user['password'])
        return self.app.put('/api/user/resetpwd',
                            data=dict(password='test'), follow_redirects=True)


    def test_active(self):
        # test error activecode
        self.login(TestUser.__test_user['username'],
                   TestUser.__test_user['password'])
        rv = self.active('asdfasafd')
        assert 'false' in rv.data
        # test success case
        activecode = hashlib.md5(TestUser.__test_user['username'] +
                                 config.MD5_SUFFIX).hexdigest()
        rv = self.active(activecode)
        assert 'true' in rv.data

    def test_resertpassword(self):
        self.login(TestUser.__test_user['username'],
                   TestUser.__test_user['password'])
        rv = self.resert_password()
        assert 'true' in rv.data

    def test_addsubuser(self):
        self.login(TestUser.__test_user['username'],
                   TestUser.__test_user['password'])
        rv = self.add_sub_user()
        assert 'true' in rv.data

    def test_register(self):
        # test no username
        rv = self.register('', 'test200', 'wuxuewen@163.com')
        assert 'false' in rv.data
        # test no password
        rv = self.register('test200', '', 'wuxuewen@163.com')
        assert 'false' in rv.data
        # test no email
        rv = self.register('test200', 'test200', '')
        assert 'false' in rv.data
        # test email type error
        rv = self.register('test200', 'test200', 'wuxuewen#163.com')
        assert 'false' in rv.data
        # test username type error
        rv = self.register('test!@#$200', 'test200', 'wuxuewen@163.com')
        assert 'false' in rv.data
        # test success cond
        rv = self.register(str(int(time.time())) + '2' + '@qq.com',
                           TestUser.__test_user['password'],
                           TestUser.__test_user['email'])
        assert 'true' in rv.data

    def test_login_logout(self):
        # test no password
        rv = self.login('admin', '')
        assert 'false' in rv.data
        # test no username
        rv = self.login('', 'passwd')
        assert 'false' in rv.data
        # test not exist username
        rv = self.login('noexist', 'passwd')
        assert 'false' in rv.data
        # test wrong passwd
        rv = self.login('admin', 'wrong passwd')
        assert 'false' in rv.data
        # test success cond
        rv = self.login(TestUser.__test_user['username'],
                        TestUser.__test_user['password'])
        assert 'true' in rv.data
        rv = self.logout()
        assert 'true' in rv.data

    def test_updateuser(self):
        # test success cond
        self.login(TestUser.__test_user['username'],
                   TestUser.__test_user['password'])
        rv = self.update_user(uid=TestUser.__testuid,
                              password=TestUser.__test_user['password'],
                              real_name=self.__test_user['real_name'],
                              # email='test@test.com',
                              utype='0', phone=self.__test_user['phone'])
        assert 'true' in rv.data
        self.logout()

    def test_deluser(self):
        # test no uid
        # rv = self.deluser('','test')
        # print rv.data
        # assert 'false' in rv.data
        # test useless uid
        rv = self.deluser(2553, 'test')
        assert 'false' in rv.data
        # test no password
        # rv = self.deluser(TestUser.__testuid, '')
        # assert 'false' in rv.data
        # test success cond
        print '111'
        rv = self.deluser(uid=TestUser.__testuid, password='test')
        print rv.data
        assert 'true' in rv.data


if __name__ == '__main__':
    unittest.main()