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

# welcome Message
print('welcome to P03 Python Assignment\n')

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

ID = []
Name = []
Fam = []
Hus = []
Wif = []
Ind = PrettyTable(["ID", "NAME"])
Family = PrettyTable(["ID", "Husband Name", "Wife Name"])

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


def find_str(fhand):
    """
    To extract the valve and update the variable value only if more than 2 parameters are there to check with the provided dict
    """
    global ID, Name, Ind, Fam, Hus, Wif
    ind_list = []
    for line in fhand:
        line = line.strip()  # Return a copy of the sequence with specified leading and trailing bytes removed (spaces)
        if len(line) > 1:  # ignored any data without 2 parameters.
            splitline = line.split(' ', 2)
            found, index = data_match(splitline)
            if index != 1:  # swapping 2 and 3 index if the tag is present in 3 element
                splitline[1], splitline[2] = splitline[2], splitline[1]
            if len(splitline) > 2:
                if '@' in splitline[2]:
                    splitline[2] = splitline[2].replace("@", "")

            if splitline[0] == '0' and splitline[1] == 'INDI':
                if splitline[2] not in ID:
                    ID.append(splitline[2])

            if splitline[0] == '1' and splitline[1] == 'NAME':
                if splitline[2] not in Name:
                    Name.append(splitline[2])

            if splitline[0] == '0' and splitline[1] == 'FAM':
                if splitline[2] not in Fam:
                    Fam.append(splitline[2])

            if splitline[0] == '1' and splitline[1] == 'HUSB':
                if splitline[2] not in Hus:
                    Hus.append(splitline[2])

            if splitline[0] == '1' and splitline[1] == 'WIFE':
                if splitline[2] not in Wif:
                    Wif.append(splitline[2])

    for i, n in zip(ID, Name):
        Ind.add_row([i, n])
        ind_list.append((i, n))
    Ind.sortby = 'ID'
    print("Individual ID and Name \n", Ind)

    for f, h, w in zip(Fam, Hus, Wif):
        hus_name = ''#default
        wif_name = ''#default
        for i in range(len(ind_list)):
            if ind_list[i][0] == h:
                hus_name = ind_list[i][1]
            if ind_list[i][0] == w:
                wif_name = ind_list[i][1]

        Family.add_row([f, hus_name, wif_name])

    Family.sortby = 'ID'

    print(" Family info \n", Family)

fname = input("Enter the file name: ")
try:
    fhand = open(fname)  # open File
    sys.stdout = open('OutputFile.txt', 'w')
    find_str(fhand)
    fhand.close()  # Close the file
except:
    print('File cannot be opened:', fname)
    sys.exit()

