"""
#===========================================================================================#
Subject         : SSW -555(Agile Methods for Software Development) 
Assignment      : P03: Continue programming, create version control repository
Script Author   : Team#7
Date            : 02/20/2021
Script Name     : SSW555-Porject.py
#===========================================================================================#

Purpose:
--------
After reading all of the data, print the unique identifiers and names of each of
 the individuals in order by their unique identifiers. Then, for each family,
 print the unique identifiers and names of the husbands and wives, in order
 by unique family identifiers.
---------------------------------------------------------------------------------------------

"""

import sys
from prettytable import PrettyTable
import validity_test
from data_classes import Individual
from data_classes import Family
from validity_test import get_age

print('Enter file name with extension when prompted  e.g : test.ged \n')

# Dictionary  from Project file
Tag_Level = {
    'INDI': 0,
    'NAME': 1,
    'SEX': 1,
    'BIRT': 1,
    'DEAT': 1,
    'FAMC': 1,
    'FAMS': 1,
    'FAM': 0,
    'MARR': 1,
    'HUSB': 1,
    'WIFE': 1,
    'CHIL': 1,
    'DIV': 1,
    'DATE': 2,
    'HEAD': 0,
    'TRLR': 0,
    'NOTE': 0}


Ind = PrettyTable(["ID", "NAME","BIRTH DATE","DEATH DATE","SPOUSE ID","CHILD ID","AGE"])
Fam = PrettyTable(["ID", "Husband Name", "Wife Name", "CHILD ID"])
ind = []
fam = []
ind_list = []
individuals = []
families = []
read_dates = []
ids_list =[]
read_birth_dates = []
read_death_dates = []
read_marriage_dates = []

def data_match(splitline):
    data_found = False
    index = 1  # default value
    for key, val in Tag_Level.items():
        if key in splitline:
            index = splitline.index(key)
        if key == splitline[index] and val == int(splitline[0]):
            data_found = True
            break
    return data_found, index

def strip_valid_line(line):
    splitline = []
    line = line.strip()  # Return a copy of the sequence with specified leading and trailing bytes removed (spaces)
    if len(line) > 1:  # ignored any data without 2 parameters.
        splitline = line.split(' ', 2)
        found, index = data_match(splitline)
        if index != 1:  # swapping 2 and 3 index if the tag is present in 3 element
            splitline[1], splitline[2] = splitline[2], splitline[1]
        if len(splitline) > 2:
            if '@' in splitline[2]:
                splitline[2] = splitline[2].replace("@", "")
    return splitline

def extract_ind_date (instance, day, splitline):
    if day == 'BIRT':
        instance.birth_d = splitline[2]
    if day == 'DEAT':
        instance.death_d = splitline[2]

def extract_mar_date(instance, day, splitline):
    if day == 'MARR':
        instance.marriage_d = splitline[2]
    if day == 'DIV':
        instance.divorce_d = splitline[2]

def extract_individual_info(read_lines, line_no, individual):
    line_no +=1
    splitline = strip_valid_line(read_lines[line_no])
    while splitline[0] != "0" and line_no < len(read_lines):
        if splitline[1] == 'NAME':
            individual.name = splitline[2]

        if splitline[1] == 'SEX':
            individual.sex = splitline[2]

        if splitline[1] == 'BIRT' or splitline[1] == 'DEAT':
            extract_ind_date(individual, splitline[1], strip_valid_line(read_lines[line_no+1]))

        if splitline[1] == 'FAMC':
            individual.child_id = splitline[2]

        if splitline[1] == 'FAMS':
            individual.spouse_id = splitline[2]

        line_no +=1
        splitline = strip_valid_line(read_lines[line_no])
    individuals.append(individual)

def extract_family_info(read_lines, line_no, family):
    line_no +=1
    splitline = strip_valid_line(read_lines[line_no])
    while splitline[0] != "0" and line_no < len(read_lines):

        if splitline[1] == 'MARR' or splitline[1] == 'DIV':
            extract_mar_date(family, splitline[1], strip_valid_line(read_lines[line_no+1]))

        if splitline[1] == 'HUSB':
            family.hus_id = splitline[2]

        if splitline[1] == 'WIFE':
            family.wife_id = splitline[2]

        if splitline[1] == 'CHIL':
            family.children.append(splitline[2])

        line_no +=1
        splitline = strip_valid_line(read_lines[line_no])

    families.append(family)

