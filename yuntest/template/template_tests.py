import unittest
from yunapp import app

class TestTemplate(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()

    def tearDown(self):
        pass

    def add_template(self):
        self.app.post()

    def get_template_types(self, parent_type_id=None):
        self.app.get('/ctemplate/templates', query_string=dict(
            parent_type_id = parent_type_id
        ), follow_redirects=True)

    def test_template_type(self):
        self.get_template_types(4)
