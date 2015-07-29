#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Converts needed values from m->km or km->m and so on.
For the conversion pint library have been used.
"""
from pint import UnitRegistry
from logger import Logger


class UnitConverter():

    def __init__(self, log_level="ERROR"):
        logger = Logger(log_level)
        self.log = logger.get_logger()
        self.ureg = UnitRegistry()

    def convert(self, from_unit, to_unit, value):
        """
        Converts from a unit to another one.

        Args:
                form_unit (str)
                to_unit (str)
                value (float)

        Kwargs:
                None

        Returns:
                float
        """
        if(from_unit != to_unit):
            if(from_unit == "m"):
                value_with_unit = value * self.ureg.m
                return (value_with_unit.to(self.ureg.km)).magnitude
            elif(from_unit == "km"):
                value_with_unit = value * self.ureg.km
                return (value_with_unit.to(self.ureg.m)).magnitude
            elif(from_unit == "rad"):
                value_with_unit = value * self.ureg.rad
                return (value_with_unit.to(self.ureg.deg)).magnitude
            elif(from_unit == "deg"):
                value_with_unit = value * self.ureg.deg
                return (value_with_unit.to(self.ureg.rad)).magnitude

    def km_to_m(self, value):
        """
        Converts a value from km to m
        """
        value_with_unit = value * self.ureg.km
        return (value_with_unit.to(self.ureg.m)).magnitude

    def m_to_km(self, value):
        """
        Converts a value from m to km
        """
        value_with_unit = value * self.ureg.m
        return (value_with_unit.to(self.ureg.km)).magnitude

    def rad_to_deg(self, value):
        """
        Converts radians to degrees
        """
        value_with_unit = value * self.ureg.rad
        return (value_with_unit.to(self.ureg.deg)).magnitude

    def deg_to_rad(self, value):
        """
        Converts degrees to radian
        """
        value_with_unit = value * self.ureg.deg
        return (value_with_unit.to(self.ureg.rad)).magnitude
