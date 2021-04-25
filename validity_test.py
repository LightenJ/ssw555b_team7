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
from dateutil import relativedelta
from typing import List, Dict
from collections import Counter

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

            # Track siblings
            for other_child in family.children:
                if child != other_child:
                    ancestor_dict[child].siblings.append(other_child)

    # Use the dictionary to find all grandparents, aunts, and uncles of each individual in a family
    for person in ancestor_dict:
        for parent in ancestor_dict[person].parents:
            if parent in ancestor_dict:
                for grandparent in ancestor_dict[parent].parents:
                    ancestor_dict[person].grandparents.append(grandparent)
                for sibling in ancestor_dict[parent].siblings:
                    ancestor_dict[person].aunts_and_uncles.append(sibling)

    # Check for married first cousins
    for family in families:
        temp_error_status = married_first_cousins(family, ancestor_dict)
        # Append any errors we found to the top level error_statuses
        if len(temp_error_status) > 0:
            error_statuses.append(temp_error_status)

    # Check for married nieces/nephews married to aunts/uncles
    for family in families:
        temp_error_status = married_to_aunt_or_uncle(family, ancestor_dict)
        # Append any errors we found to the top level error_statuses
        if len(temp_error_status) > 0:
            error_statuses.append(temp_error_status)

    # check for married siblings
    for family in families:
        temp_error_status = us18_siblings_shud_not_marry(family, ancestor_dict)
        if len(temp_error_status) > 0:
            error_statuses.append(temp_error_status)

    for family in families:
        temp_error_status = us15_fewer_than_15_siblings(family)
        if len(temp_error_status) > 0:
            error_statuses.append(temp_error_status)

    # check for children born after the death of parents
    for family in families:
        father_death = get_death(family.hus_id, individuals)
        mother_death = get_death(family.wife_id, individuals)
        for child in family.children:
            child_birth = get_birth(child, individuals)
            temp_error_status = birth_should_be_before_death_of_parents(child, child_birth, mother_death, father_death)
            if len(temp_error_status) > 0:
                error_statuses.append(temp_error_status)

    # check for children too closely together
    for family in families:
        child_births: Dict[str, datetime] = {}
        for child in family.children:
            child_births[child] = get_birth(child, individuals)
        temp_error_status = births_should_be_spaced_appropriately(family.fam_id, child_births)
        if len(temp_error_status) > 0:
            error_statuses.append(temp_error_status)

    return error_statuses


def convert_date(input_date: str):
    try:
        converted_date = datetime.strptime(input_date, '%d %b %Y')
    except ValueError:
        converted_date = None
    except TypeError:
        converted_date = None

    return converted_date


# Get the death date of an individual
def get_death(ind_id: str, individuals: List[Individual]):
    return_value = None
    for ind in individuals:
        if ind.ind_id == ind_id:
            return_value = convert_date(ind.death_d)
    return return_value


# Get the birth date of an individual
def get_birth(ind_id: str, individuals: List[Individual]):
    return_value = None
    for ind in individuals:
        if ind.ind_id == ind_id:
            return_value = convert_date(ind.birth_d)
    return return_value


def get_age(ind : Individual):
    return_value = "Unknown"
    birth_date = convert_date(ind.birth_d)
    end_date = convert_date(ind.death_d)
    if end_date is None:
        end_date = date.today()
    if birth_date is not None:
        return_value = year_difference(end_date, birth_date)
    return return_value


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
    years_diff = 0
    if date1 is not None and date2 is not None:
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
            if not date_is_invalid(date):
                f_date = convert_date(date)
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


# User story 9, check for a child born after his or her parents died.
def birth_should_be_before_death_of_parents(child_id: str, birth_date: date, mother_death: date, father_death: date):
    my_error = ""
    mother_error = False
    father_error = False

    # Days are more accurate than months in this case
    gestation_period_days = 280

    if birth_date:
        if mother_death:
            if mother_death < birth_date:
                mother_error = True
        if father_death:
            if day_difference(father_death, birth_date) < -gestation_period_days:
                father_error = True

        if mother_error or father_error:
            my_error = "Error: US#09: " + child_id + " was born after "
            if mother_error and father_error:
                my_error += "both his/her parents had died."
            elif mother_error:
                my_error += "his/her mother died."
            else:
                my_error += "his/her father died."

    return my_error



