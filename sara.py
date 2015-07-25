#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Manages SARA Program, a tool from MASTER-2009
To use the code you need MASTER-2009 installed, please Download it
from: https://sdup.esoc.esa.int
"""

import subprocess
import threading
from datetime import datetime, date, time
import os
import re
import sys
import shutil
from unit_converter import UnitConverter
from database import DB

class Sara:

    def __init__(self, sara_path, db, default_dir_path):
        self.set_sara_path(sara_path)
        self.set_default_dir(default_dir_path)
        self.set_db(db)
        self.uc = UnitConverter()

    def set_sara_path(self, sara_path):
        """
        Sets the Master Absolute Path
        """
        self.sara_path = sara_path

    def get_db(self):
        """
        Return database instance
        """
        return self.db

    def set_db(self, db):
        """
        Sets the database instance
        """
        self.db = db

    def get_default_dir(self):
        """
        returns the absolute path to the default directory
        """
        return self.default_dir

    def set_default_dir(self, default_path):
        """
        set the defualt abs path
        """
        self.default_dir = default_path

    def get_sara_path(self):
        """
        returns the absolute path to SARA
        """
        return self.sara_path

    def get_space_objects(self):
        """
        creates the folders and set the env
        variable so the master simulation
        can be run
        """
        return self.db.get_space_objects_data()

    def format_date_to_ymd(self, date):
        """
        formats date object to YYYY/MM/DD
        """
        return datetime.strptime(date, "%Y-%m-%dT%H:%M:%S.%f").strftime("%Y/%m/%d")

    def format_date_to_hms(self, date):
        """
        formats date object to HH:MM:SS.SSS
        """
        return datetime.strptime(date, "%Y-%m-%dT%H:%M:%S.%f").strftime("%H:%M:%S.%f")

    def create_files(self, db_tuple):
        """
        creates and copies files to run SARA
        """

        self.path = self.get_default_dir() + "/sara_sim/" + db_tuple[1]
        os.mkdir(self.path)
        os.chdir(self.path)
        os.mkdir("input")
        os.mkdir("output")

        cfg_content = {"name": db_tuple[1], 
                        "kep_e": db_tuple[4], 
                        "kep_i": self.uc.rad_to_deg(db_tuple[5]),
                        "kep_ran": self.uc.rad_to_deg(db_tuple[6]), 
                        "kep_aop": self.uc.rad_to_deg(db_tuple[7]),
                        "kep_tan": self.uc.rad_to_deg(db_tuple[8]), 
                        "kep_a": self.uc.m_to_km(db_tuple[3]),
                        "init_date_ymd": self.format_date_to_ymd(db_tuple[2]),
                        "init_time_hms": self.format_date_to_hms(db_tuple[2]),
                        }

        cfg_template = open(self.get_default_dir() + "/sample_files/sara.inp", "r")
        data = cfg_template.read()

        data = data.format(**cfg_content)

        cfg_file = open(os.getcwd() + "/input/reentry.inp", "w")
        cfg_file.write(data)

        cfg_template.close()
        cfg_file.close()

        shutil.copyfile(self.get_default_dir(
        ) + "/sample_files/usermat.db", os.getcwd() + "/input/usermat.db")

    def run_sara(self):
        """
        runs SARA
        """
        subprocess.call(self.get_sara_path() + "/REENTRY/reentry_linux")

class SaraThread(threading.Thread):
    """
    Sara threads
    """
    def __init__(self, divider, db_tuple, sara):
        threading.Thread.__init__(self)
        self.divider = divider
        self.db_tuple = db_tuple
        self.sara = sara
        self.handled = False
        
        sara.create_files(db_tuple)

    def run(self):
        self.sara.run_sara()

db = DB("satgen.db")
s = Sara("/opt/DRAMA-2.0/TOOLS/SARA", db, "/home/pouyan/Projects/Python/Satgen")

space_objects = db.get_final_state_data()

thread_list = []
for u in space_objects["data"]:
    while(len(thread_list) > 4):
        for t in thread_list:
            if not t.isAlive():
                t.handled = True
        thread_list = [t for t in thread_list if not t.handled]
    thread0 = SaraThread(1, u, s)
    thread0.start()
    thread_list.append(thread0)
