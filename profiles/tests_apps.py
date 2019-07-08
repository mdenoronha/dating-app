from django.apps import apps
from django.test import TestCase
from .apps import ProfilesConfig


class test_profilesconfig(TestCase):

    def test_app(self):
        self.assertEqual("profiles", ProfilesConfig.name)
        self.assertEqual("profiles", apps.get_app_config("profiles").name)