#US11

def US11_NoBigamy(family1, family2):
    if (family1 is None or family2 is None):
        return True
    if (family1.marriage_d > family2.marriage_d):
        if (family1.divorce_d is None):
            return False
        elif (family1.divorce_d < family2.marriage_d):
            return True
        else:
            print("ERROR: FAMILY: US11: Marriage should not occur during marriage to another spouse " + family1.fam_id +" and " + family2.fam_id)
            return False


# User story 13, check for births (that aren't multiple births) too close together.
def births_should_be_spaced_appropriately(family_id: str, child_births: Dict[str, datetime]):
    my_error = ""

    days_in_eight_months = 240
    found_invalid_birth_spacing = False

    for bdate in child_births:
        for bdate2 in child_births:
            if child_births[bdate] and child_births[bdate2]:
                abs_date_difference = abs(day_difference(child_births[bdate], child_births[bdate2]))
                if 1 < abs_date_difference < days_in_eight_months:
                    found_invalid_birth_spacing = True
    if found_invalid_birth_spacing:
        my_error = "Error: US#13: " + family_id + " has children that were born too close to each other.\n"

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

def get_child_name_and_birth_d(f, individuals):
    child_name_birth_d = []
    for child in f.children:
        for i in individuals:
            if child == i.ind_id:
                child_name = i.name
                child_birth_d = i.birth_d
                child_name_birth_d.append((child_birth_d, child_name))

    return child_name_birth_d

####US25##### Unique first names in families
#No more than one child with the same name and birth date should appear in a family
def unique_families_by_child(individuals, families):
    duplicate = []
    for f in families:
        f_duplicate = get_duplicate(get_child_name_and_birth_d (f, individuals))
        if f_duplicate:
            f_duplicate.append(f.fam_id)
            duplicate.append(f_duplicate)
    return duplicate

####US28##### Order siblings by age
#List siblings in families by decreasing age, i.e. oldest siblings first
def order_siblings_by_age(individuals, families):
    child_order_for_family = []
    for f in families:
        f_sorted = sorted(get_child_name_and_birth_d (f, individuals), key=lambda x: convert_date(x[0]))
        if f_sorted:
            f_sorted.append(f.fam_id)
            child_order_for_family.append(f_sorted)
    return child_order_for_family

####US29####

def list_of_deceased_individuals(individuals):
    lstdeceased_indi = []
    for ind in individuals:
        if ind.death_d is not None:
            lstdeceased_indi.append(ind.name)
    return lstdeceased_indi

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

####US33#### List orphans
def list_orphans(individuals, families):
    lst_orphans = []
    wife_death_d = None
    hus_death_d = None
    for f in families:
        for ind in individuals:
            if ind.ind_id == f.wife_id:
                wife_death_d = ind.death_d
            if ind.ind_id == f.hus_id:
                hus_death_d = ind.death_d
        if wife_death_d != None and hus_death_d != None:
            if f.children:
                for child in f.children:
                    for ind in individuals:
                        if ind.ind_id == child:
                            if ind.spouse_id is None and ind.death_d is None:
                                age = get_age(ind)
                                if age < 18:
                                    lst_orphans.append(ind.name)
    return lst_orphans



def get_age_based_on_date(mar_d, birth_d):
    return_value = "Unknown"
    birth_date = convert_date(birth_d)
    mar_date = convert_date(mar_d)
    if birth_date is not None and mar_date is not None:
        return_value = year_difference(mar_date, birth_date)
    return return_value


