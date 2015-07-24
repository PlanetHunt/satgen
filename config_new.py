#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
import sys
import xml.etree.ElementTree as ET
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

  def find_child_element(self, element, json_list):
    """
    Finds the children of the element by the given element. json_list

    Args:
            element (dict)
            json_list (list)

    Kwargs:
            None

    Returns:
            list of elements (empty list when nothing found)
    """

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
      a = [item for item in needed_elements if item["parent"] in i["parent"]]
      i["parent"] = a[0]["parent"]
      needed_elements.append(i)
    return needed_elements

  def find_parents(self, section):
    """
    Finds the element's parent if any exists.

    Args:
            section (dict)

    Kwargs:
            None

    Returns:
            list (Empty if False)
    """
    if(len(section["parent"]) > 0):
      if(type(section["parent"] != list)):
        return section["parent"]
      else:
        return [section["parent"]]
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
    return (len([item for item in json_list if item["name"] == element["name"]]) > 0)

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
      element["value"] = i["value"]
      if(not self.multi_parentage(element)):
        parent_element = self.find_element_by_name(
            element["parent"], stjs_sections)[0]
        needed_elements.append(element)
      if(not self.element_exists(parent_element, needed_elements)):
        needed_elements.append(parent_element)
      # sorted_elements = sorted(needed_elements, key=lambda k:
      # k['sort_number'])
    needed_elements = self.solve_multi_parentage(needed_elements)
    for i in needed_elements:
      if(len(self.find_parents(i)) == 0):
        root = i



config = Config("satgen.db")
config.generate_xml()
