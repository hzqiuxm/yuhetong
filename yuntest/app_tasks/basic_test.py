# -*- coding: utf-8 -*-
import unittest, time
from yunapp.app_tasks.cel_tasks import add


class TestCelAppBasic(unittest.TestCase):

    def test_add(self):
        add_result = add.delay(5, 5)
        print add_result.ready()
        time.sleep(2)
        sum_add = add_result.get(timeout=1)
        print sum_add


if __name__ == '__main__':
    unittest.main()