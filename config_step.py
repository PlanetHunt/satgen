#!/bin/env python
# -*- coding: utf-8 -*-

from logger import Logger
import itertools
import ast
import re


class ConfigStep:

    """
    This class reads the json step files and creates the needed combinations.
    It is not inteligent in creating the combinations at this time but can be
    better in this aspect impleingting the DEAP GA.

    If you want to add something to the combination you should edit the
    stela_step.json file as follows.

    {
    "name": "semiMajorAxis",
    "start": 6600,
    "end": 7200,
    "step": 50,
    "unit": "km"
    }

    in the section list.
    """

  def __init__(self, log_level="ERROR", step_json):
      """
      Initials the step configuration.

      Args:
                log_level (str)
                step_json (json list)

      Kwargs:
                None

      Returns:
                ConfigStep
      """
    self.logger = Logger(log_level)
    self.log = self.logger.get_logger()
    self.steps = step_json

  def add_edge_length(self, a, b):
    """
    Adds the edges toghether.

    Args:
            a,b (float)

    Kwargs:
            None

    Returs:
            tuple
    """
    return tuple(sum(x) for x in zip(a, b))

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
    return ast.literal_eval(tuple_str)

  def do_steps(self):
    """
    Returns all the possible values for different paramters in array
    With the help of this results, the combination matirx will be created
    """
    steps = self.get_step_conf()
    all_step_config = dict()
    for k, v in steps.items():
      tmp_list = list()
      all_step_config[k] = tmp_list
      start = v["Start Value"]
      end = v["End Value"]
      # special handling of edge length
      if(k == "Edge Length"):
        start = self.convert_to_tuple(start)
        end = self.convert_to_tuple(end)
        tmp_list.append(str(start))
        while(start != end):
          start = self.add_edge_length(
              start, self.convert_to_tuple(v["Step"]))
          tmp_list.append(str(start))
          print start
      else:
        tmp_list.append(float(start))
        while float(start) < float(end):
          start = float(start) + float(v["Step"])
          tmp_list.append(start)
    return all_step_config

  def get_combinations(self):
    """
    Returns all the possible combinations from the given dict
    it uses product function.
    """
    all_steps = self.do_steps()
    self.option = [k for k, v in all_steps.items()]
    result = itertools.product(*(v for k, v in all_steps.items()))
    return result

  def get_options(self):
    all_steps = self.get_step_conf()
    return self.option

steps = ConfigStep()
steps.read_conf("steps.cfg")
print list(steps.get_combinations())
print steps.get_options()
