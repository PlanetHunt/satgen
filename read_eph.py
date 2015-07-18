#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Reads the ephemerdian files and create points to it so
master can do the simulations. With this method the accuracy will be higher.
"""

from jd_utils import JD
from database import DB
from datetime import datetime


class Eph:

    def __init__(self, name, prefix):
        self.name = name
        self.prefix = prefix
        self.name_suffix = "_a_sim.xml_out_eph_eph.txt"
        self.sum_of = 0
        self.counter = 0
        self.jd = JD()
        self.file_name = self.prefix + self.name + self.name_suffix

    def calulate_mean(self):
        """
        calculates the mean value (middle of the
        simulation to get an extra point)
        """
        for line in open(self.file_name):
            li = line.strip()
            if not li.startswith("#") and li.rstrip():
                self.counter = self.counter + 1
        return int(self.counter / 2)

    def format_to_date(self, mjd):
        """
        gets the modified julian date and convert
        it to suitable date for MASTER
        """
        jud = self.jd.mjd_to_jd(float(mjd))
        cal_date = self.jd.jd_to_date(jud)
        (2014, 8, 21.0)
        date = str(cal_date[0]) + " " + str(cal_date[1]) + \
            " " + str(int(cal_date[2])) + " " + "00"
        return date

    def get_sim_eph(self):
        """
        give back the formated start, middle eph for the MASTER simulation.
        Better than just one point.
        """
        result = {"name": self.name}
        mean = self.calulate_mean()
        counter = 0
        for line in open(self.file_name):
            li = line.strip()
            if not li.startswith("#") and li.rstrip():
                if (counter == 0):
                    res = line.rstrip().split(" ")
                    result.update({"init_date_1": self.format_to_date(res[0]),
                                   "final_date_1": "",
                                   "init_semiMajorAxis_1": res[2],
                                   "init_eccentricity_1": res[3],
                                   "init_inclination_1": res[4],
                                   "init_rAAN_1": res[5],
                                   "init_argOfPerigee_1": res[6]})
                if (counter == mean):
                    res = line.rstrip().split(" ")
                    result.update({"init_date_2": self.format_to_date(res[0]),
                                   "final_date_2": "",
                                   "init_semiMajorAxis_2": res[2],
                                   "init_eccentricity_2": res[3],
                                   "init_inclination_2": res[4],
                                   "init_rAAN_2": res[5],
                                   "init_argOfPerigee_2": res[6]})
                    result["final_date_1"] = self.format_to_date(res[0])
                if(counter == (mean * 2) - 1):
                    res = line.rstrip().split(" ")
                    result["final_date_2"] = self.format_to_date(res[0])
                counter = counter + 1
        return result
# eph = Eph("sim/GTVITX7Q")
# print eph.get_sim_eph()
