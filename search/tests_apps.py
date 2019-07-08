from django.apps import apps
from django.test import TestCase
from .apps import SearchConfig


class test_searchconfig(TestCase):

    def test_app(self):
        self.assertEqual("search", SearchConfig.name)
        self.assertEqual("search", apps.get_app_config("search").name)