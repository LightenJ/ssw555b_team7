
from unittest import TestCase
from validity_test import younger_than_150
from gedcom.element.individual import IndividualElement


class Test(TestCase):
    def test_younger_than_150(self):
        self.assertEqual(younger_than_150("12 DEC 1980", "", "Fred Smith"), "")
        self.assertNotEqual(younger_than_150("12 DEC 1870", "", "Fred Smith"), "")
        self.assertEqual(younger_than_150("12 DEC 1980", "11 DEC 2130", "Fred Smith"), "")
        self.assertNotEqual(younger_than_150("12 DEC 1980", "12 DEC 2130", "Fred Smith"), "")
        self.assertNotEqual(younger_than_150("12 DEC 1980", "13 DEC 2130", "Fred Smith"), "")
        self.assertNotEqual(younger_than_150("12 NOV 1980", "01 DEC 2130", "Fred Smith"), "")
