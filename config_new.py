#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
import sys
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
    Read Stela XML configurations
    """

    def __init__(self,
                 db,
                 log_level="ERROR",
                 stela_file="stela.json",
                 step_file="stela_step.json",
                 start_file="stela_start.json",
                 ):
        logger = Logger(log_level)
        self.log = logger.get_logger()
        self.db = db
        self.stjs = stela_file
        self.stspjs = step_file
        self.ststjs = start_file
        self.multiparentage = []

    def add_to_db(self):
        """
        Adds the newly generated satelite to the database.

        Args:
                None

        Kwargs:
                None

        Returns:
                Boolean
        """

    def recursive_xml_generate(self, root, parent=""):
        """
        Generate the recursive xml element with from root object.

        Args:
                root Element
                parent ElementTree

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
        return prettify(self.root)

    def sort_by_parents_children(self, json_list):
        """
        Sorts the list descending with parent child relation.

        Args:
                json_list list

        Kwargs:
                None

        Returns:
                element
        """
        root = [item for item in json_list if item["parent"] == ""][0]
        self.find_children_element(root, json_list)
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
        if(len(element["children"]) > 0):
            element['children_obj'] = []
        while(len(element["children"]) > 0):
            c = element["children"].pop()
            element_tmp = self.find_element_by_name(c, json_list)
            if(len(element_tmp) > 0):
                element_t = element_tmp[0]
                element["children_obj"].append(element_t)
                element["children_obj"] = sorted(
                    element["children_obj"], key=itemgetter("sort_number"),
                    reverse=False)
                self.find_children_element(element_t, json_list)
        else:
            element.pop("children", None)

    def find_element_by_name(self, name, json_list):
        """
        Find an element by the given name. searches in alias

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
                element dict

        Kwargs:
                None

        Returns:
                dict (an element) or "{}"
        """
        if(type(element["parent"]) == list and len(element["parent"]) > 1):
            self.multiparentage.append(element)
            return True
        else:
            return False

    def solve_multi_parentage(self, needed_elements):
        """
        Solves the multiparentage problem. by adding multiparent element
        with only the right parent.


        Args:
                needed_elements list

        Kwargs:
                None

        Returns:
                needed_elements (list)
        """
        for i in self.multiparentage:
            a = [item for item in needed_elements if item[
                "parent"] in i["parent"]]
            if(len(a) > 0):
                i["parent"] = a[0]["parent"]
                needed_elements.append(i)
        return needed_elements

    def parents_exists(self, element, needed_elements, full_list):
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
            if(not self.element_exists(element, needed_elements)):
                needed_elements.append(element)
            parent_element = self.find_element_by_name(
                element["parent"], full_list)
            if(len(parent_element) > 0):
                if(not self.element_exists(parent_element[0],
                                           needed_elements)):
                    needed_elements.append(parent_element[0])
                self.parents_exists(
                    parent_element[0], needed_elements, full_list)

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
        stjs_file = open(self.stjs)
        stst_file = open(self.ststjs)
        stst_json = json.load(stst_file)
        stjs_json = json.load(stjs_file)
        stjs_sections = stjs_json["sections"]
        stst_sections = stst_json["sections"]
        stst_file.close()
        stjs_file.close()
        root = {}
        needed_elements = []
        for i in stst_sections:
            element = self.find_element_by_name(i["name"], stjs_sections)[0]
            if("value" in i):
                element["value"] = i["value"]
            self.parents_exists(element, needed_elements, stjs_sections)
            if(not self.multi_parentage(element)):
                parent_element = self.find_element_by_name(
                    element["parent"], stjs_sections)[0]
                needed_elements.append(element)
            if(not self.element_exists(parent_element, needed_elements)):
                needed_elements.append(parent_element)
        needed_elements = self.solve_multi_parentage(needed_elements)
        xml_feed = self.sort_by_parents_children(needed_elements)
        print self.recursive_xml_generate(xml_feed)

config = Config("satgen.db")
config.generate_xml()
