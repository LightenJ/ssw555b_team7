from typing import Dict
from unittest import TestCase
from validity_test import younger_than_150, date_before, unique_ids
from validity_test import birthbeforemarriage, unique_name_and_birth_date, unique_families_by_child, order_siblings_by_age, us42_reject_illegitimate_dates
from validity_test import birthbeforedeath, unique_families_by_spouses, us16_male_last_names, us14_multiple_births_less_than_5, us41_accept_partial_dates
from validity_test import divorce_before_death, birth_before_marriage_of_parents, us15_fewer_than_15_siblings,list_of_deceased_individuals,list_orphans
from validity_test import married_at_14_or_older,US04_marriage_before_divorce,US05_marriage_before_death, us18_siblings_shud_not_marry,list_of_anniversaries
from validity_test import correct_gender_for_role, married_first_cousins,list_of_upcoming_birthdays,list_of_recent_deaths,list_of_recent_births,list_of_survivors
from datetime import datetime, timedelta
from data_classes import Individual, Family, Ancestors
from validity_test import get_age, married_to_aunt_or_uncle, birth_should_be_before_death_of_parents, List_large_age_differences
from validity_test import births_should_be_spaced_appropriately, List_multiple_births


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

    # User Story 27: This test verifies that we can accurately determine someone's age, which
    # allows us to include it in the output
    def test_get_age(self):
        ind = Individual("I001")
        ind.birth_d = None
        ind.death_d = None

        # We know nothing
        self.assertEqual(get_age(ind), "Unknown")

        # Known death date, but not birth date
        ind.death_d = "01 jan 1980"
        self.assertEqual(get_age(ind), "Unknown")

        # Garbage death date
        ind.death_d = "Sixscore and fifteen years ago"
        self.assertEqual(get_age(ind), "Unknown")

        # Garbage birth date
        ind.birth_d = "Eightscore and fifteen years ago"
        self.assertEqual(get_age(ind), "Unknown")

        # Ten years old
        ind.birth_d = "01 jan 1980"
        ind.death_d = "01 jan 1990"
        self.assertEqual(get_age(ind), 10)

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


    ####US09#####
    # This test verifies that the individual is not born before his/her parents were married.
    def test_birth_should_be_before_death_of_parents(self):
        june_1_2019 = datetime(2019, 6, 1)
        jan_1_2019 = datetime(2019, 1, 1)
        jan_1_2020 = datetime(2020, 1, 1)
        jan_2_2020 = datetime(2020, 1, 2)

        # Parents not dead
        self.assertEqual(birth_should_be_before_death_of_parents("I1", jan_1_2020, None, None), "")

        # Unknown birth date
        self.assertEqual(birth_should_be_before_death_of_parents("I2", None, jan_1_2020, jan_1_2020), "")

        # Parents died later
        self.assertEqual(birth_should_be_before_death_of_parents("I3", jan_1_2020, jan_2_2020, jan_2_2020), "")

        # Parents died on the same day (possible)
        self.assertEqual(birth_should_be_before_death_of_parents("I4", jan_1_2020, jan_1_2020, jan_1_2020), "")

        # Father died less than and more than 9 months earlier
        self.assertEqual(birth_should_be_before_death_of_parents("I5", jan_2_2020, jan_2_2020, june_1_2019), "")
        self.assertNotEqual(birth_should_be_before_death_of_parents("I6", jan_2_2020, jan_2_2020, jan_1_2019), "")

        # Mother died earlier
        self.assertNotEqual(birth_should_be_before_death_of_parents("I7", jan_2_2020, june_1_2019, jan_2_2020), "")

        # Both died earlier
        self.assertNotEqual(birth_should_be_before_death_of_parents("I8", jan_2_2020, jan_1_2020, jan_1_2019), "")


    ####US13#####
    # This test verifies that births in a family are spaced appropriately.
    def test_births_should_be_spaced_appropriately(self):
        child_births: Dict[str, datetime] = {}

        oct_1_2018 = datetime(2018, 10, 1)
        jan_1_2019 = datetime(2019, 1, 1)
        jan_2_2019 = datetime(2019, 1, 2)
        sept_15_2019 = datetime(2019, 9, 15)

        # No children
        self.assertEqual(births_should_be_spaced_appropriately("F1", child_births), "")

        child_births["I1"] = jan_1_2019

        # One child
        self.assertEqual(births_should_be_spaced_appropriately("F2", child_births), "")

        # Twins, one day apart
        child_births["I2"] = jan_2_2019
        self.assertEqual(births_should_be_spaced_appropriately("F3", child_births), "")

        # 9 month(ish) separation
        child_births["I3"] = sept_15_2019
        self.assertEqual(births_should_be_spaced_appropriately("F4", child_births), "")

        # Too close
        child_births["I4"] = oct_1_2018
        self.assertNotEqual(births_should_be_spaced_appropriately("F5", child_births), "")


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

    ####US23##### Unique name and birth date
    def test_unique_name_and_birth_date(self):
        ind = []

        ind1 = Individual("I01")
        ind1.name = 'emay'
        ind1.birth_d = '27 OCT 1983'
        ind.append(ind1)
        ind2 = Individual("I02")
        ind2.name = 'Test'
        ind2.birth_d = '27 OCT 1983'
        ind.append(ind2)

        self.assertEqual(unique_name_and_birth_date(ind), [])#different Name but same date of birth

        ind4 = Individual("I04")
        ind4.name = 'Test1'
        ind4.birth_d = '27 OCT 1980'
        ind.append(ind4)

        self.assertEqual(unique_name_and_birth_date(ind), [])#different name  and different date of birth

        ind3 = Individual("I03")
        ind3.name = 'emay'
        ind3.birth_d = '27 OCT 1983'
        ind.append(ind3)
        self.assertEqual(unique_name_and_birth_date(ind), [('emay', '27 OCT 1983')]) #Duplicate Name and date of birth

    ####US24##### Unique families by spouses
    def test_unique_families_by_spouses(self):

        ind1 = Individual("I01")
        ind1.name = 'HUS1'
        ind2 = Individual("I02")
        ind2.name = 'WIFE1'
        ind3 = Individual("I03")
        ind3.name = 'HUS2'
        ind4 = Individual("I04")
        ind4.name = 'WIFE2'
        fam1 = Family('F01')
        fam1.hus_id = 'I01'
        fam1.wife_id = 'I02'
        fam1.marriage_d = '22 FEB 2013'
        fam2 = Family('F02')
        fam2.hus_id = 'I03'
        fam2.wife_id = 'I04'
        fam2.marriage_d = '23 FEB 2013'
        fam3 = Family('F03')
        fam3.hus_id = 'I01'
        fam3.wife_id = 'I02'
        fam3.marriage_d = '22 FEB 2013'
        self.assertEqual(unique_families_by_spouses((ind1, ind2, ind3, ind4), (fam1, fam2)), [])#
        self.assertEqual(unique_families_by_spouses((ind1, ind2, ind3, ind4), (fam1, fam2, fam3)), [('22 FEB 2013', 'WIFE1')])#
        fam3.marriage_d = '23 FEB 2013'
        self.assertEqual(unique_families_by_spouses((ind1, ind2, ind3, ind4), (fam1, fam2, fam3)), [])#

    ####US25##### Unique families by spouse
    def test_unique_families_by_child(self):
        ind1 = Individual("I01")
        ind1.name = 'Child1'
        ind1.birth_d = '27 OCT 1983'
        ind2 = Individual("I02")
        ind2.name = 'Child2'
        ind2.birth_d = '26 OCT 1985'

        ind3 = Individual("I03")
        ind3.name = 'Child3'
        ind3.birth_d = '25 OCT 1982'

        ind4 = Individual("I04")
        ind4.name = 'Child4'
        ind4.birth_d = '26 OCT 1983'

        fam1 = Family('F01')
        fam1.children = ['I01', 'I02', 'I03', 'I04']
        fam2 = Family('F02')
        fam2.children = ['I03', 'I04']
        fam3 = Family('F03')
        fam3.children = 'I01'

        self.assertEqual(unique_families_by_child((ind1, ind2, ind3, ind4), (fam1, fam2)), [])  #
        ind2.name = 'Child1'
        ind2.birth_d = '27 OCT 1983'
        self.assertEqual(unique_families_by_child((ind1, ind2, ind3, ind4), (fam1, fam2, fam3)),
                         [[('27 OCT 1983', 'Child1'), 'F01']])  #
        ind2.birth_d = '27 OCT 2000'
        ind2.name = 'Child5'

        self.assertEqual(unique_families_by_child((ind1, ind2, ind3, ind4), (fam1, fam2, fam3)), [])  #
        ind2.name = 'Child1'
        ind2.birth_d = '25 OCT 1983'

        self.assertEqual(unique_families_by_child((ind1, ind2, ind3, ind4), (fam1, fam2, fam3)), [])  #

    ####US28##### Order siblings by age
    def test_order_siblings_by_age(self):

        ind1 = Individual("I01")
        ind1.name = 'Child1'
        ind1.birth_d = '27 OCT 1983'
        ind2 = Individual("I02")
        ind2.name = 'Child2'
        ind2.birth_d = '26 OCT 1985'

        ind3 = Individual("I03")
        ind3.name = 'Child3'
        ind3.birth_d = '25 OCT 1982'

        ind4 = Individual("I04")
        ind4.name = 'Child4'
        ind4.birth_d = '26 OCT 1983'

        fam1 = Family('F01')
        fam1.children = ['I01', 'I02', 'I03', 'I04']
        fam2 = Family('F02')
        fam2.children = ['I03', 'I04']
        fam3 = Family('F03')
        fam3.children = 'I01'

        self.assertEqual(order_siblings_by_age((ind1, ind2, ind3, ind4), (fam1, fam2)), [[('25 OCT 1982', 'Child3'), ('26 OCT 1983', 'Child4'), ('27 OCT 1983', 'Child1'), ('26 OCT 1985', 'Child2'), 'F01'],[('25 OCT 1982', 'Child3'), ('26 OCT 1983', 'Child4'), 'F02']])#
        ind2.name = 'Child1'
        ind2.birth_d = '27 OCT 1983'
        #duplicate name and birthday
        self.assertEqual(order_siblings_by_age((ind1, ind2, ind3, ind4), (fam1, fam2, fam3)), [[('25 OCT 1982', 'Child3'), ('26 OCT 1983', 'Child4'), ('27 OCT 1983', 'Child1'), ('27 OCT 1983', 'Child1'), 'F01'], [('25 OCT 1982', 'Child3'), ('26 OCT 1983', 'Child4'), 'F02']])#
        ind2.name = 'Child2'
        ind2.birth_d = '27 NOV 1983'
        #same day and year but different month
        self.assertEqual(order_siblings_by_age((ind1, ind2, ind3, ind4), (fam1, fam3)), [[('25 OCT 1982', 'Child3'),('26 OCT 1983', 'Child4'),('27 OCT 1983', 'Child1'),('27 NOV 1983', 'Child2'),'F01']])#
        ind2.birth_d = '25 OCT 1983'
        fam1.children = []
        #family with no Children
        self.assertEqual(order_siblings_by_age((ind1, ind2, ind3, ind4), (fam1,fam3 )), [])#

    ####US29#####
    # This test verifies that these individuals are deceased in the input Gedcom file
    def test_list_of_deceased_individuals(self):
        ind1 = Individual("I8")
        ind1.name = 'IND1'
        ind2 = Individual("I12")
        ind2.name = 'IND2'
        ind3 = Individual("I6")
        ind3.name = 'IND3'
        ind4 = Individual("I16")
        ind4.name = 'IND4'
        ind5 = Individual("I15")
        ind5.name = 'IND5'
        self.assertFalse(list_of_deceased_individuals((ind1,ind3)), "")
        self.assertFalse(list_of_deceased_individuals((ind2, ind5)), "")


    ####US33#####
    # This test verifies that these individuals are orphans
    def test_list_orphans(self):
        ind1 = Individual("I5")
        ind1.name = 'IND1'
        ind2 = Individual("I5")
        ind2.name = 'IND2'
        ind3 = Individual("I7")
        ind3.name = 'IND3'
        ind4 = Individual("I5")
        ind4.name = 'IND4'
        fam1 = Family('F2')
        fam1.children = ['I5', 'I5']
        fam2 = Family('F2')
        fam2.children = ['I5', 'I5']
        fam3 = Family('F03')
        fam3.children = 'I01'
        self.assertFalse(list_orphans([ind1,ind2], [fam1,fam2]),"")
        self.assertFalse(list_orphans((ind1, ind2, ind3, ind4), (fam1, fam2)), "")
        self.assertFalse(list_orphans((ind3, ind4), (fam1, fam3)), "")
        self.assertFalse(list_orphans((ind1, ind2,ind4), (fam2, fam3)), "")
    ####US35#####
    # This test verifies that these individuals are dead within last 30 days or not
    def test_list_of_recent_births(self):
        ind1 = Individual("I01")
        ind1.name = 'HUS1'
        ind2 = Individual("I02")
        ind2.name = 'WIFE1'
        ind3 = Individual("I03")
        ind3.name = 'HUS2'
        ind4 = Individual("I04")
        ind4.name = 'WIFE2'
        self.assertTrue(list_of_recent_births(["15 APR 2021"], (ind1, ind2, ind3, ind4)), "")
        self.assertFalse(list_of_recent_births(["25 MAY 2021"], (ind1, ind2, ind3, ind4)), "")
        self.assertTrue(list_of_recent_births(["14 APR 2021"], (ind1, ind2, ind3, ind4)), "")
        self.assertFalse(list_of_recent_births(["5 APR 1985"], (ind1, ind2, ind3, ind4)), "")

    ####US36#####
    # This test verifies that these individuals are dead within last 30 days or not
    def test_list_of_recent_deaths(self):
        ind1 = Individual("I01")
        ind1.name = 'HUS1'
        ind2 = Individual("I02")
        ind2.name = 'WIFE1'
        ind3 = Individual("I03")
        ind3.name = 'HUS2'
        ind4 = Individual("I04")
        ind4.name = 'WIFE2'
        self.assertTrue(list_of_recent_deaths(["12 APR 2021"], (ind1, ind2, ind3, ind4)), "")
        self.assertFalse(list_of_recent_deaths(["25 MAY 2021"], (ind1, ind2, ind3, ind4)), "")
        self.assertTrue(list_of_recent_deaths(["15 APR 2021"], (ind1, ind2, ind3, ind4)), "")
        self.assertFalse(list_of_recent_deaths(["5 APR 1985"], (ind1, ind2, ind3, ind4)), "")

        ####US37#####
        # This test verifies that these individuals are survived within last 30 days or not

    def test_list_of_survivors(self):
        ind1 = Individual("I109")
        ind1.name = 'HUS1'
        ind2 = Individual("I100")
        ind2.name = 'WIFE1'
        ind3 = Individual("I209")
        ind3.name = 'HUS2'
        ind4 = Individual("I4")
        ind4.name = 'WIFE2'
        fam1 = Family('F100')
        fam1.children = ['I01', 'I02', 'I03', 'I04']
        fam2 = Family('F102')
        fam2.children = ['I03', 'I04']
        fam3 = Family('F100')
        fam3.children = 'I01'
        self.assertFalse(list_of_survivors((ind1, ind2),(fam1, fam2)))
        self.assertFalse(list_of_survivors((ind1, ind2, ind3, ind4),(fam1, fam2)))
        self.assertFalse(list_of_survivors((ind1, ind2, ind3, ind4,),(fam1,fam2, fam3)))
        self.assertFalse(list_of_survivors((ind1, ind2, ind3, ind4),(fam1,fam2, fam3)))

    ####US38#####
    # This test verifies that these individuals birthday is in next 30 days or not
    def test_list_of_upcoming_birthdays(self):
        ind1 = Individual("I01")
        ind1.name = 'HUS1'
        ind2 = Individual("I02")
        ind2.name = 'WIFE1'
        ind3 = Individual("I03")
        ind3.name = 'HUS2'
        ind4 = Individual("I04")
        ind4.name = 'WIFE2'
        self.assertTrue(list_of_upcoming_birthdays(["18 APR 2021"], (ind1, ind2, ind3, ind4)), "")
        self.assertFalse(list_of_upcoming_birthdays(["25 MAY 2021"], (ind1, ind2, ind3, ind4)), "")
        self.assertTrue(list_of_upcoming_birthdays(["16 APR 2021"], (ind1, ind2, ind3, ind4)), "")
        self.assertFalse(list_of_upcoming_birthdays(["5 JAN 1985"], (ind1, ind2, ind3, ind4)), "")
        self.assertFalse(list_of_upcoming_birthdays(["5 DEC 1985"], (ind1, ind2, ind3, ind4)), "")
        ####US38#####
        # This test verifies that these individuals birthday is in next 30 days or not

    def test_list_of_anniversaries(self):
        ind1 = Individual("I01")
        ind1.name = 'HUS1'
        ind2 = Individual("I02")
        ind2.name = 'WIFE1'
        ind3 = Individual("I03")
        ind3.name = 'HUS2'
        ind4 = Individual("I04")
        ind4.name = 'WIFE2'
        self.assertTrue(list_of_anniversaries(["18 APR 2021"], (ind1, ind2, ind3, ind4)), "")
        self.assertFalse(list_of_anniversaries(["25 MAY 2021"], (ind1, ind2, ind3, ind4)), "")
        self.assertTrue(list_of_anniversaries(["16 APR 2021"], (ind1, ind2, ind3, ind4)), "")
        self.assertFalse(list_of_anniversaries(["5 JAN 1985"], (ind1, ind2, ind3, ind4)), "")
        self.assertFalse(list_of_anniversaries(["5 DEC 1985"], (ind1, ind2, ind3, ind4)), "")

    # User Story 21: Correct gender for role
    def test_correct_gender_for_role(self):

        ind = Individual("TestID")
        family = Family("FAM001")
        family.wife_id = "WIFEIND"
        family.hus_id = "HUSIND"
        ind.name = "A name"

        # Husband cases
        ind.ind_id = "HUSIND"

        # Valid husband cases
        ind.sex = "M"
        self.assertEqual(correct_gender_for_role(ind, family), "")
        ind.sex = "m"
        self.assertEqual(correct_gender_for_role(ind, family), "")

        # Unrecognized gender cases
        ind.sex = None
        self.assertNotEqual(correct_gender_for_role(ind, family), "")
        ind.sex = "Male"
        self.assertNotEqual(correct_gender_for_role(ind, family), "")
        ind.sex = "Banana"
        self.assertNotEqual(correct_gender_for_role(ind, family), "")

        # Illegal gender cases
        ind.sex = "F"
        self.assertNotEqual(correct_gender_for_role(ind, family), "")
        ind.sex = "f"
        self.assertNotEqual(correct_gender_for_role(ind, family), "")

        # Wife cases
        ind.ind_id = "WIFEIND"

        # Valid wife cases
        ind.sex = "F"
        self.assertEqual(correct_gender_for_role(ind, family), "")
        ind.sex = "f"
        self.assertEqual(correct_gender_for_role(ind, family), "")

        # Unrecognized gender cases
        ind.sex = None
        self.assertNotEqual(correct_gender_for_role(ind, family), "")
        ind.sex = "Female"
        self.assertNotEqual(correct_gender_for_role(ind, family), "")
        ind.sex = "Banana"
        self.assertNotEqual(correct_gender_for_role(ind, family), "")

        # Illegal gender cases
        ind.sex = "M"
        self.assertNotEqual(correct_gender_for_role(ind, family), "")
        ind.sex = "m"
        self.assertNotEqual(correct_gender_for_role(ind, family), "")

    # User Story 19: Married first cousins
    def test_married_first_cousins(self):

        ancestor_dict: Dict[str, Ancestors] = {}
        family = Family("FAM001")

        family.fam_id = "FAM01"
        family.wife_id = "WIFE01"
        family.hus_id = "HUS01"

        # No ancestors exist
        self.assertEqual(married_first_cousins(family, ancestor_dict), "")

        # Only parents known
        ancestor_dict[family.wife_id] = Ancestors()
        ancestor_dict[family.wife_id].parents = {"MOM1", "DAD1"}
        ancestor_dict[family.hus_id] = Ancestors()
        ancestor_dict[family.hus_id].parents = {"MOM2", "DAD2"}
        self.assertEqual(married_first_cousins(family, ancestor_dict), "")

        # Unrelated grandparents
        ancestor_dict[family.wife_id].grandparents = {"GMA1", "GPA1", "GMA2", "GPA2"}
        ancestor_dict[family.hus_id].grandparents = {"GMA3", "GPA3", "GMA4", "GPA4"}
        self.assertEqual(married_first_cousins(family, ancestor_dict), "")

        # One shared grandparent
        ancestor_dict[family.wife_id].grandparents = {"GMA3", "GPA1", "GMA2", "GPA2"}
        self.assertNotEqual(married_first_cousins(family, ancestor_dict), "")

        # Shared grandparent but same parents
        ancestor_dict[family.wife_id].parents = {"MOM2", "DAD1"}
        self.assertEqual(married_first_cousins(family, ancestor_dict), "")

        # User Story 20: Aunts/uncles married to nephews/nieces
    def test_married_to_aunt_or_uncle(self):
        ancestor_dict: Dict[str, Ancestors] = {}
        family = Family("FAM001")

        family.fam_id = "FAM01"
        family.wife_id = "WIFE01"
        family.hus_id = "HUS01"

        # No ancestors exist
        self.assertEqual(married_to_aunt_or_uncle(family, ancestor_dict), "")

        # Only parents known
        ancestor_dict[family.wife_id] = Ancestors()
        ancestor_dict[family.wife_id].parents = {"MOM1", "DAD1"}
        ancestor_dict[family.hus_id] = Ancestors()
        ancestor_dict[family.hus_id].parents = {"MOM2", "DAD2"}
        self.assertEqual(married_to_aunt_or_uncle(family, ancestor_dict), "")

        # Parents' siblings are unrelated to the married parties
        ancestor_dict[family.wife_id].aunts_and_uncles = {"AUNT1", "AUNT2", "UNCLE1", "UNCLE2"}
        ancestor_dict[family.hus_id].aunts_and_uncles = {"AUNT3", "AUNT4", "UNCLE3", "UNCLE4"}
        self.assertEqual(married_to_aunt_or_uncle(family, ancestor_dict), "")

        # Wife's uncle is the husband
        ancestor_dict[family.wife_id].aunts_and_uncles = {"AUNT01", "AUNT02", "HUS01"}
        self.assertNotEqual(married_to_aunt_or_uncle(family, ancestor_dict), "")

        # Husband's aunt is the wife
        ancestor_dict[family.wife_id].aunts_and_uncles = {}
        ancestor_dict[family.hus_id].aunts_and_uncles = {"UNCLE01", "UNCLE02", "WIFE01"}
        self.assertNotEqual(married_to_aunt_or_uncle(family, ancestor_dict), "")


    # User Story 18: us18_siblings_shud_not_marry
    def test_us18_siblings_shud_not_marry(self):
        ancestor_dict: Dict[str, Ancestors] = {}
        family = Family("FAM001")
        family.fam_id = "FAM01"
        family.wife_id = "WIFE01"
        family.hus_id = "HUS01"

        # No ancestors exist
        self.assertEqual(us18_siblings_shud_not_marry(family, ancestor_dict), "")

        # Only parents known
        ancestor_dict[family.wife_id] = Ancestors()
        ancestor_dict[family.wife_id].parents = {"MOM1", "DAD1"}
        ancestor_dict[family.hus_id] = Ancestors()
        ancestor_dict[family.hus_id].parents = {"MOM2", "DAD2"}
        self.assertEqual(us18_siblings_shud_not_marry(family, ancestor_dict), "")

        # Unrelated grandparents
        ancestor_dict[family.wife_id].grandparents = {"GMA1", "GPA1", "GMA2", "GPA2"}
        ancestor_dict[family.hus_id].grandparents = {"GMA3", "GPA3", "GMA4", "GPA4"}
        self.assertEqual(us18_siblings_shud_not_marry(family, ancestor_dict), "")

        # # One shared grandparent
        # ancestor_dict[family.wife_id].grandparents = {"GMA3", "GPA1", "GMA2", "GPA2"}
        # self.assertNotEqual(us18_siblings_shud_not_marry(family, ancestor_dict), "")

        # Shared grandparent but same parents
        ancestor_dict[family.wife_id].parents = {"MOM1", "DAD1"}
        self.assertEqual(us18_siblings_shud_not_marry(family, ancestor_dict), "")

    # User Story 15: us15_fewer_than_15_siblings
    def test_us15_fewer_than_15_siblings(self):
        family = Family("FAM001")
        family.children = ["CHIL1", "CHIL2", "CHIL3", "CHIL4", "CHIL5", "CHIL6", "CHIL7", "CHIL8",
                           "CHIL9", "CHIL10", "CHIL11", "CHIL12", "CHIL13", "CHIL14", "CHIL15", "CHIL16", ]

        self.assertTrue(us15_fewer_than_15_siblings(family), "")
        
        family = Family("FAM002")
        family.children = ["CHIL1", "CHIL2", "CHIL3", "CHIL4", "CHIL5"]
        self.assertFalse(us15_fewer_than_15_siblings(family), "")
        
    # User story 16: us16_male_last_names
    def test_us16_male_last_names(self):
        ind = []
        fam = []
        fam1 = Family('F01')
        fam1.hus_id = 'I01'
        fam1.children = ["chil1", "chil2"]
        fam2 = Family('F02')
        fam2.hus_id = 'I03'
        fam1.children = ["chil1", "chil2"]
        ind1 = Individual("I01")
        ind1.id = 'I01'
        ind1.name = 'HUS1 lname'
        ind2 = Individual("I02")
        ind2.name = 'rob kname'
        ind2.sex = 'M'

        # self.assertEqual(us16_male_last_names((ind1, ind2, ind3, ind4), (fam1, fam2)), [])
        self.assertEqual(us16_male_last_names((ind1, ind2), (fam1, fam2)), "")
        self.assertEqual(us16_male_last_names((ind1), (fam1, fam2)), "")

    # User story 14, Multiple births <= 5
    def test_us14_multiple_births_less_than_5(self):
        fam1 = Family("FAM001")
        fam1.children = ["I01", "I02", "I03", "I04", "I05", "I06"]
        fam2 = Family("FAM001")
        fam2.children = ["I01", "I02", "I03", "I04", "I05", "I06"]
        ind1 = Individual("I01")
        ind1.birth_d = '27 OCT 1999'
        ind2 = Individual("I02")
        ind2.birth_d = '27 OCT 1999'
        ind3 = Individual("I03")
        ind3.birth_d = '27 OCT 1999'
        ind4 = Individual("I04")
        ind4.birth_d = '27 OCT 1999'
        ind5 = Individual("I05")
        ind5.birth_d = '27 OCT 1999'
        ind6 = Individual("I06")
        ind6.birth_d = '27 OCT 1999'
        self.assertNotEqual(us14_multiple_births_less_than_5((ind1, ind2, ind3, ind4, ind5, ind6), (fam1, fam2)), "")
        self.assertEqual(us14_multiple_births_less_than_5((ind1, ind2, ind3, ind4, ind5), (fam1, fam2)), "")
        self.assertEqual(us14_multiple_births_less_than_5((ind1, ind2, ind3, ind4), (fam1, fam2)), "")

    ####US34#### List large age differences
    def test_List_large_age_differences(self):
        ind1 = Individual("I01")
        ind1.name = 'HUS1'
        ind1.birth_d = '5 Jun 1950'
        ind2 = Individual("I02")
        ind2.name = 'WIFE1'
        ind2.birth_d = '5 Mar 1955'
        ind3 = Individual("I03")
        ind3.name = 'HUS2'
        ind3.birth_d = '5 Jun 1990'
        ind4 = Individual("I04")
        ind4.name = 'WIFE2'
        ind4.birth_d = '5 Jun 1990'
        fam1 = Family('F01')
        fam1.hus_id = 'I01'
        fam1.wife_id = 'I02'
        fam1.marriage_d = '22 FEB 1980'
        fam2 = Family('F02')
        fam2.hus_id = 'I03'
        fam2.wife_id = 'I04'
        fam2.marriage_d = '23 FEB 2021'
        self.assertEqual(List_large_age_differences((ind1, ind2, ind3, ind4), (fam1, fam2)),[])
        # equal to 2*
        ind4.birth_d = '5 Jun 1960'
        self.assertEqual(List_large_age_differences((ind1, ind2, ind3, ind4), (fam1, fam2)),[])

        #grether than 2* Hus
        ind4.birth_d = '5 Jun 1959'
        self.assertEqual(List_large_age_differences((ind1, ind2, ind3, ind4), (fam1, fam2)),[['wife older', '23 FEB 2021','WIFE2', 61, 'HUS2', 30]])

        #grether than 2* Wife
        ind3.birth_d = '5 Jun 1959'
        ind4.birth_d = '5 Jun 1990'
        self.assertEqual(List_large_age_differences((ind1, ind2, ind3, ind4), (fam1, fam2)),[['Husband older', '23 FEB 2021', 'HUS2', 61, 'WIFE2', 30]])

    # User story 32, List multiple births
    def test_List_multiple_births(self):
        ind1 = Individual("I01")
        ind1.name = 'HUS1'
        ind1.birth_d = '5 Jun 1950'
        ind2 = Individual("I02")
        ind2.name = 'WIFE1'
        ind2.birth_d = '5 Mar 1955'
        ind3 = Individual("I03")
        ind3.name = 'HUS2'
        ind3.birth_d = '5 Jun 1990'
        ind4 = Individual("I04")
        ind4.name = 'WIFE2'
        ind4.birth_d = '5 Jun 1990'
        ind5 = Individual("I05")
        ind6 = Individual("I06")
        ind5.name = 'Child1'
        ind6.name = 'Child2'
        ind7 = Individual("I07")
        ind8 = Individual("I08")
        ind9 = Individual("I09")
        ind7.name = 'Child7'
        ind8.name = 'Child8'
        ind9.name = 'Child8'
        ind7.birth_d = '5 Jun 1990'
        ind8.birth_d = '5 Jun 1991'
        ind9.birth_d = '5 Jun 1991'

        fam1 = Family('F01')
        fam1.hus_id = 'I01'
        fam1.wife_id = 'I02'
        fam1.marriage_d = '22 FEB 1980'
        fam2 = Family('F02')
        fam2.hus_id = 'I03'
        fam2.wife_id = 'I04'
        fam2.children = ["I06", "I07"]
        fam2.marriage_d = '23 FEB 2021'

        fam3 = Family('F03')
        fam3.hus_id = 'I06'
        fam3.wife_id = 'I05'
        fam3.marriage_d = '22 FEB 1980'
        fam3.children = ["I07", "I08"]

        self.assertEqual(List_multiple_births((ind1, ind2, ind3, ind4, ind5, ind6, ind7, ind8), (fam1, fam2, fam3)),"")
        ind8.birth_d = '5 Jun 1990'

        self.assertEqual(List_multiple_births((ind1, ind2, ind3, ind4,  ind5, ind6, ind7, ind8), (fam1, fam2, fam3)),[['5 Jun 1990', 'Child7'] , ['5 Jun 1990', 'Child8']])
        
        
         # # User story 42, Reject illegitimate dates
    def test_us42_reject_illegitimate_dates(self):


        ind = {'@I1@': {'Name': 'Smit /Nawar/', 'Gender': 'M', 'BIRTH DATE': '31 MAY 2023', 'DEATH DATE': '37 OCT 2098',
                        'FAMS': {1: '@F1@'}, 'FAMC': {1: '@I4@'}},
               '@I2@': {'Name': 'Yi Xie /Nawar/', 'Gender': 'F', 'BIRTH DATE': '32 MAY 2023', 'DEATH DATE': '39 MAY 2067',
                        'FAMS': {1: '@F1@'}, 'FAMC': {1: '@I4@'}}}
        fam = {'@F1@': {'Married': '32 OCT 2065', 'Divorced': '43 MAY 2023', 'Husband Id': '@I1@',
                        'Husband Name': 'Smit /Nawar/', 'Wife Id': '@I2@', 'Wife Name': 'Yi Xie /Nawar/',
                        'Children': {1: '@I4@'}}}

        # for i in range(1):
        self.assertNotEqual(us42_reject_illegitimate_dates(ind), "True")

    # # # User story 41, Accept partial dates
    def test_us41_accept_partial_dates(self):
        fam = {'@F1@': {'BIRTH DATE': 'None', 'Husband Id': '@I1@',
                        'Husband Name': 'Smit /Nawar/', 'Wife Id': '@I2@', 'Wife Name': 'Yi Xie /Nawar/',
                        'Children': {1: '@I4@'}},
               '@F2@': {'Married': '1991-09', 'Husband Id': '@I1@',
                        'Husband Name': 'Ron /Nawar/', 'Wife Id': '@I2@', 'Wife Name': 'Yi Xie /Nawar/',
                        'Children': {1: '@I4@'}}
               }
        ind = {'@I1@': {'Name': 'Smit /Nawar/', 'Gender': 'M', 'BIRTH DATE': '2000-01-77', 'DEATH DATE': '2000-08-322',
                        'FAMS': {1: '@F1@'}, 'FAMC': {1: '@I4@'}},
               '@I2@': {'Name': 'Yi Xie /Nawar/', 'Gender': 'F', 'BIRTH DATE': '3023-33-04', 'DEATH DATE': '2000-08-05',
                        'FAMS': {1: '@F1@'}, 'FAMC': {1: '@I4@'}}}

        # for i in range(1):
        self.assertNotEqual(us41_accept_partial_dates(ind), "True")

