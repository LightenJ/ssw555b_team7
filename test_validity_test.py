
from unittest import TestCase
from validity_test import younger_than_150, date_before, unique_ids
from validity_test import birthbeforemarriage
from validity_test import birthbeforedeath
from validity_test import divorce_before_death, birth_before_marriage_of_parents
from validity_test import married_at_14_or_older,US04_marriage_before_divorce,US05_marriage_before_death
from datetime import datetime, timedelta


class Test(TestCase):

    # User Story 07: This test verifies that we can detect if someone, living or dead, is 150 years old or older.
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

    # User Story 06: Divorce must happen before a person's death
    def test_divorce_before_death(self):
        # Still living
        self.assertEqual(divorce_before_death("12 DEC 1980", "", "Fred Smith"), "")
        self.assertEqual(divorce_before_death("12 DEC 1980", None, "Fred Smith"), "")

        # Never divorced
        self.assertEqual(divorce_before_death("", "12 DEC 1870", "Fred Smith"), "")
        self.assertEqual(divorce_before_death(None, "12 DEC 1870", "Fred Smith"), "")

        # Neither divorced nor dead
        self.assertEqual(divorce_before_death("", None, "Fred Smith"), "")
        self.assertEqual(divorce_before_death(None, "", "Fred Smith"), "")

        # Tests divorces right around deaths
        self.assertNotEqual(divorce_before_death("12 DEC 2130", "11 DEC 2130", "Fred Smith"), "")
        self.assertEqual(divorce_before_death("12 DEC 2130", "12 DEC 2130", "Fred Smith"), "")
        self.assertEqual(divorce_before_death("12 DEC 2130", "13 DEC 2130", "Fred Smith"), "")
        self.assertEqual(divorce_before_death("12 NOV 2130", "01 DEC 2130", "Fred Smith"), "")


    # User Story 10: People must marry at 14 or older
    def test_married_at_14_or_older(self):
        # Not married
        self.assertEqual(married_at_14_or_older("12 DEC 1980", "", "Fred Smith"), "")
        self.assertEqual(married_at_14_or_older("12 DEC 1980", None, "Fred Smith"), "")

        # Not born (?!)
        self.assertEqual(married_at_14_or_older("", "12 DEC 1870", "Fred Smith"), "")
        self.assertEqual(married_at_14_or_older(None, "12 DEC 1870", "Fred Smith"), "")

        # Neither married nor born
        self.assertEqual(married_at_14_or_older("", None, "Fred Smith"), "")
        self.assertEqual(married_at_14_or_older(None, "", "Fred Smith"), "")

        # Tests marriages right around age 14
        self.assertNotEqual(married_at_14_or_older("12 DEC 2130", "11 DEC 2144", "Fred Smith"), "")
        self.assertEqual(married_at_14_or_older("12 DEC 2130", "12 DEC 2144", "Fred Smith"), "")
        self.assertEqual(married_at_14_or_older("12 DEC 2130", "13 DEC 2144", "Fred Smith"), "")
        self.assertEqual(married_at_14_or_older("12 NOV 2130", "01 DEC 2144", "Fred Smith"), "")

    ####US01##### Dates (Birth, Death, Marriage, Divorce) Before Today
    def test_date_lessthan_current(self):
        self.assertEqual(date_before(("12 DEC 1980", "12 DEC 1990", "29 Dec 2020")), True)  # < current date
        self.assertTrue(date_before(("12 DEC 1980", "01 DEC 1990", "29 Dec 2020")), False)  # < current date
        self.assertNotEqual(date_before(("12 DEC 1980", "12 DEC 1990", "29 Dec 2020")), False)  # < current date
        self.assertIn(date_before(("12 DEC 1980", "12 DEC 1990", "29 Dec 2020")), (True, None))  # < current date
        self.assertIsNone(date_before(("12 DEC 1980", "12 DEC 1990", "29Dec 2020")), None)  # invalid date

    def test_date_equalto_current(self):
        current_date = datetime.now().date().strftime('%d %b %Y')
        self.assertEqual(date_before(("12 DEC 1980", "12 DEC 1990", current_date)), True)  # = current date

    def test_date_greaterthan_current(self):
        current_date_plus = datetime.now().date() + timedelta(days=1)
        self.assertEqual(date_before(("12 DEC 1980", current_date_plus.strftime('%d %b %Y'), "29 Dec 2020")),False)  # > current date

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
        
####US04#####
# This test verifies that marriage date is before divorce
    def test_US04_marriage_before_divorce(self):
        self.assertNotEqual(US04_marriage_before_divorce("6 APR 2001", "1 JUL 1999", "Jonathan Sebast"), "")
        self.assertEqual(US04_marriage_before_divorce("5 AUG 1785", "5 Aug 1789", "Eric Sebast"), "")
        self.assertEqual(US04_marriage_before_divorce("12 DEC 1980", "12 NOV 2020", "Eric Sebast"), "")
        self.assertNotEqual(US04_marriage_before_divorce("1 JUL 1990", "5 AUG 1784", "Eric Sebast"), "")
        self.assertNotEqual(US04_marriage_before_divorce("1 JUL 1990", "5 AUG 1784", "Eric Sebast"), "")
        self.assertNotEqual(US04_marriage_before_divorce("12 NOV 1980", "5 AUG 1784", "Eric Sebast"), "")

####US05#####
# This test verifies that marriage date is before death date
    def test_US05_marriage_before_death(self):
        self.assertEqual(US05_marriage_before_death("6 APR 2001", "1 AUG 2019", "Timothy williams"), "")
        self.assertNotEqual(US05_marriage_before_death("5 AUG 1990", "08 AUG 1784", "Eric Sebast"), "")
        self.assertNotEqual(US05_marriage_before_death("12 NOV 2020", "12 Dec 1980", "Eric Sebast"), "")
        self.assertNotEqual(US05_marriage_before_death("1 JUL 1990", "5 AUG 1784", "Eric Sebast"), "")
        self.assertNotEqual(US05_marriage_before_death("1 JUL 1990", "5 AUG 1784", "Eric Sebast"), "")
        self.assertNotEqual(US05_marriage_before_death("12 NOV 1980", "5 AUG 1784", "Eric Sebast"), "")

####US08#####
# This test verifies that the individual is not born before his/her parents were married.
    def test_birth_before_marriage_of_parents(self):
        self.assertEqual(birth_before_marriage_of_parents("6 may 2005", "6 APR 2001", "Eric Sebast"), "")
        self.assertEqual(birth_before_marriage_of_parents("5 sep 1790", "5 AUG 1785", "Eric Sebast"), "")
        self.assertNotEqual(birth_before_marriage_of_parents("6 may 1990", "6 APR 2001", "Eric Sebast"), "")
        self.assertNotEqual(birth_before_marriage_of_parents("5 Jan 1785", "5 AUG 1785", "Eric Sebast"), "")


    ####US22##### Unique ID's --> All individual IDs should be unique and all family IDs should be unique
    def test_unique_ids(self):
        self.assertEqual(unique_ids(("I1", "I5", "F1", "F5")), True) #All Unique ID's
        self.assertEqual(unique_ids(("I1", "I5", "F1", "F5", "I1")), False) #one individual duplicate ID's
        self.assertEqual(unique_ids(("I1", "I5", "F1", "F5", "F1")), False) #one Family duplicate ID's
        self.assertEqual(unique_ids(("I1", "I5", "F1", "F5", "F1", "I5")), False) #Individual and Family duplicate ID's

