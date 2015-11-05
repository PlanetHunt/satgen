#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import json
import subprocess
import xml.etree.ElementTree as ET
from datetime import datetime
from operator import itemgetter
from config_new import Config
from database import DB
from xml.dom.minidom import parse
import time


class Extrapolate:

    def __init__(self,
                 db,
                 deap_params="stela_deap.json"):
        self.stela_config = Config(db)
        self.stela_config.db.create_all_tables()
        self.stela_config.generate_xml()
        try:
            stdp = open(deap_params)
        except IOError as e:
            print "One (more) of the config files is not avaialbe."
            print e
            raise
        try:
            self.stdp_sections = json.load(stdp)["sections"]
        except ValueError as e:
            print "One (more) of the config files is not valid json."
            print e
            raise
        stdp.close()
        self.path = self.stela_config.config["project"][
            "base"] + self.stela_config.config["stela"]["sim_path"]

    def extrapolate(self, name):
        """
        Run the Extrapolation.

        Args:
                name (str) the name of the sattelite random gen.

        Kwargs:
                None

        Returns:
                Boolean
        """
        stela_path = self.stela_config.config["stela"]["path"]
        os.chdir(stela_path)
        input_file = str(self.path + "/" + name + "_a_sim.xml")
        output_file = str(self.path + "/" + name + "_out_sim.xml")
        output_eph_file = str(self.path + "/" + name + "_out")
        command = ["./stela-batch.sh",
                   "-i ",
                   input_file,
                   "-o ",
                   output_file,
                   "-eph_stela ",
                   output_eph_file,
                   "mean",
                   "keplerian CIRF"]
        time.sleep(0.1)
        CR = subprocess.call(command)
        time.sleep(0.1)
        os.chdir(self.stela_config.config["project"][
            "base"])

    def prepare(self, update_values):
        """
        prepare the file for extrapolation. (updates the reflectingArea when
        drag area is set.)

        Args:
                update_values (list)

        Kwargs:
                None

        Returns:
                name of the generated file. (str)
        """
        keys = sorted(self.stdp_sections, key=itemgetter("sort_number"),
                      reverse=False)
        counter = 0
        for i in update_values:
            if(keys[counter]["name"] == "dragArea"):
                self.stela_config.update_value(
                    "reflectingArea", i, keys[counter]["unit"])
            self.stela_config.update_value(
                keys[counter]["name"], i, keys[counter]["unit"])
            counter = counter + 1
        name = self.stela_config.generate_name()
        date = self.stela_config.get_date_now()
        self.stela_config.update_value("name", name)
        self.stela_config.update_value("date", date)
        self.stela_config.generate_xml()
        self.stela_config.agument_database()
        self.stela_config.db.update_all(self.stela_config.db_list)
        return name

    def write_to_log(self, logfile, to_write):
        """
        Writes to log, for debug only.
        """
        f = open(logfile, 'w')
        f.write(to_write)  # python will convert \n to os.linesep
        f.close()  # you can omit in most cases as the destructor will call it

    def generate_final_tuple(self, name, years):
        """
        Generate the tuple needed for the database entry in finalState

        Args:
                name (str)
                years (float)

        Kwargs:
                None

        Returns:
                dict
        """
        date = self.get_final_date(name)
        final_results = self.get_final_state_value(name)
        result = {}
        qu = "("
        keys = ()
        values = ()
        for i in final_results:
            qu = qu + "?,"
            keys = keys + (i.tag,)
            values = values + (i.text,)
        qu = qu + "?,?,?)"
        keys = keys + ('spaceObjectId', 'date', 'years')
        self.write_to_log("test.log", repr(
            self.stela_config.db.get_sat_id_by_name(name)))
        values = values + \
            (self.stela_config.db.get_sat_id_by_name(name)[0], date, years)
        result["qu"] = qu
        result["names"] = keys
        result["values"] = values
        return result

    def read_results(self, name):
        """
        Reads the result files to calculate different values.

        Args:
                filename (str)

        Kwargs:
                None

        Returns:
                None
        """
        try:
            self.doc = parse(str(self.path + "/" + name + "_out_sim.xml"))
            self.tree = ET.parse(str(self.path + "/" + name + "_out_sim.xml"))
        except IOError as e:
            return False

        return True

    def get_final_state_value(self, name):
        """
        Get the final status value that can be set in the database.

        Args:
                key (str)

        Kwargs:
                None

        Returns:
                Value
        """

        res = self.read_results(name)
        if(res):
            root = self.tree.getroot()
            finalstate = root.findall(
                str(".//finalState/bulletin/" + self.get_final_type() + "/*"))
            return list(finalstate)
        else:
            return self.get_inital_state_value()

    def get_inital_state_value(self):
        root = self.tree.getroot()
        initalstate = root.findall(
            str(".//initState/bulletin/" + self.get_inital_type() + "/*"))
        return list(initalstate)

    def get_final_date(self, name):
        """
        Get the Final Date. (as the Stela Formated Day.)

        Args:
                None

        Kwargs:
                None

        Returns:
                str
        """
        res = self.read_results(name)
        if(res):
            node = self.doc.getElementsByTagName(
                "finalState")[0].getElementsByTagName("date")
            return node[0].firstChild.nodeValue
        else:
            return self.get_initial_date(name)

    def get_initial_date(self, name):
        """
        Get the Initial Date. (as the Stela Formated Day.)

        Args:
                None

        Kwargs:
                None

        Returns:
                str
        """
        res = self.read_results(name)
        if(res):
            node = self.doc.getElementsByTagName(
                "initState")[0].getElementsByTagName("date")
            return node[0].firstChild.nodeValue
        else:
            self.doc = parse(str(self.path + "/" + name + "_a_sim.xml"))
            self.tree = ET.parse(str(self.path + "/" + name + "_a_sim.xml"))
            node = self.doc.getElementsByTagName(
                "initState")[0].getElementsByTagName("date")
            return node[0].firstChild.nodeValue

    def get_final_type(self):
        """
        Get the Simulation type in final mode.
        most of the time shoud be the same as initType.

        Args:
                None

        Kwargs:
                None

        Retruns:
                list
        """
        root = self.tree.getroot()
        finalstate = root.findall(".//finalState/bulletin")
        self.final_type = list(finalstate[0])[1].tag
        return list(finalstate[0])[1].tag

    def get_inital_type(self):
        root = self.tree.getroot()
        finalstate = root.findall(".//initState/bulletin")
        self.final_type = list(finalstate[0])[1].tag
        return list(finalstate[0])[1].tag

    def get_time_diff(self, name):
        """
        calcultes the time difference between to give time in the Stela format.

        Args:
                start_date (str YYYYMMDDTHH:MM:SS.MMM)
                end_date (str YYYYMMDDTHH:MM:SS.MMM)

        Kwargs:
                None

        Returns:
                float
        """
        if(self.read_results(name)):
            start_date = self.get_initial_date(name)
            final_date = self.get_final_date(name)
            days_in_year = 365.2425
            sd = datetime.strptime(start_date, "%Y-%m-%dT%H:%M:%S.%f")
            ed = datetime.strptime(final_date, "%Y-%m-%dT%H:%M:%S.%f")
            time_diff = ed - sd
            diff_in_years = time_diff.days / days_in_year
            return diff_in_years
        else:
            return 0
