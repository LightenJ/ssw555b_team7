"""
#===========================================================================================#
Subject         : SSW -555(Agile Methods for Software Development)
Assignment      : P04: First Sprint
Script Author   : Team#7
Date            : 02/27/2021
Script Name     : validity_test.py
#===========================================================================================#

Purpose:
--------
Test that the input file is valid, and report any errors.
---------------------------------------------------------------------------------------------

"""

import datetime
from datetime import datetime
from datetime import date
from data_classes import Individual
from data_classes import Family
from typing import List


def check_valid(individuals: List[Individual], families: List[Family]):
    error_statuses = []
    temp_error_statuses = []
    individual:Individual
    for individual in individuals:
        temp_error_statuses = check_valid_individual(individual)

        # Append any errors we found to the top level error_statuses
        for error_msg in temp_error_statuses:
            error_statuses.append(error_msg)

        for family in families:

            # Currently, only checking for husbands and wives being part of the family.  If
            # a story needs to check children in a family, we'd have to add a case for finding
            # children from a family.
            if family.hus_id == individual.ind_id or family.wife_id == individual.ind_id:
                temp_error_statuses = check_valid_individual_spouse(individual, family)

                # Append any errors we found to the top level error_statuses
                for error_msg in temp_error_statuses:
                    error_statuses.append(error_msg)

    return error_statuses


def check_valid_individual(individual: Individual):
    error_statuses = []
    birth_date = individual.birth_d
    death_date = individual.death_d
    my_full_name = individual.name
    error_text = younger_than_150(birth_date, death_date, my_full_name)
    if len(error_text) > 0:
        error_statuses.append(error_text)
    error_text = birthbeforedeath(birth_date, death_date, my_full_name)
    if len(error_text) > 0:
        error_statuses.append(error_text)

    return error_statuses


def check_valid_individual_spouse(individual: Individual , family: Family):
    error_statuses = []
    my_full_name = individual.name
    birth_date = individual.birth_d
    death_date = individual.death_d
    marriage_date = family.marriage_d
    divorce_date = family.divorce_d
    error_text = birthbeforemarriage(birth_date, marriage_date, my_full_name)
    if len(error_text) > 0:
        error_statuses.append(error_text)
    error_text = divorce_before_death(divorce_date, death_date, my_full_name)
    if len(error_text) > 0:
        error_statuses.append(error_text)
    return error_statuses


def younger_than_150(birth_date: str, death_date: str, name: str):
    my_error = ""

    if death_date is None or len(death_date) == 0:   # Individual has not died, check against current date
        death_date = date.today()
        birth_date = datetime.strptime(birth_date, '%d %b %Y')
    else:                      # Individual has died, check birth against death
        death_date = datetime.strptime(death_date, '%d %b %Y')
        birth_date = datetime.strptime(birth_date, '%d %b %Y')

    if year_difference(death_date, birth_date) >= 150:
        my_error = "Error: US#07: " + name + " is more than 150 years old.\n"

    return my_error


def year_difference(date1: datetime.date, date2: datetime.date):
    years_diff = date1.year - date2.year
    if date2.month > date1.month or (date1.month == date2.month and date2.day > date1.day):
        years_diff = years_diff - 1
    return years_diff


def day_difference(late_date: datetime.date, early_date: datetime.date):
    return (late_date - early_date).days

####US01##### Dates (Birth, Death, Marriage, Divorce) Before Today
def date_before(dates):

    valid = False
    try:
        for date in dates:
            if date != None:
                f_date = datetime.strptime(date.rstrip(), '%d %b %Y').date()
                c_date = datetime.now().date()
                if f_date > c_date:
                    valid = True
    except: valid = None

    return valid

####US02#####
def birthbeforemarriage(birth_date: str, marriage_date: str, name: str):
    my_error = ""
    if marriage_date is None or len(marriage_date) == 0:   # Individual is not married, check against current date
        marriage_date = date.today()
        birth_date = datetime.strptime(birth_date, '%d %b %Y')
    else:
        marriage_date = datetime.strptime(marriage_date, '%d %b %Y')
        birth_date = datetime.strptime(birth_date, '%d %b %Y')

    if year_difference(marriage_date, birth_date) < 0:
        my_error = "Error:INDIVIDUAL: US#02: Individual " + name + " was married before they were born.\n"
    return my_error

####US03#####
def birthbeforedeath(birth_date: str, death_date: str, name: str):
    my_error = ""
    if death_date is None or len(death_date) == 0:  # Individual is not dead, check against current date
        death_date = date.today()
        birth_date = datetime.strptime(birth_date, '%d %b %Y')
    else:  # Individual has died, check birth against death
        death_date = datetime.strptime(death_date, '%d %b %Y')
        birth_date = datetime.strptime(birth_date, '%d %b %Y')

    if year_difference(birth_date, death_date) > 0:
        my_error = "Error:INDIVIDUAL: US#02: Individual " + name + " died before they were born.\n"
    return my_error


####US04####
def US04_marriage_before_divorce(marriage_date: str, divorce_date: str):
    my_error = ""
    if divorce_date is None or len(divorce_date) == 0:  # Husband and wife are not divorced, check against current date
        divorce_date = date.today()
        marriage_date = datetime.strptime(marriage_date, '%d %b %Y')
    else:  # Individual has died, check birth against death
        divorce_date = datetime.strptime(divorce_date, '%d %b %Y')
        marriage_date = datetime.strptime(marriage_date, '%d %b %Y')

    if year_difference(marriage_date, divorce_date) > 0:
        my_error = "Error: US#04: Family: Married before divorce date.\n"
    return my_error


# User Story 6, divorce must be before (okay, or on the day of) death.
def divorce_before_death(divorce_date: str, death_date: str, name: str):
    my_error = ""
    if death_date is None or len(death_date) == 0 or divorce_date is None or len(divorce_date) == 0:
        # Either hasn't died or hasn't divorced, so no way to be invalid
        pass
    else:
        divorce_date = datetime.strptime(divorce_date, '%d %b %Y')
        death_date = datetime.strptime(death_date, '%d %b %Y')
        if day_difference(death_date, divorce_date) < 0:
            my_error = "Error: US#06: Individual " + name + " was divorced after they died.\n"
    return my_error
