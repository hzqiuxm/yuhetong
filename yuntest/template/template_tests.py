import unittest
from yunapp import app

class TestTemplate(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()

    def tearDown(self):
        pass

    def add_template(self):
        return self.app.post('/ctemplate/templates', data=dict(
            template_name='test_template',
            template_type_id = 4,
            template_content = """
                <xml>
                    content test
                    <p>page one</p>
                </xml>
            """
        ), follow_redirects=True)

    def del_template(self, template_id):
        return self.app.delete('/ctemplate/' + template_id,
                               follow_redirects=True)


    def get_template_types(self, parent_type_id=None):
        return self.app.get('/ctemplate/template_types', query_string=dict(
            parent_type_id = parent_type_id
        ), follow_redirects=True)

    def template_type(self):
        # Get level 0 types
        rv = self.get_template_types()
        assert 'true' in rv.data
        # Get level 1 types
        rv = self.get_template_types(4)
        assert 'true' in rv.data

    def test_template_add(self):
        # Get level 0 types
        rv = self.add_template()
        print rv.json


if __name__ == '__main__':
    unittest.main()