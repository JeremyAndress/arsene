from unittest import TestCase
from arsene import Arsene
from arsene.exceptions import ValidationBroker


class arseneTestCase(TestCase):

    def test_without_broker(self):
        with self.assertRaises(ValidationBroker) as context:
            Arsene()
            self.assertTrue('Need a broker to use Arsene' in context.exception)
