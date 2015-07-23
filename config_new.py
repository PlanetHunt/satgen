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
      needed_elements.append(
          self.find_element_by_name(i["name"], stjs_sections)[0])
      sorted_elements = sorted(needed_elements, key=lambda k: k['sort_number'])
    # print needed_elements
    print sorted_elements


config = Config("satgen.db")
config.generate_xml()
