#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
import sys
import os
import itertools
import string
import random
import xml.etree.ElementTree as ET
from awesome_print import ap
from ast import literal_eval
from operator import itemgetter
from xml_pretty import prettify
from time import gmtime, strftime
from logger import Logger
from database import DB
from unit_converter import UnitConverter


class Config:

    """
    Read STELA XML configurations, create the config files and add the satelite
    in database. This module is only generate only STELA compatible data.
    To get data out of database user should use or change the database package.
    """

    def __init__(self,
                 db,
                 log_level="ERROR",
                 stela_file="stela.json",
                 step_file="stela_step.json",
                 start_file="stela_start.json",
                 config_file="config.json"
                 ):
        logger = Logger(log_level)
        self.log = logger.get_logger()
        self.db = DB(db)
        self.convert = UnitConverter(log_level)
        try:
            stjsha = open(stela_file)
            ststha = open(start_file)
            stspha = open(step_file)
            confha = open(config_file)
        except IOError as e:
            print "One (more) of the config files is not avaialbe."
            print e
            raise
        try:
            self.stjs_sections = json.load(stjsha)["sections"]
            self.stst_sections = json.load(ststha)["sections"]
            self.stsp_sections = json.load(stspha)["sections"]
            self.config = json.load(confha)["config"]
        except ValueError as e:
            print "One (more) of the config files is not valid json."
            print e
            raise
        stjsha.close()
        ststha.close()
        stspha.close()
        confha.close()
        self.combination_option = []
        self.db_list = {}
        self.multiparentage = []
        self.needed_elements = []

    def add_edge_length(self, a, b):
        """
        Adds the edges toghether.

        Args:
                a,b (float)

        Kwargs:
                None

        Returns:
                tuple
        """
        return tuple(sum(x) for x in zip(a, b))

    def calculate_drag_area(self, edge_tuple):
        """
        Calculates the drag area with the given tuple.

        Args:
                  edge_tuple (tuple)

        Kwargs:
                  None

        Returns:
                  float
        """
        area = 0
        for i in itertools.combinations(edge_tuple, 2):
            area = ((i[0] * i[1]) * 2) + area
        return float(area / 4)

    def convert_to_tuple(self, tuple_str):
        """
        Converts the given tuple string to a tuple python object.

        Args:
                tuple_str (str)

        Kwargs:
                None

        Returns:
                tuple
        """
        return literal_eval(tuple_str)

    def do_steps(self):
        """
        Create the steps from the json step files. Please be cautious how you
        fill file. The application will stop working if the values here are
        not set correctly.
        If you want to add something to the combination you should edit the
        stela_step.json file as follows:
        {
        "name": "semiMajorAxis",
        "start": 6600,
        "end": 7200,
        "step": 50,
        "unit": "km"
        }

        Args:
                None

        Kwargs:
                None

        Returns:
                dict
        """
        steps = self.stsp_sections
        all_step_config = dict()
        for k in steps:
            if(k["end"] < k["start"]):
                print "The 'end' smaller than 'start', please change the '" + \
                    str(k["name"]) + "' settings in the stela_step.json file."
                raise ValueError
            tmp_list = list()
            all_step_config[k["name"]] = tmp_list
            start = k["start"]
            end = k["end"]
            if(k["type"] == "tuple"):
                start = self.convert_to_tuple(start)
                end = self.convert_to_tuple(end)
                tmp_list.append(str(start))
                while(start != end):
                    start = self.add_edge_length(
                        start, self.convert_to_tuple(k["step"]))
                    tmp_list.append(str(start))
            else:
                if(not (k["unit"] == self.find_element_by_name(k["name"], self.needed_elements)[0]["unit"])):
                    start = self.convert.convert(k["unit"], self.find_element_by_name(
                        k["name"], self.needed_elements)[0]["unit"], float(start))
                    step = self.convert.convert(k["unit"], self.find_element_by_name(
                        k["name"], self.needed_elements)[0]["unit"], float(k["step"]))
                    end = self.convert.convert(k["unit"], self.find_element_by_name(
                        k["name"], self.needed_elements)[0]["unit"], float(k["end"]))
                else:
                    start = float(start)
                    step = float(k["step"])
                tmp_list.append(float(start))
                while float(start) < float(end):
                    start = float(start) + float(step)
                    tmp_list.append(start)
        return all_step_config

    def get_combinations(self):
        """
        Returns all the possible combinations from the given dict
        it uses product function.

        Args:
                None

        Kwargs:
                None

        Returns:
                itertools.product
        """
        all_steps = self.do_steps()
        self.combination_option = [k for k, v in all_steps.items()]
        self.combination_option.append("name")
        self.combination_option.append("date")
        result = itertools.product(*(v for k, v in all_steps.items()))
        return result

    def get_combination_options(self):
        """
        Returns the options from the combinations.

        Args:
               None

        Kwargs:
               None

        Returns:
               list
        """
        if(len(self.combination_option) == 0):
            self.get_combinations()
        return self.combination_option

    def generate_name(self, size_of=8):
        """
        Generates Random UPPERCASE names for the satellite taken from
        http://stackoverflow.com/q/2257441

        Args:
                size (int)

        Kwargs:
                None

        Returns:
                str
        """
        return ''.join(random.choice(string.ascii_uppercase + string.digits)
                       for _ in range(size_of))

    def get_path(self):
        """
        Finds the right pass to save the xml file created.

        Args:
                  None

        Kwargs:
                  None

        Returns:
                  None
        """
        if(not os.path.isdir(self.config["sim"]["path"])):
            os.mkdir(self.config["sim"]["path"])
        return self.config["sim"]["path"] + "/" + \
            [item for item in self.needed_elements
             if item["name"] == "name"][0]["value"] + "_a_sim.xml"

    def agument_database(self):
        """
        Adds the varaible data to the database, which not comming with start
        data. The qus are always the second in the database object.

        Args:
                  None

        Kwargs:
                  None

        Retruns:
                  None
        """
        for i in self.db_list.items():
            qu = i[1]
            qu = qu["qu"][:-1] + ")"
            self.db_list[i[0]]["qu"] = qu

    def get_element_index(self, element, json_list):
        """
        Finds an element index in a given list.

        Args:
                element (dict)
                json_list (list)

        Kwargs:
                None

        Returns:
                int (index within)
        """
        return [i for i, val in enumerate(
            json_list) if element["name"] == val["name"]][0]

    def exchange_element(self, element, json_list):
        """
        Exchanges the element with the same element given in a list
        and also the database.

        Args:
                  element (dict)
                  json_list (list)

        Kwargs:
                  None

        Returns:
                  None
        """
        index = self.get_element_index(element, json_list)
        self.set_new_value_in_db_list(element)
        json_list.pop(index)
        json_list.append(element)

    def set_new_value_in_db_list(self, element):
        """
        Finds the element index in the database element dict.

        Args:
                element (dict)

        Kwargs:
                None

        Returns:
                int
        """
        index = [item for item in self.db_list.items()
                 if element["database_tag"] == item[0]][0]
        index2 = [i for i, val in enumerate(
            list(index)[1]["names"]) if element["name"] == val][0]
        values = list(index[1]["values"])
        values[index2] = element["value"]
        self.db_list[index[0]]["values"] = tuple(values)

    def generate_json_stub(self, json_file, **vars):
        """
        Generate a json stub or appends to it for the given paramater names.

        Args:
                json_file (str) address of the given json file

        Kwargs:
                parameters name (str)

        Returns:
                None
        """

    def agument_config(self, combination):
        """
        Infulence the STELA settings with the created combinations.

        Args:
                  combination (list)

        Kwargs:
                  None

        Returns:
                  None
        """
        counter = 0
        for o in self.combination_option:
            if(o == "Length"):
                new_value = combination[counter]
                self.update_value("dragArea", self.calculate_drag_area(
                    self.convert_to_tuple(new_value)))
                self.update_value("reflectingArea", self.calculate_drag_area(
                    self.convert_to_tuple(new_value)))
                counter = counter + 1
            else:
                new_value = combination[counter]
                self.update_value(o, new_value)
                counter = counter + 1

    def update_value(self, name, value):
        """
        Update a value in the needed elements.

        Args:
                name (str)
                value (float)

        Kwargs:
                None

        Returns:
                None
        """
        element = self.find_element_by_name(name, self.needed_elements)[0]
        element["value"] = value
        self.exchange_element(element, self.needed_elements)

    def add_element_to_db_tuple(self, element):
        """
        Adds the newly generated satelite to the database.

        Args:
                element (dict)

        Kwargs:
                None

        Returns:
                None
        """
        if("database_tag" in element and "value" in element):
            if(element["database_tag"] != ""):
                if(element["database_tag"] not in list
                   (self.db_list.keys())):
                    self.db_list[element["database_tag"]] = {}
                    self.db_list[element["database_tag"]][
                        "names"] = (str(element["xml_tag"]),)
                    if(type(element["value"]) != str):
                        self.db_list[element["database_tag"]][
                            "values"] = (element["value"],)
                    else:
                        self.db_list[element["database_tag"]][
                            "values"] = (str(element["value"]),)
                    self.db_list[element["database_tag"]]["qu"] = "(?,"
                else:
                    if(element["xml_tag"] not in
                       self.db_list[element["database_tag"]]["names"]):
                        self.db_list[element["database_tag"]]["names"] = self.db_list[
                            element["database_tag"]]["names"] +\
                            (str(element["xml_tag"]),)
                        if(type(element["value"]) != str):
                            self.db_list[element
                                         ["database_tag"]]["values"] = self.db_list[
                                element["database_tag"]]["values"] + \
                                (element["value"],)
                        else:
                            self.db_list[element
                                         ["database_tag"]]["values"] = self.db_list[
                                element["database_tag"]]["values"] + \
                                (str(element["value"]),)
                        self.db_list[element
                                     ["database_tag"]]["qu"] = self.db_list[element["database_tag"]]["qu"] + "?,"

    def recursive_xml_generate(self, root, parent=""):
        """
        Generate the recursive xml element with from root object.

        Args:
                root (Element)
                parent (ElementTree)

        Kwargs:
                None

        return:
                string
        """
        if(root["parent"] == ""):
            ETS = ET.Element(root["xml_tag"])
            self.root = ETS
        else:
            ETS = ET.SubElement(parent, root["xml_tag"])
        if(len(root["default_parms"]) > 0):
            for i in root["default_parms"]:
                if(type(i) == dict):
                    ETS.set(list(i.keys())[0], list(i.values())[0])
        if(root["unit"] != ""):
            ETS.set("unit", root["unit"])
        if("value" in root):
            ETS.text = str(root["value"])
        if("children_obj" in root):
            if(len(root["children_obj"]) > 0):
                for i in root["children_obj"]:
                    self.recursive_xml_generate(i, ETS)
        ET.ElementTree(self.root).write(
            self.get_path(),
            encoding="UTF-8",
            xml_declaration=True)

    def sort_by_parents_children(self):
        """
        Sorts the list descending with parent child relation.

        Args:
                None

        Kwargs:
                None

        Returns:
                element
        """
        root = [
            item for item in self.needed_elements if item["parent"] == ""][0]
        self.find_children_element(root, self.needed_elements)
        root.pop("children", None)
        root["children_obj"] = sorted(
            root["children_obj"], key=itemgetter("sort_number"),
            reverse=False)
        return root

    def find_children_element(self, element, json_list):
        """
        finds and adds element as childeren to their parents.

        Args:
                element (dict)
                json_list (list)

        Kwargs:
                None

        Returns:
                None
        """
        if("children" in element):
            if(len(element["children"]) > 0):
                element['children_obj'] = []
                while(len(element["children"]) > 0):
                    child = element["children"].pop()
                    element_tmp = self.find_element_by_name(child, json_list)
                    if(len(element_tmp) > 0):
                        element_t = element_tmp[0]
                        element["children_obj"].append(element_t)
                        element["children_obj"] = sorted(
                            element["children_obj"], key=itemgetter(
                                "sort_number"),
                            reverse=False)
                        self.find_children_element(element_t, json_list)
            else:
                element.pop("children", None)

    def find_element_by_name(self, name, json_list):
        """
        Find an element by the given name. searches in alias.

        Args:
                name (str)
                json_list (list)

        Kwargs:
                None

        Returns:
                dict
        """
        result = [item for item in json_list if item["name"] == name]
        if (len(result) == 0):
            return [item for item in json_list if name in item["alias"]]
        else:
            return result

    def multi_parentage(self, element):
        """
        Solves the multiparentage problem, when one exists.

        Args:
                element (dict)

        Kwargs:
                None

        Returns:
                Boolean
        """
        if(type(element["parent"]) == list and len(element["parent"]) > 1):
            self.multiparentage.append(element)
            return True
        else:
            return False

    def solve_multi_parentage(self):
        """
        Solves the multiparentage problem. by adding multiparent element
        with only the right parent.


        Args:
                needed_elements list

        Kwargs:
                None

        Returns:
                None
        """
        for element in self.multiparentage:
            a = [item for item in self.needed_elements if item[
                "parent"] in element["parent"]]
            if(len(a) > 0):
                element["parent"] = a[0]["parent"]
                self.needed_elements.append(element)
                self.add_element_to_db_tuple(element)

    def parents_exists(self, element, full_list):
        """
        Searches in the full element list for the parents of the given
        element and add it to the given list.

        Args:
                element (dict)
                needed_elements (list)
                full_list (list)

        Kwargs:
                None

        Returns:
                None
        """
        if(element["parent"] != ""):
            if(not self.element_exists(element, self.needed_elements)):
                self.needed_elements.append(element)
            parent_element = self.find_element_by_name(
                element["parent"], full_list)
            if(len(parent_element) > 0):
                if(not self.element_exists(parent_element[0],
                                           self.needed_elements)):
                    self.needed_elements.append(parent_element[0])
                self.parents_exists(
                    parent_element[0], full_list)

    def find_parents(self, element):
        """
        Finds the element's parent if any exists.

        Args:
                element (dict)

        Kwargs:
                None

        Returns:
                list (Empty if False)
        """
        if(len(element["parent"]) > 0):
            if(type(element["parent"] != list)):
                return element["parent"]
            else:
                return [element["parent"]]
        else:
            return []

    def add_name_to_combination(self, combination):
        """
        Adds the name to the combination

        Args:
                combination (tuple)

        Kwargs:
                None

        Returns:
                 tuple (new combination)
        """
        combination_list = list(combination)
        combination_list.append(self.generate_name())
        return tuple(combination_list)

    def add_date_to_combination(self, combination):
        """
        Update the date for the given STELA sim object.

        Args:
                combination (tuple)

        Kwargs:
                None

        Returns:
                tuple (new combination)
        """
        combination_list = list(combination)
        date = strftime("%Y-%m-%dT%H:%M:%S.000", gmtime())
        combination_list.append(date)
        return tuple(combination_list)

    def element_exists(self, element, json_list):
        """
        Checks if an element exists in the given json_list.

        Args:
                element (dict)
                json_list (list)

        Kwargs:
                None

        Returns:
                Boolean
        """
        return (len([item for item in json_list if item["name"] ==
                     element["name"]]) > 0)

    def generate_xml(self):
        """
        Generate the xml file for stela from given data.

        Args:
                None

        Kwargs:
                None

        Returns:
                Boolean
        """
        if(len(self.needed_elements) == 0):
            self.generate_foundation_xml()
            xml_feed = self.sort_by_parents_children()
            print self.get_path()
            self.recursive_xml_generate(xml_feed)
        else:
            xml_feed = self.sort_by_parents_children()
            print self.get_path()
            self.recursive_xml_generate(xml_feed)

    def generate_foundation_xml(self):
        """
        Generate the xml file for stela from given data.

        Args:
                None

        Kwargs:
                None

        Returns:
                Boolean
        """
        for i in self.stst_sections:
            element = self.find_element_by_name(
                i["name"], self.stjs_sections)[0]
            if("value" in i):
                element["value"] = i["value"]
            self.parents_exists(element, self.stjs_sections)
            if(not self.multi_parentage(element)):
                parent_element = self.find_element_by_name(
                    element["parent"], self.stjs_sections)[0]
                self.add_element_to_db_tuple(element)
            if(not self.element_exists(parent_element, self.needed_elements)):
                self.needed_elements.append(element)
                self.add_element_to_db_tuple(element)
        self.solve_multi_parentage()
        self.generate_xml()

config = Config("satgen.db")
config.generate_xml()
combinations = config.get_combinations()
config.agument_database()
config.db.create_all_tables()
for c in combinations:
    c = config.add_name_to_combination(c)
    c = config.add_date_to_combination(c)
    config.agument_config(c)
    config.db.update_all(config.db_list)
    config.generate_xml()
