"""
#===========================================================================================#
Subject         : SSW -555(Agile Methods for Software Development)
Script Author   : Team#7
Date            : 03/04/2021
Script Name     : data_classes.py
#===========================================================================================#

Purpose:
--------
Contains data classes shared among multiple Python scripts
---------------------------------------------------------------------------------------------
"""


class Individual:
    def __init__(self, ind_id):
        self.ind_id = ind_id
        self.name = None
        self.sex = None
        self.birth_d = None
        self.death_d = None
        self.spouse_id = None
        self.child_id = None


class Family:
    def __init__(self, fam_id):
        self.fam_id = fam_id
        self.marriage_d = None
        self.hus_id = None
        self.wife_id = None
        self.children = []
        self.divorce_d = None

