
from unittest import TestCase
from validity_test import younger_than_150
from validity_test import birthbeforemarriage
from validity_test import birthbeforedeath
from gedcom.element.individual import IndividualElement


class Test(TestCase):

    # This test verifies that we can detect if someone, living or dead, is 150 years old or older.
    def test_younger_than_150(self):
        # Young but still living
        self.assertEqual(younger_than_150("12 DEC 1980", "", "Fred Smith"), "")
        self.assertEqual(younger_than_150("12 DEC 1980", None, "Fred Smith"), "")

        # Old and still living
        self.assertNotEqual(younger_than_150("12 DEC 1870", "", "Fred Smith"), "")
        self.assertNotEqual(younger_than_150("12 DEC 1870", None, "Fred Smith"), "")

        # Tests right around 150 years of age
        self.assertEqual(younger_than_150("12 DEC 1980", "11 DEC 2130", "Fred Smith"), "")
        self.assertNotEqual(younger_than_150("12 DEC 1980", "12 DEC 2130", "Fred Smith"), "")
        self.assertNotEqual(younger_than_150("12 DEC 1980", "13 DEC 2130", "Fred Smith"), "")
        self.assertNotEqual(younger_than_150("12 NOV 1980", "01 DEC 2130", "Fred Smith"), "")

####US02#####
# This test verifies that the individual is born before marriage
    def test_birth_before_marriage(self):
        self.assertEqual(birthbeforemarriage("6 APR 2001", "", "Eric Sebast"), "")
        self.assertNotEqual(birthbeforemarriage("5 AUG 1785", "", "Eric Sebast"), "12 Mar 2020")
        self.assertEqual(birthbeforemarriage("12 DEC 1980", "12 NOV 2020", "Eric Sebast"), "")
        self.assertNotEqual(birthbeforemarriage("2 FEB 1975", "12 NOV 2020", "Eric Sebast"), "12 Mar 2020")
        self.assertNotEqual(birthbeforemarriage("12 DEC 1980", "12 NOV 2020", "Eric Sebast"), "12 Mar 2020")
        self.assertNotEqual(birthbeforemarriage("12 NOV 1980", "12 NOV 2020", "Eric Sebast"), "12 Mar 2020")

####US03#####
# This test verifies that the individual is born before death
    def test_birth_before_death(self):
        self.assertEqual(birthbeforedeath("6 APR 2001", "", "Eric Sebast"), "")
        self.assertNotEqual(birthbeforedeath("5 AUG 1785", "", "Eric Sebast"), "12 Mar 2020")
        self.assertEqual(birthbeforedeath("12 DEC 1980", "12 NOV 2020", "Eric Sebast"), "")
        self.assertNotEqual(birthbeforedeath("1 JUL 1990", "5 AUG 1784", "Eric Sebast"), "12 Mar 2020")
        self.assertNotEqual(birthbeforedeath("1 JUL 1990", "5 AUG 1784", "Eric Sebast"), "12 Mar 2020")
        self.assertNotEqual(birthbeforedeath("12 NOV 1980", "5 AUG 1784", "Eric Sebast"), "12 Mar 2020")
