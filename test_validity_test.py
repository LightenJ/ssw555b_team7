
from unittest import TestCase
from validity_test import younger_than_150, date_before
from validity_test import birthbeforemarriage
from validity_test import birthbeforedeath
from datetime import datetime, timedelta

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

####US01##### Dates (Birth, Death, Marriage, Divorce) Before Today

    def test_date_lessthan_current(self):
        self.assertEqual(date_before(("12 DEC 1980", "12 DEC 1990", "29 Dec 2020")), False) #< current date
        self.assertFalse(date_before(("12 DEC 1980", "01 DEC 1990", "29 Dec 2020")), False) #< current date
        self.assertNotEqual(date_before(("12 DEC 1980", "12 DEC 1990", "29 Dec 2020")), True) #< current date
        self.assertIn(date_before(("12 DEC 1980", "12 DEC 1990", "29 Dec 2020")), (False, None)) #< current date
        self.assertIsNone(date_before(("12 DEC 1980", "12 DEC 1990", "29Dec 2020")), None) # invalid date

    def test_date_equalto_current(self):
        current_date = datetime.now().date().strftime('%d %b %Y')
        self.assertEqual(date_before(("12 DEC 1980", "12 DEC 1990", current_date)), False)# = current date

    def test_date_greaterthan_current(self):
        current_date_plus = datetime.now().date() + timedelta(days=1)
        self.assertTrue(date_before(("12 DEC 1980",current_date_plus.strftime('%d %b %Y') , "29 Dec 2020")), True)# > current date

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
