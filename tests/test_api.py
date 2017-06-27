import unittest

from api.app import create_app


class TestAPI(unittest.TestCase):

    def setUp(self):
        self.app = create_app('test_config')
        self.context = self.app.app_context()
        self.context.push()

    def tearDown(self):
        self.context.pop()
