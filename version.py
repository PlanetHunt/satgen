#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Gives the version of Program from the version file
"""


class Version:
    def get_version(self):
        f = open("VERSION", "r+")
        version = list(f)[0]
        return version
