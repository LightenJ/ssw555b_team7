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
from data_classes import Individual, Ancestors
from data_classes import Family
from data_classes import Ancestors
from typing import List, Dict, Any


def check_valid(individuals: List[Individual], families: List[Family]):
    error_statuses = []
    temp_error_statuses = []
    individual: Individual
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

    # Restarting through families to process all children
    for family in families:
        # Find all the children in a family
        for child in family.children:
            for temp_ind in individuals:
                if child == temp_ind.ind_id:
                    temp_error_statuses = check_valid_individual_child(temp_ind, family)

                    # Append any errors we found to the top level error_statuses
                    for error_msg in temp_error_statuses:
                        error_statuses.append(error_msg)

    # Building parent and grandparent lists.  Using families only, since any
    #   individuals not in families don't have enough data to create the list.
    #   Note that an individual must be a child, as well as a spouse, in a
    #   family to find first cousins.
    ancestor_dict: Dict[str, Ancestors] = {}
    for family in families:
        # Find all the children in a family and record their parents
        for child in family.children:
            if child not in ancestor_dict:
                ancestor_dict[child] = Ancestors()
            ancestor_dict[child].parents.append(family.hus_id)
            ancestor_dict[child].parents.append(family.wife_id)

    # Use the dictionary to find all grandparents of each individual in a family
    for person in ancestor_dict:
        for parent in ancestor_dict[person].parents:
            if parent in ancestor_dict:
                for grandparent in ancestor_dict[parent].parents:
                    ancestor_dict[person].grandparents.append(grandparent)

    # Check for married first cousins
    for family in families:
        temp_error_status = married_first_cousins(family, ancestor_dict)
        # Append any errors we found to the top level error_statuses
        if len(temp_error_status) > 0:
            error_statuses.append(temp_error_status)

    return error_statuses


def convert_date(input_date: str):
    try:
        converted_date = datetime.strptime(input_date, '%d %b %Y')
    except ValueError:
        converted_date = None

    return converted_date


def date_is_invalid(input_date: str):
    date_invalid = (input_date is None or len(input_date) == 0)
    if not date_invalid:
        return_date = convert_date(input_date)
        if return_date is None:
            date_invalid = True

    return date_invalid

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
    error_text = US04_marriage_before_divorce(marriage_date, divorce_date, my_full_name)
    if len(error_text) > 0:
        error_statuses.append(error_text)
    error_text = US05_marriage_before_death(marriage_date, death_date, my_full_name)
    if len(error_text) > 0:
        error_statuses.append(error_text)
    error_text = divorce_before_death(divorce_date, death_date, my_full_name)
    if len(error_text) > 0:
        error_statuses.append(error_text)
    error_text = married_at_14_or_older(birth_date, marriage_date, my_full_name)
    if len(error_text) > 0:
        error_statuses.append(error_text)
    error_text = correct_gender_for_role(individual, family)
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

    if date_is_invalid(death_date):   # Individual has not died, check against current date
        death_date = date.today()
        birth_date = convert_date(birth_date)
    else:                      # Individual has died, check birth against death
        death_date = convert_date(death_date)
        birth_date = convert_date(birth_date)

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

    valid = True
    try:
        for date in dates:
            if date != None:
                f_date = datetime.strptime(date.rstrip(), '%d %b %Y').date()
                c_date = datetime.now().date()
                if f_date > c_date:
                    valid = False
    except: valid = None

    return valid

####US02#####
def birthbeforemarriage(birth_date: str, marriage_date: str, name: str):
    my_error = ""
    if date_is_invalid(marriage_date):   # Individual is not married, check against current date
        marriage_date = date.today()
        birth_date = convert_date(birth_date)
    else:
        marriage_date = convert_date(marriage_date)
        birth_date = convert_date(birth_date)

    if year_difference(marriage_date, birth_date) < 0:
        my_error = "Error: US#02: Individual " + name + " was married before they were born.\n"
    return my_error

