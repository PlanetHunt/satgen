#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
A dict for all the cfg xml transition names
STELA is sortsenstive, how the xml items are sorted play a role
"""


class ConfigDict:

    def get_sort_space_object(self):
        """
        Returns the sorting way of space object
        """
        return {
            "Mass": 1,
            "Drag Area": 2,
            "Reflecting Area": 3,
            "Reflectivity Coefficient": 4,
            "Orbit Type": 5,
            "Drag Coefficent Type": 6,
            "Drag Coefficent Type VARIABLE": 6,
            "Drag Coefficent Type CONSTANT": 7,
            "Constant Drag Coef": 8,
            "Name": 9}

    def get_sort_general(self):
        """
        Returns the sorting way for the general params
        """
        return {
            "Author": 1,
            "Comment": 2,
            "Simulation Duration": 3,
            "Simulation duration": 3,
            "Ephemeris Step": 4,
            "Ephemeris step": 4,
            "Difference Between Terrestrial And Universal Time": 5,
            "Difference between terrestrial and universal time": 5,
            "Solar radiation pressure switch": 6,
            "Solar Radiation Pressure Switch": 6,
            "Sun Switch": 7,
            "Sun switch": 7,
            "Moon Switch": 8,
            "Moon switch": 8,
            "Warning Flag": 9,
            "Iterative Mode": 10,
            "Model": 11,
            "Model": 11,
            "Atmospheric Model": 12,
            "Atmospheric model": 12,
            "Solar Activity Type": 13,
            "Integration Step": 14,
            "Integration step": 14,
            "Atmospheric drag switch": 15,
            "Atmospheric Drag Switch": 15,
            "Drag Quadrature Points": 16,
            "Drag quadrature Points": 16,
            "Atmospheric Drag Recompute Step": 17,
            "Atmospheric drag Recompute Step": 17,
            "Solar radiation pressure quadrature Points": 18,
            "Solar Radiation Pressure Quadrature Points": 18,
            "Reentry Altitude": 19,
            "Reentry altitude": 19,
            "Iteration Data": 20,
            "Iteration data": 20,
            "Tesseral Min Period": 21,
            "Zonal Order": 22,
            "Zonal order": 22}

    def get_sort_iteration_data(self):
        """
        Returns the Sorted list of Iteration data
        """
        return {
            "Function Value Accuracy": 1,
            "Expiring Duration": 2,
            "Simulation Minus Expiring Duration": 3,
            "Iteration Method": 4}

    def get_sort_solar_act(self):
        """
        Returns the sorting list for the solar activity
        """
        return {
            "Solar Activity Type": 1,
            "AP Constant Equivalent Solar Activity": 2,
            "F10.7 Constant Equivalent Solar Activity": 3}

    def get_unit_dict(self):
        """
        Returns the Dictionary needed for the Units
        """
        unit_dict = {
            "Mass": "kg",
            "Simulation duration": "years",
            "Simulation Duration": "years",
            "Ephemeris step": "s",
            "Ephemeris Step": "s",
            "Difference between terrestrial and universal time": "s",
            "Difference Between Terrestrial And Universal Time": "s",
            "a (Semi major axis)": "m",
            "A (Semi Major Axis)": "m",
            "lambdaEq": "rad",
            "Integration Step": "s",
            "Reentry Altitude": "m",
            "Function Value Accuracy": "days",
            "Expiring Duration": "years",
            "Simulation Minus Expiring Duration": "years",
            "Zp (Perigee altitude)": "m",
            "Za (Apogee altitude)": "m",
            "Zp (Perigee Altitude)": "m",
            "Za (Apogee Altitude)": "m",
            "Inclination": "rad",
            "I (Inclination)": "rad",
            "RAAN (Right Ascension of Ascending Node)": "rad",
            "M (Mean anomaly)": "rad",
            "w (Argument of perigee)": "rad",
            "RAAN (Right Ascension Of Ascending Node)": "rad",
            "M (Mean Anomaly)": "rad",
            "W (Argument Of Perigee)": "rad"}
        return unit_dict

    def get_dict(self):
        """
        Returns the Dictionary needed for the
        XML
        """
        config_dict = {
            "Stela Version": "STELAVersion",
            "Model": "modelType",
            "Author": "author",
            "Comment": "comment",
            "Simulation duration": "simulationDuration",
            "Simulation Duration": "simulationDuration",
            "Ephemeris step": "ephemerisStep",
            "Ephemeris Step": "ephemerisStep",
            "Difference between terrestrial and universal time": "ttMinusUT1",
            "Difference Between Terrestrial And Universal Time": "ttMinusUT1",
            "Integration Step": "integrationStep",
            "Atmospheric drag switch": "dragSwitch",
            "Atmospheric Drag Switch": "dragSwitch",
            "Drag quadrature Points": "dragQuadPoints",
            "Drag Quadrature Points": "dragQuadPoints",
            "Atmospheric Drag Recompute step": "atmosDragRecomputeStep",
            "Atmospheric Drag Recompute Step": "atmosDragRecomputeStep",
            "Solar radiation pressure switch": "srpSwitch",
            "Solar Radiation Pressure Switch": "srpSwitch",
            "Solar radiation pressure quadrature Points": "srpQuadPoints",
            "Solar Radiation Pressure Quadrature Points": "srpQuadPoints",
            "Iterative Mode": "IterativeMode",
            "Sun switch": "sunSwitch",
            "Sun Switch": "sunSwitch",
            "Moon switch": "moonSwitch",
            "Moon Switch": "moonSwitch",
            "Zonal order": "zonalOrder",
            "Zonal Order": "zonalOrder",
            "Earth Tesseral switch": "tesseralSwitch",
            "Earth Tesseral Switch": "tesseralSwitch",
            "Tesseral order": "Tesseralorder",
            "Tesseral min period": "nbIntegrationStepTesseral",
            "Tesseral Min Period": "nbIntegrationStepTesseral",
            "Reentry Altitude": "reentryAltitude",
            "Mass": "mass",
            "Warning Flag": "warningFlag",
            "Drag Area": "dragArea",
            "Reflecting Area": "reflectingArea",
            "Reflectivity Coefficient": "reflectivityCoefficient",
            "Orbit Type": "orbitType",
            "Drag Coefficent Type CONSTANT": "ConstantDragCoef",
            "Drag Coefficent Type VARIABLE": "VariableDragCoef",
            "Drag Coefficent Type COOK": "CookDragCoef",
            "Constant Drag Coef": "cstDragCoef",
            "Space Object": "SpaceObject",
            "SpaceObject": "SpaceObject",
            "General": "simGeneral",
            "iterationData": "iterationData",
            "LEOSimulation": "simGeneral",
            "Name": "name",
            "Initial": "initState",
            "Bulletin": "bulletin",
            "Edge Length": "EdgeLength",
            "Date": "date",
            "Type Perigee/Apogee": "Type0PosVel",
            "Type Cartesian": "Type1PosVel",
            "Type Keplerian": "Type2PosVel",
            "Type Equinoctial": "Type8PosVel",
            "Frame": "frame",
            "Nature": "nature",
            "Zp (Perigee altitude)": "perigeeAltitude",
            "Za (Apogee altitude)": "apogeeAltitude",
            "I (Inclination)": "inclination",
            "RAAN (Right Ascension of Ascending Node)": "rAAN",
            "Raan (Right Ascension Of Ascending Node)": "rAAN",
            "W (Argument Of Perigee)": "argOfPerigee",
            "w (Argument of perigee)": "argOfPerigee",
            "M (Mean Anomaly)": "meanAnomaly",
            "M (Mean anomaly)": "meanAnomaly",
            "A (Semi Major Axis)": "semiMajorAxis",
            "a (Semi major axis)": "semiMajorAxis",
            "E (Eccentricity)": "eccentricity",
            "e (Eccentricity)": "eccentricity",
            "lambdaEq": "lambdaEq",
            "Atmospheric model": "atmosModel",
            "Atmospheric Model": "atmosModel",
            "longitudeTFE": "longitudeTFE",
            "epochTFE": "epochTFE",
            "eX": "eX",
            "eY": "eY",
            "iX": "iX",
            "iY": "iY",
            "x": "x",
            "y": "y",
            "z": "z",
            "vX": "vX",
            "vY": "vY",
            "vZ": "vZ",
            "Solar Activity Type MEAN_CONSTANT": "ConstantEquivalentSolarActivity",
            "Solar Activity Type VARIABLE": "VariableSolarActivity",
            "Solar Activity Type CONSTANT": "ConstantSolarActivity",
            "Solar Activity Type": "solActType",
            "AP Constant Equivalent Solar Activity": "constantAP",
            "F10.7 Constant Equivalent Solar Activity": "constantF107",
            "Function Value Accuracy": "funcValueAccuracy",
            "Iteration Data": "iterationData",
            "Simulation Minus Expiring Duration": "simMinusExpDuration",
            "Iteration Method": "iterationMethod",
            "Expiring Duration": "expDuration",
            "Iterative Mode": "iterativeMode"}
        return config_dict

    def get_conf_sim(self, type_of_sim):
        """
        Gives an array of paramaters that are possible for everry Simulation
        Type Input: Type0PosVel, Type1PosVel, Type8PosVel and Type2PosVel
        """
        result = []
        if(type_of_sim == "Type0PosVel"):
            result = ["Frame", "Nature", "Zp (Perigee altitude)",
                      "Za (Apogee altitude)", "I (Inclination)",
                      "RAAN (Right Ascension of Ascending Node)",
                      "w (Argument of perigee)", "M (Mean anomaly)"]
        if(type_of_sim == "Type8PosVel"):
            result = [
                "Frame", "Nature", "a (Semi major axis)", "lambdaEq", "eX",
                "eY", "iX", "iY"]
        if(type_of_sim == "Type2PosVel"):
            result = ["Frame", "Nature", "a (Semi major axis)",
                      "e (Eccentricity)", "I (Inclination)",
                      "RAAN (Right Ascension of Ascending Node)",
                      "w (Argument of perigee)", "M (Mean anomaly)"]
        if(type_of_sim == "Type1PosVel"):
            result = ["Frame", "Nature", "x", "y", "z", "vX", "vY", "vZ"]
        return result
