import os
import unittest
import tempfile
from yunapp import app

class TestUser(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()

    def tearDown(self):
        pass

    def register(self, username, password):
        return self.app.post('/user/register', data=dict(
            username=username,
            password=password
        ), follow_redirects=True)

    def login(self, username, password):
        return self.app.post('/user/login', data=dict(
            username=username,
            password=password
        ), follow_redirects=True)

    def logout(self):
        return self.app.get('/logout', follow_redirects=True)

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
        rv = self.login('test', 'lxTest')
        assert 'true' in rv.data





if __name__ == '__main__':
    unittest.main()