####US03#####
def birthbeforedeath(birth_date: str, death_date: str, name: str):
    my_error = ""
    if date_is_invalid(death_date):  # Individual is not dead, check against current date
        death_date = date.today()
        birth_date = convert_date(birth_date)
    else:  # Individual has died, check birth against death
        death_date = convert_date(death_date)
        birth_date = convert_date(birth_date)

    if year_difference(birth_date, death_date) > 0:
        my_error = "Error: US#03: Individual " + name + " died before they were born.\n"
    return my_error


####US04####
def US04_marriage_before_divorce(marriage_date: str, divorce_date: str, name: str):
    my_error = ""
    if date_is_invalid(divorce_date):  # Husband and wife are not divorced, check against current date
        divorce_date = date.today()
        marriage_date = convert_date(marriage_date)
    else:  # Individual has died, check birth against death
        divorce_date = convert_date(divorce_date)
        marriage_date = convert_date(marriage_date)

    if year_difference(marriage_date, divorce_date) > 0:
        my_error = "Error: US#04: Family: Married before divorce date.\n"
    return my_error


####US05####
def US05_marriage_before_death(marriage_date: str, death_date: str, name: str):
    my_error = ""
    if date_is_invalid(death_date):  # Not dead, check against current date
        death_date = date.today()
        marriage_date = convert_date(marriage_date)
    else:  
        death_date = convert_date(death_date)
        marriage_date = convert_date(marriage_date)

    if year_difference(marriage_date, death_date) > 0:
        my_error = "Error: US#05: Family: Married before death.\n"
    return my_error


# User Story 6, divorce must be before (okay, or on the day of) death.
def divorce_before_death(divorce_date: str, death_date: str, name: str):
    my_error = ""
    if date_is_invalid(death_date) or date_is_invalid(divorce_date):
        # Either hasn't died or hasn't divorced, so no way to be invalid
        pass
    else:
        divorce_date = convert_date(divorce_date)
        death_date = convert_date(death_date)
        if day_difference(death_date, divorce_date) < 0:
            my_error = "Error: US#06: Individual " + name + " was divorced after they died.\n"
    return my_error


# User story 10, marriage before 14 - married persons must be at least 14 when married.
def married_at_14_or_older(birth_date: str, marriage_date: str, name: str):
    my_error = ""

    if date_is_invalid(marriage_date) or date_is_invalid(birth_date):
        # Don't check if no marriage date or no birth date is available - though this is for a family, so
        # those shouldn't really be possible.
        pass
    else:                      # Individual has died, check birth against death
        marriage_date = convert_date(marriage_date)
        birth_date = convert_date(birth_date)
        if year_difference(marriage_date, birth_date) < 14:
            my_error = "Error: US#10: " + name + " was married when younger than 14.\n"

    return my_error


# User story 8, check for a child born before his or her parents were married.
def birth_before_marriage_of_parents(birth_date: str, marriage_date: str, name: str):
    my_error = ""

    if date_is_invalid(marriage_date) or date_is_invalid(birth_date):
        # Don't check if no marriage date or no birth date is available - though this is for a family, so
        # those shouldn't really be possible.
        pass
    else:                      # See if the parents were married before the individual was born
        marriage_date = convert_date(marriage_date)
        birth_date = convert_date(birth_date)
        if day_difference(birth_date, marriage_date) < 0:
            my_error = "Error: US#08: " + name + " was born before his/her parents were married.\n"

    return my_error


