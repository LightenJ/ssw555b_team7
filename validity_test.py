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
    individual: Individual
    for individual in individuals:
        error_statuses = check_valid_individual(individual)

    return error_statuses


def check_valid_individual(individual: Individual):
    error_statuses = []
    birth_date = individual.birth_d
    death_date = individual.death_d
    my_full_name = individual.name

    error_text = younger_than_150(birth_date, death_date, my_full_name)
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
        my_error = "Error: " + name + " is more than 150 years old.\n"

    return my_error


def year_difference(date1: datetime.date, date2: datetime.date):
    years_diff = date1.year - date2.year
    if date2.month > date1.month or (date1.month == date2.month and date2.day > date1.day):
        years_diff = years_diff - 1
    return years_diff
