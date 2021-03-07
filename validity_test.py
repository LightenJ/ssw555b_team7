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

    #Restarting through families to process all children
    for family in families:
        # Find all the children in a family
        for child in family.children:
            for temp_ind in individuals:
                if child == temp_ind.ind_id:
                    temp_error_statuses = check_valid_individual_child(temp_ind, family)

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


def check_valid_individual_spouse(individual: Individual, family: Family):
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
    error_text = married_at_14_or_older(birth_date, marriage_date, my_full_name)
    if len(error_text) > 0:
        error_statuses.append(error_text)
    error_text = US04_marriage_before_divorce(marriage_date, divorce_date, my_full_name)
    if len(error_text) > 0:
        error_statuses.append(error_text)
    error_text = US05_marriage_before_death(marriage_date, death_date, my_full_name)
    if len(error_text) > 0:
        error_statuses.append(error_text)
    return error_statuses


def check_valid_individual_child(individual: Individual, family: Family):
    error_statuses = []
    my_full_name = individual.name
    birth_date = individual.birth_d
    death_date = individual.death_d
    marriage_date = family.marriage_d
    divorce_date = family.divorce_d
    error_text = birth_before_marriage_of_parents(birth_date, marriage_date, my_full_name)
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
        my_error = "Error:INDIVIDUAL: US#03: Individual " + name + " died before they were born.\n"
    return my_error


####US04####
def US04_marriage_before_divorce(marriage_date: str, divorce_date: str, name: str):
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


####US05####
def US05_marriage_before_death(marriage_date: str, death_date: str, name: str):
    my_error = ""
    if death_date is None or len(death_date) == 0:  # Not dead, check against current date
        death_date = date.today()
        marriage_date = datetime.strptime(marriage_date, '%d %b %Y')
    else:  
        death_date = datetime.strptime(death_date, '%d %b %Y')
        marriage_date = datetime.strptime(marriage_date, '%d %b %Y')

    if year_difference(marriage_date, death_date) > 0:
        my_error = "Error: US#05: Family: Married before death.\n"
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


# User story 10, marriage before 14 - married persons must be at least 14 when married.
def married_at_14_or_older(birth_date: str, marriage_date: str, name: str):
    my_error = ""

    if marriage_date is None or len(marriage_date) == 0 or birth_date is None or len(birth_date) == 0:
        # Don't check if no marriage date or no birth date is available - though this is for a family, so
        # those shouldn't really be possible.
        pass
    else:                      # Individual has died, check birth against death
        marriage_date = datetime.strptime(marriage_date, '%d %b %Y')
        birth_date = datetime.strptime(birth_date, '%d %b %Y')
        if year_difference(marriage_date, birth_date) < 14:
            my_error = "Error: US#10: " + name + " was married when younger than 14.\n"

    return my_error


# User story 8, check for a child born before his or her parents were married.
def birth_before_marriage_of_parents(birth_date: str, marriage_date: str, name: str):
    my_error = ""

    if marriage_date is None or len(marriage_date) == 0 or birth_date is None or len(birth_date) == 0:
        # Don't check if no marriage date or no birth date is available - though this is for a family, so
        # those shouldn't really be possible.
        pass
    else:                      # See if the parents were married before the individual was born
        marriage_date = datetime.strptime(marriage_date, '%d %b %Y')
        birth_date = datetime.strptime(birth_date, '%d %b %Y')
        if day_difference(birth_date, marriage_date) < 0:
            my_error = "Error: US#08: " + name + " was born before his/her parents were married.\n"

    return my_error

####US22##### Unique IDs
def unique_ids (ids_list):
    valid = False
    dict_id_count = {i: ids_list.count(i) for i in ids_list}
    duplicate = [key for key, val in dict_id_count.items() if val > 1]
    if not duplicate:
        valid = True
    return valid

####US30####

def list_of_living_married(individuals):
    lstliving_married = []
    for ind in individuals:
        if ind.spouse_id is not None and ind.death_d is None:
            lstliving_married.append(ind.name)
    return lstliving_married

####US31####

def list_of_living_single(individuals):
    lstliving_single = []
    for ind in individuals:
        if ind.spouse_id is None and ind.death_d is None:
            lstliving_single.append(ind.name)
    return lstliving_single

####US35####

def list_of_recent_births(birth_dates,individuals):
    lstrecent_birth = []
    for (birth,ind) in zip(birth_dates,individuals):
        if birth is not None:
            _date = datetime.strptime(birth, '%d %b %Y')
            birthdt = abs((_date - datetime.today()).days)
            if birthdt < 30:
                lstrecent_birth.append(ind.name)
    return lstrecent_birth

####US36####

def list_of_recent_deaths(death_dates,individuals):
    lstrecent_deaths = []
    for (deaths,ind) in zip(death_dates,individuals):
        if deaths is not None:
            _date = datetime.strptime(deaths, '%d %b %Y')
            death = abs((_date - datetime.today()).days)
            if death < 30:
                lstrecent_deaths.append(ind.name)
    return lstrecent_deaths