# User story 21, correct gender for role
def correct_gender_for_role(individual : Individual, family : Family):
    my_error = ""

    # Assumption: this function is called only if the individual is a spouse in the family - so
    # the individual ID is valid, and at least one spouse's ID in the family matches it.
    if individual.sex is None or (individual.sex.upper() != "M" and individual.sex.upper() != "F"):
        my_error = "Warning: US#21: " + individual.name + " is a spouse in family " + family.fam_id + \
                   ", but that person's gender is unknown.\n"
    elif individual.sex.upper() == "M":
        if individual.ind_id == family.wife_id:
            my_error = "Error: US#21: " + individual.name + " is a man listed as a wife in family " \
                       + family.fam_id + ".\n"
    else:  # individual.sex.upper() == "F":
        if individual.ind_id == family.hus_id:
            my_error = "Error: US#21: " + individual.name + " is a woman listed as a husband in family " \
                       + family.fam_id + ".\n"

    return my_error


####US22##### Unique IDs
def unique_ids (ids_list):
    valid = False
    dict_id_count = {i: ids_list.count(i) for i in ids_list}
    duplicate = [key for key, val in dict_id_count.items() if val > 1]
    if not duplicate:
        valid = True
    return valid

def get_duplicate(test_list):
    unique =[]
    duplicate =[]
    for element in test_list:
        if element in unique:
            duplicate.append(element)
        else:
            unique.append(element)
    return duplicate

####US23##### Unique name and birth date
def unique_name_and_birth_date(individuals):
    name_birth_d = []

    for ind in individuals:
        name_birth_d.append((ind.name, ind.birth_d))
    return get_duplicate(name_birth_d)

####US24##### Unique families by spouses
def unique_families_by_spouses(individuals, families):
    spouse_name_marr_d = []
    for f in families:
        if f.marriage_d:
            marriage_d = f.marriage_d
            for i in individuals:
                if f.wife_id == i.ind_id:
                    wife_name = i.name
        spouse_name_marr_d.append((marriage_d, wife_name))

    duplicate= get_duplicate(spouse_name_marr_d)
    return duplicate

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
            _date = convert_date(birth)
            birthdt = abs((_date - datetime.today()).days)
            if birthdt < 30:
                lstrecent_birth.append(ind.name)
    return lstrecent_birth

####US36####

def list_of_recent_deaths(death_dates,individuals):
    lstrecent_deaths = []
    for (deaths,ind) in zip(death_dates,individuals):
        if deaths is not None:
            _date = convert_date(deaths)
            death = abs((_date - datetime.today()).days)
            if death < 30:
                lstrecent_deaths.append(ind.name)
    return lstrecent_deaths


# User story 19, first cousins should not marry
def married_first_cousins(family : Family, ancestors : Ancestors):
    my_error = ""
    husband_grandparents = []
    wife_grandparents = []
    husband_parents = []
    wife_parents = []
    shared_grandparent_list = []
    if family.wife_id in ancestors:
        for w_parent in ancestors[family.wife_id].parents:
            wife_parents.append(w_parent)
        for w_grandparent in ancestors[family.wife_id].grandparents:
            wife_grandparents.append(w_grandparent)
    if family.hus_id in ancestors:
        for h_parent in ancestors[family.hus_id].parents:
            husband_parents.append(h_parent)
        for h_grandparent in ancestors[family.hus_id].grandparents:
            husband_grandparents.append(h_grandparent)

    shared_grandparents = False
    for h_grandparent in husband_grandparents:
        for w_grandparent in wife_grandparents:
            if h_grandparent == w_grandparent:
                shared_grandparents = True
                shared_grandparent_list.append(h_grandparent)

    # Still need to make sure they're not actually siblings rather than cousins.
    shared_parents = False
    if shared_grandparents:
        for h_parent in husband_parents:
            for w_parent in wife_parents:
                if h_parent == w_parent:
                    shared_parents = True

    if shared_grandparents and not shared_parents:
        my_error = "Error: US#19: Husband " + family.hus_id + " and wife " + family.wife_id + " in family "
        my_error = my_error + family.fam_id + " are first cousins who share the following grandparent(s):"
        for grandparent_id in shared_grandparent_list:
            my_error = my_error + " " + grandparent_id
        my_error = my_error + ".\n"

    return my_error
