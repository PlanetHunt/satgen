#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Satellite Simulation Configuration Parser.
Reads data from the Text or XML config file
"""

import ConfigParser
import io
import re
import os.path
from logger import Logger
from config_converter import Converter


class ConfParser:

    def __init__(self, log_level="ERROR"):
        self.logger = Logger(log_level)
        self.log = self.logger.get_logger()

    def config_parser_generator(self):
        """
        generates ConfigParser objects where needed
        """
        config = ConfigParser.ConfigParser()
        return config

    def check_new_file_cfg(self, file_name):
        """
        Matches the name with cfg pattern
        """
        pattern = "(\w+.cfg)"
        if(re.match(pattern, file_name)):
            return True
        else:
            return False

    def check_file(self, file_address):
        """
        Check if the file has the right syntax.
        Mainly the name.cfg.
        """
        converter = Converter()
        f = open(file_address, "r+")
        directory = os.path.dirname(os.path.abspath(file_address))
        file_name_full = converter.get_file_container(f)
        file_name = file_name_full["name"]
        given_name = ""
        try:
            tmp_config = self.config_parser_generator()
            tmp_config.read(f.name)
            del tmp_config
            return f.name
        except ConfigParser.ParsingError as e:
            self.log.warning(
                "The file was not cfg, converted to cfg file.")
            if(file_name + ".cfg" in os.listdir(directory)):
                while(not self.check_new_file_cfg(given_name) and
                      given_name != 'q'):
                    self.log.warning("The file name must be name+.cfg")
                    given_name = raw_input(
                        "The file already exists in this directory, "
                        "give a new name?(press q to exit)")
                if(given_name != 'q'):
                    written_file_name = given_name.strip()
                    converter.convert_file(f.name, written_file_name)
                    file_name = written_file_name
                else:
                    raise
                    self.log.error("The file name must be given")
            else:
                file_name = converter.convert_file(f.name)
            return file_name

    def strip_alpha(self, word):
        """
        removes all alphabetic chars from the word
        """
        return re.sub("[^0123456789\.]", "", word)

    def read_file(self, file_address):
        """
        Reads the config file contents and
        generates a configuration dict
        """
        config = self.config_parser_generator()
        file_name = self.check_file(file_address)
        config.read(file_name)
        sections = config.sections()
        configs = {}
        for section in sections:
            configs[section] = {}
            for option in config.options(section):
                # use the title to capitlize the first leter.
                # see here:
                # https://stackoverflow.com/q/12410242
                config_value = config.get(section, option, True)
                if(re.search("(?=.*\d)(?=.*[A-Za-z])[A-Za-z0-9]",
                             config_value) and
                   option != "atmospheric model"):
                    config_value = self.strip_alpha(config_value)
                configs[section][option.title()] = config_value
        return configs
