from unittest import TestCase
from cobnut import Cobnut
from cobnut.exceptions import ValidationBroker


class CobnutTestCase(TestCase):

    def test_without_broker(self):
        with self.assertRaises(ValidationBroker) as context:
            Cobnut()
            self.assertTrue('Need a broker to use cobnut' in context.exception)
