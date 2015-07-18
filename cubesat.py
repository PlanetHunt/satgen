#!/usr/bin/env python

import urllib2
from sgp4.earth_gravity import wgs72
from sgp4.io import twoline2rv
from sgp4 import propagation
import math


class Sat:

    """
    create primary satellite object from the TLE data
    """

    def __init__(self, name, tle1, tle2):
        self.tle1 = tle1
        self.tle2 = tle2
        self.name = name

    def __str__(self):
        return "(" + self.get_name() + ", " + self.get_tle1() + ", " +\
            self.get_tle2() + ")"

    def get_tle1(self):
        return self.tle1

    def get_tle2(self):
        return self.tle2

    def get_name(self):
        return self.name

    __repr__ = __str__

response = urllib2.urlopen("http://celestrak.com/NORAD/elements/cubesat.txt")
data = response.readlines()

sats = []
thc = 0  # three counter count three and set to zero again.
for d in data:
    if(thc < 3):
        if(thc == 0):
            tmp_sat_name = d.rstrip()
            thc = thc + 1
        elif(thc == 1):
            tmp_sat_tle1 = d.rstrip()
            thc = thc + 1
        else:
            tmp_sat_tle2 = d.rstrip()
            sat = Sat(tmp_sat_name, tmp_sat_tle1, tmp_sat_tle2)
            sats.append(sat)
            thc = 0


earth_radius = 6378.137
print "sat_name, sma, inclination,ecco"
for sat in sats:
    satellite = twoline2rv(sat.get_tle1(), sat.get_tle2(), wgs72)
    satellite.propagate(2014, 8, 1, 12, 50, 19)
    satllite_data = propagation._initl(satellite.satnum, satellite.whichconst,
                                       satellite.ecco,
                                       satellite.jdsatepoch, satellite.inclo,
                                       satellite.no, satellite.method, "a")
    print sat.get_name() + "," + str(satllite_data[3] * earth_radius) + "," +\
        str(math.degrees(satellite.inclo)) + "," + str(satellite.ecco)
