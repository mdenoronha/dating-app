from django.apps import apps
from django.test import TestCase
from .apps import AccountConfig


class test_accountconfig(TestCase):

    def test_app(self):
        self.assertEqual("account", AccountConfig.name)
        self.assertEqual("account", apps.get_app_config("account").name)