####US34#### List large age differences
def List_large_age_differences(individuals, families):
    List_large_age_diff =[]
    for f in families:
        marriage_date = f.marriage_d
        for ind in individuals:
            if ind.ind_id == f.wife_id:
                wife_age_at_mar = get_age_based_on_date(marriage_date, ind.birth_d)
                wife_n = ind.name
            if ind.ind_id == f.hus_id:
                hus_age_at_mar = get_age_based_on_date(marriage_date, ind.birth_d)
                hus_n = ind.name
        if wife_age_at_mar > 2*hus_age_at_mar:
            details = ["wife older", marriage_date,  wife_n, wife_age_at_mar, hus_n, hus_age_at_mar]
            List_large_age_diff.append(details)
        if hus_age_at_mar > 2*wife_age_at_mar:
            details = ["Husband older", marriage_date, hus_n, hus_age_at_mar, wife_n,wife_age_at_mar]
            List_large_age_diff.append(details)
    return List_large_age_diff

####US36####
def list_of_recent_births(birth_dates,individuals):
    lstrecent_birth = []
    for (birth,ind) in zip(birth_dates,individuals):
        if birth is not None:
            _date = convert_date(birth)
            birthdt = abs((_date - datetime.today()).days)
            if birthdt < 30:
                lstrecent_birth.append(ind.name)
    return lstrecent_birth

####US36 List all people in a GEDCOM file who died in the last 30 days####

def list_of_recent_deaths(death_dates,individuals):
    lstrecent_deaths = []
    for (deaths,ind) in zip(death_dates,individuals):
        if not date_is_invalid(deaths):
            _date = convert_date(deaths)
            death = abs((_date - datetime.today()).days)
            if death < 30:
                lstrecent_deaths.append(ind.name)
    return lstrecent_deaths

####US37 List recent survivors

def list_of_survivors(individuals, families):
    individualsId = [individual.ind_id for individual in individuals]
    individualsDeathday = [individual.death_d for individual in individuals]
    recentDeathId = []
    recentsurvivors = []
    x = 0
    while (x < len(individualsId)):
        if not date_is_invalid(individualsDeathday[x]):
            _date = convert_date(individualsDeathday[x])
            death = abs((_date - datetime.today()).days)
            if death < 30:
                recentDeathId.append(individualsId[x])
        x += 1
    for death in recentDeathId:
        if death != None:
            for fam in families:
                if fam.hus_id == death:
                    for i in individuals:
                        if fam.wife_id == i.ind_id:
                            wife_name = i.name
                            recentsurvivors.append(wife_name)
                elif fam.wife_id == death:
                    for fam in families:
                        for i in individuals:
                            if fam.hus_id == i.ind_id:
                                husband_name = i.name
                                recentsurvivors.append(husband_name)
            for fam in families:
                    for c in fam.children:
                        if c and (fam.wife_id == death or fam.hus_id == death):
                            for i in individuals:
                                if c == i.ind_id:
                                    children = i.name
                                    recentsurvivors.append(children)
    return recentsurvivors


####US38 List all living people in a GEDCOM file whose birthdays occur in the next 30 days####

def list_of_upcoming_birthdays(birth_dates,individuals):
    lstupcoming_birthdays = []
    thirtyDays = datetime.today() + relativedelta.relativedelta(days=30)
    today = datetime.today()
    for (births, ind) in zip(birth_dates, individuals):
        if births is not None:
            _date = convert_date(births)
            if (thirtyDays.month == today.month):
                if (thirtyDays.month == _date.month):
                    if (today.day <= _date.day and thirtyDays.day >= _date.day):
                        lstupcoming_birthdays.append(ind.name)
            else:
                if (today.month == _date.month):
                    if (_date.day >= today.month):
                        lstupcoming_birthdays.append(ind.name)
                elif thirtyDays.month == _date.month:
                    if (_date.day <= thirtyDays.day):
                        lstupcoming_birthdays.append(ind.name)
    return lstupcoming_birthdays

####US39 List upcoming anniversaries####

def list_of_anniversaries(marriage_dates,individuals):
    lstrecent_marriage = []
    for (marr,ind) in zip(marriage_dates,individuals):
        if marr is not None:
            _date = convert_date(marr)
            marriage = abs((_date - datetime.today()).days)
            if marriage < 30:
                lstrecent_marriage.append(ind.name)
    return lstrecent_marriage

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


