#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json
import random
from extrapolate_new import Extrapolate
from deap import creator, base, tools, algorithms


class GA:

    def __init__(self, var_constraints, result_constraint):
        """
        GA Class is the genetic algorithm runner class. it needs two options
        to be set. first the variables constraints which limits varaibles
        containgency and the result constraint which moves the algorithm toward
        the result. our problem here is a Min problem. For the genetic algorithm
        the deap toolkit from university of Alberta is used. At this moment
        GA is not multiparamtered, but as extrapolation of objects far away
        takes much longer the execution time can also be considered as a factor.
        this is only related to STELA. For master GA can not be combined with
        time.

        Args:
                var_constraints (dict)
                result_constraint (float)

        Kwargs:
                None

        Returns:
                None
        """
        self.var_constr = var_constraints
        self.res_constr = result_constraint

    def initSat(self, icls):
        """
        Initializes random satellites within given constraints.
        """

    def evalSat(self):
        """
        Evaluates satellite's lifetime with the help of STELA and compare
        it to the result constraint.
        """

    def run(self):
        """
        Runs the genetic algorithm.
        """
