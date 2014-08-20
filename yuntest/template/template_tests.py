import unittest, json
from yunapp import app

class TestTemplate(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()

    def tearDown(self):
        pass

    def add_template(self):
        rv = self.app.post('/ctemplate/templates', data=dict(
            template_name='test_template',
            template_type_id = 4,
            template_content = """
                <xml>
                    content test
                    <p>page one</p>
                </xml>
            """
        ), follow_redirects=True)

        if rv.status_code != 200:
            print 'add template status_code error' + rv.status_code
            return None
        return json.loads(rv.data)

    def del_template(self, template_id):
        rv = self.app.delete('/ctemplate/' + str(template_id), follow_redirects=True)
        if rv.status_code != 200:
            print 'delete template status_code error' + rv.status_code
            return None
        return json.loads(rv.data)

    def update_template(self, template_id):
        rv = self.app.put('/ctemplate/' + str(template_id),data=dict(
            template_name = 'test_template_updated'
        ), follow_redirects=True)
        if rv.status_code != 200:
            print 'delete template status_code error' + rv.status_code
            return None
        return json.loads(rv.data)

    def get_template(self, template_id):
        rv = self.app.get('/ctemplate/' + str(template_id),
                            follow_redirects=True)
        if rv.status_code != 200:
            print 'delete template status_code error' + rv.status_code
            return None
        return json.loads(rv.data)

    def get_templates(self):
        rv = self.app.get('/ctemplate/templates',
                            follow_redirects=True)
        if rv.status_code != 200:
            print 'delete template status_code error' + rv.status_code
            return None
        return json.loads(rv.data)

    def get_template_types(self, parent_type_id=None):
        return self.app.get('/ctemplate/template_types', query_string=dict(
            parent_type_id = parent_type_id
        ), follow_redirects=True)

    ###### Test Begin
    def template_type(self):
        # Get level 0 types
        rv = self.get_template_types()
        assert 'true' in rv.data
        # Get level 1 types
        rv = self.get_template_types(1)
        assert 'true' in rv.data

    def template_add_and_del(self):
        # Get level 0 types
        add_result = self.add_template()
        if add_result is None:
            raise AssertionError
        self.assertEqual(add_result.get('success'), True)
        del_result = self.del_template(add_result.get('data'))
        if del_result is None:
            raise AssertionError
        self.assertEqual(del_result.get('success'), True)

    def template_update(self):
        # Get level 0 types
        add_result = self.add_template()
        if add_result is None:
            raise AssertionError

        update_result = self.update_template(add_result.get('data'))
        self.assertEqual(update_result.get('success'), True)

        del_result = self.del_template(add_result.get('data'))
        if del_result is None:
            raise AssertionError

    def template_get_one(self):
        add_result = self.add_template()
        if add_result is None:
            raise AssertionError

        get_result = self.get_template(add_result.get('data'))
        if get_result is None:
            raise AssertionError
        self.assertEqual(get_result.get('success'), True)

        del_result = self.del_template(add_result.get('data'))
        if del_result is None:
            raise AssertionError

    def test_template_get_list(self):
        add_result = self.add_template()
        if add_result is None:
            raise AssertionError

        get_result = self.get_templates()
        if get_result is None:
            raise AssertionError
        self.assertEqual(get_result.get('success'), True)

        del_result = self.del_template(add_result.get('data'))
        if del_result is None:
            raise AssertionError

if __name__ == '__main__':
    unittest.main()