def find_str(read_lines):
    """
    To extract the valve and update the variable value only if more than 2 parameters are there to check with the provided dict
    """
    line_no = 0
    while line_no < len(read_lines):
        splitline = strip_valid_line(read_lines[line_no])

        if splitline[0] == '0' and splitline[1] == 'INDI':
            extract_individual_info(read_lines, line_no, Individual(splitline[2]))

        if splitline[0] == '0' and splitline[1] == 'FAM':
            extract_family_info(read_lines, line_no, Family(splitline[2]))
        line_no += 1

    for ind in individuals:
        Ind.add_row([ind.ind_id, ind.name,ind.birth_d,ind.death_d,ind.spouse_id,ind.child_id,get_age(ind)])
        ind_list.append((ind.ind_id, ind.name))
        read_dates.append(ind.birth_d)
        read_dates.append(ind.death_d)
        ids_list.append(ind.ind_id)
        read_death_dates.append(ind.death_d)
        read_birth_dates.append(ind.birth_d)
    Ind.sortby = 'ID'

    print("Individual ID and Name \n", Ind)

    for f in families:
        ids_list.append(f.fam_id)
        read_dates.append(f.marriage_d)
        read_dates.append(f.divorce_d)
        read_marriage_dates.append(f.marriage_d)
        lstchildren = []
        hus_name = '' #default
        wif_name = '' #default
        for i in range(len(ind_list)):
            if ind_list[i][0] == f.hus_id:
                hus_name = ind_list[i][1]
            if ind_list[i][0] == f.wife_id:
                wif_name = ind_list[i][1]
        for child_id in f.children:
            lstchildren.append(child_id)

        Fam.add_row([f.fam_id, hus_name, wif_name, ",".join(f.children)])

    Fam.sortby = 'ID'

    print(" Family info \n", Fam)



fname = input('Enter the file name: ')
sys.stdout = open('OutputFile.txt', 'w')
try:
    fhand = open(fname)  # open File
    read_lines = fhand.readlines()
except:
    print('File cannot be opened:', fname)
    sys.exit()

try:
    find_str(read_lines)
    fhand.close()  # Close the file
except Exception as e: print(e)

try:
    print("\nUS01 ==> Dates (Birth, Death, Marriage, Divorce) Before Today is :", validity_test.date_before(read_dates))
    error_text = validity_test.check_valid(individuals, families)
    for error in error_text:
        print(error)
    print("\nUS22 ==> ALL IDs Unique ?:", validity_test.unique_ids(ids_list))
    print("\nUS23 ==> Duplicate name and birth date:", validity_test.unique_name_and_birth_date(individuals))
    print("\nUS24 ==> Duplicate families by spouses:", validity_test.unique_families_by_spouses(individuals,families))
    print("\nUS25 ==> Duplicate Child by family :", validity_test.unique_families_by_child(individuals,families))
    print("\nUS28 ==> Order siblings by age :", validity_test.order_siblings_by_age(individuals,families))
    print("\nUS30 ==> List of living married is : \n", validity_test.list_of_living_married(individuals))
    print("\nUS31 ==> List of living single is : \n", validity_test.list_of_living_single(individuals))
    # print("\nUS33 ==>List of Orphans : \n", validity_test.list_orphans(individuals, families))
    print("\nUS35 ==>List of recent births : \n", validity_test.list_of_recent_births(read_birth_dates,individuals))
    print("\nUS36 ==>List of recent deaths : \n", validity_test.list_of_recent_deaths(read_death_dates,individuals))
    print("\nUS37 ==>List of recent survivors : \n", validity_test.list_of_survivors(individuals, families))
    print("\nUS38 ==>List of upcoming Birthdays : \n", validity_test.list_of_upcoming_birthdays(read_birth_dates,individuals))
    print("\nUS39 ==>List of upcoming anniversaries : \n",validity_test.list_of_anniversaries(read_marriage_dates, individuals))
    print("\nUS14 ==> Multiple births less than or equal to 5 : \n",validity_test.us14_multiple_births_less_than_5(individuals, families))
    print("\nUS16 ==> Male last names : \n", validity_test.us16_male_last_names(individuals, families))
except Exception as exception:
    print(exception)




