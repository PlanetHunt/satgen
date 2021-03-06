#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Main satgen program. Collects the data from the user and put it toghether for
simulation tools to work with.
"""
import os
import argparse
import random
import string
from config import Config
from config_converter import Converter
from config_parser import ConfParser
from config_step import ConfigStep
from database import DB


def set_verbose_level(level, quiet=False):
    """
    Set the different verbosity level.

    Args:
        level (int):  Level number to be set-.

    Kwargs:
        quiet (bool):  If it should be quiet.

    Returns:
        str. The return values::

            ERROR -- 0
            WARNING -- 1
            INFO -- 2
            Debug -- > 2
    """
    verbose = "ERROR"
    if(level == 0 or quiet):
        verbose = "ERROR"
    elif(level == 1):
        verbose = "WARNING"
    elif (level == 2):
        verbose = "INFO"
    elif (level > 2):
        verbose = "DEBUG"
    return verbose


def name_generator(size=8, chars=string.ascii_uppercase + string.digits):
    """
    Generates Random UPPERCASE names for the satellite taken from
    http://stackoverflow.com/q/2257441
    """
    return ''.join(random.choice(chars) for _ in range(size))


def set_name(name=False):
    """
    Set the name of the satellite
    """
    if not name:
        name = name_generator()
    return name


def set_options(conf, combination, options):
    """
    Set the options with the different combinations
    """
    count = 0
    for combi in combination:
        conf.set_value(combi, options[count])
        count = count + 1


def get_output_dir(direct="default"):
    """
    Gets the output directory
    """
    result = ""
    if(direct == "default"):
        result = ""
    else:
        result = direct
    return result

parser = argparse.ArgumentParser(
    description="SatGen, the Satellite generator.")
group_mutal = parser.add_mutually_exclusive_group()
group_mutal.add_argument(
    "-v",
    "--verbose",
    help="verbose logging",
    action="count",
    default=0)
group_mutal.add_argument(
    "-q",
    "--quiet",
    help="quiet mode",
    action="store_true")
parser.add_argument(
    "-n",
    "--name",
    nargs='?',
    help="satellite name (default random 8 chars)")
parser.add_argument(
    "-c",
    "--config",
    nargs='?',
    help="config file, read config from cfg")
parser.add_argument(
    "-s",
    "--step",
    nargs='?',
    help="step file for the generation of xml files")
parser.add_argument(
    "-o",
    "--outputfolder",
    nargs='?',
    help="output folder")
parser.add_argument(
    "-e",
    "--extrapolate",
    action="store_true",
    help="extraploate")
parser.add_argument(
    "-r",
    "--root",
    nargs=1,
    help="root sim")
parser.add_argument(
    "-d",
    "--database",
    nargs=1,
    help="database_file")
parser.add_argument(
    "-u",
    "--addu",
    action="store_true",
    help="if u most be set")
parser.add_argument(
    "-t",
    "--timediff",
    action="store_true",
    help="if set, calculates the timediff and put it in the database")
args = parser.parse_args()
db = DB(args.database[0])
db.create_all_tables()
verbose = set_verbose_level(args.verbose, args.quiet)
config = Config(db, log_level=verbose)

if(args.database and args.addu):
    db.set_u()

if(args.database and args.timediff):
    db.time_convert()
if(args.step):
    steps = ConfigStep()
    steps.read_conf(args.step)
    combinations = steps.get_combinations()
    options = steps.get_options()
if(args.config):
    conf_parser = ConfParser(log_level=verbose)
    config_from_file = conf_parser.read_file(args.config)
    config.set_conf(config_from_file)
if(args.step and combinations and options):
    for combination in combinations:
        name = set_name(args.name)
        config.set_space_object_name(name)
        set_options(config, combination, options)
        db.update_all(config)
        directory = get_output_dir(args.outputfolder)
        fh = open(directory + "/" + config.get_xml_file_name(), "w+")
        fh.write(config.convert_to_xml())
        fh.close
