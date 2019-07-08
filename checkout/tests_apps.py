from django.apps import apps
from django.test import TestCase
from .apps import CheckoutConfig


class test_checkoutconfig(TestCase):

    def test_app(self):
        self.assertEqual("checkout", CheckoutConfig.name)
        self.assertEqual("checkout", apps.get_app_config("checkout").name)