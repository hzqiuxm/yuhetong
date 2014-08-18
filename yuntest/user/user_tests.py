import os
import unittest
import tempfile
from yunapp import app

class UserTestCase(unittest.TestCase):
    def setUP(self):
        print app.root_path
        print dir(app)
        pass

    def tearDown(self):
        pass


if __name__ == '__main__':
    unittest.main()