# User story 20, aunts and uncles should not marry nieces and nephews
def married_to_aunt_or_uncle(family: Family, ancestors: Ancestors):
    my_error = ""

    if family.wife_id in ancestors:
        for aunt_or_uncle in ancestors[family.wife_id].aunts_and_uncles:
            if aunt_or_uncle == family.hus_id:
                my_error = "Error: US#20: family " + family.fam_id + "'s wife, " + family.wife_id + \
                           ", is married to her uncle, " + aunt_or_uncle + ".\n"

    if family.hus_id in ancestors:
        for aunt_or_uncle in ancestors[family.hus_id].aunts_and_uncles:
            if aunt_or_uncle == family.wife_id:
                my_error = "Error: US#20: family " + family.fam_id + "'s husband, " + family.hus_id + \
                           ", is married to his aunt, " + aunt_or_uncle + ".\n"

    return my_error


# User story 18, siblings should not marry
def us18_siblings_shud_not_marry(family : Family, ancestors : Ancestors):
    my_error = ""
    husband_parents = []
    wife_parents = []
    shared_parents_list = []
    if family.wife_id in ancestors:
        for w_parent in ancestors[family.wife_id].parents:
            wife_parents.append(w_parent)

    if family.hus_id in ancestors:
        for h_parent in ancestors[family.hus_id].parents:
            husband_parents.append(h_parent)

    shared_parents = False
    for h_parent in husband_parents:
        for w_parent in wife_parents:
            if h_parent == w_parent:
                shared_parents = True
                shared_parents_list.append(h_parent)

    if shared_parents:
        my_error = "Error: US#18: Husband " + family.hus_id + " and wife " + family.wife_id + " in family "
        my_error = my_error + family.fam_id + " are married siblings who share the same parent(s):"
        for parent_id in shared_parents_list:
            my_error = my_error + " " + parent_id
        my_error = my_error + ".\n"

    return my_error

# User story 15, fewer than 15 siblings
def us15_fewer_than_15_siblings(family):
    my_error = ""
    if len(family.children) >= 15:
        my_error = "Error: US15: Family: " + family.fam_id + " has 15 or more siblings"

    return my_error

# User story 16, Male last names
def us16_male_last_names(individuals, families):
    my_error = ""
    for family in families:
        if family.marriage_d:
            lastname = family.hus_id

            for ind in individuals:
                if lastname == ind.ind_id:
                    l_name = ind.name.split('/')[-2].lower()

                for ind in individuals:
                    id = ind.ind_id
                    name = ind.name
                    gender = ind.sex

                    if id in family.children:
                        if gender == "M":
                            if l_name not in name:
                                my_error = "Error: US16: " + name + "'s lastname is not same as his/her/their father's."

    return my_error


# User story 14, Multiple births <= 5
def us14_multiple_births_less_than_5(individuals, families):
    my_error = ""

    for family in families:
        sibling_uids = family.children
        siblings = list(x for x in individuals if x.ind_id in sibling_uids)
        sib_birthdays = []
        for sibling in siblings:
            sib_birthdays.append(sibling.birth_d)
        result = Counter(sib_birthdays).most_common(1)
        for (a, b) in result:
            if b > 5:
                family.fam_id
                my_error = "Error: US14: Family " + family.fam_id + " has more than 5 siblings born at once."

    return my_error


# User story 32, List multiple births
def List_multiple_births(individuals, families):
    my_error = ""
    for family in families:
        sibling_ids = family.children
        siblings = list(x for x in individuals if x.ind_id in sibling_ids)
        sib_birthdays = []
        for sibling in siblings:
            name_birth_d = [sibling.birth_d,sibling.name]
            sib_birthdays.append(name_birth_d)
            unique =[]
            duplicate =[]
            duplicate1 =[]
            for element in sib_birthdays:
                if element[0] not in unique:
                    unique.append(element[0])
                else:
                    duplicate.append(element[0])

            for element in sib_birthdays:
                if element[0] in duplicate:
                    duplicate1.append(element)

            if duplicate:
                my_error = duplicate1

    return my_error

