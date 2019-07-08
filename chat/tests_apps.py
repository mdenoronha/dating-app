from django.apps import apps
from django.test import TestCase
from .apps import ChatConfig


class test_chatconfig(TestCase):

    def test_app(self):
        self.assertEqual("chat", ChatConfig.name)
        self.assertEqual("chat", apps.get_app_config("chat").name)