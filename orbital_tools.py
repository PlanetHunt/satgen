#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Orbital tools different calculation tools
for the give orbit
"""


class OrbitalTools:

    # Earth radius given in km
    self.earth_radius = 6378.137

    def calc_semi_major_axis(
            self,
            perigee,
            apogee,
            earth_radius=False):
        """
        Calculates the Semi Major axis from Apogee and Perigee
        Earth_radius Boolean, per default false if
        not added to Perigee and Apogee
        """
        apogee_earth = apogee + self.earth_radius
        perigee_earth = perigee + self.earth_radius

        return float((apogee_earth + perigee_earth) / 2)

    def calc_apogee(semi_major_axis, eccentricity):
        """
        Calculates the apogee from SemiMajor Axis and Eccentricity
        """
        return float((1 + eccentricity) * semi_major_axis)

    def calc_perigee(semi_major_axis, eccentricity):
        """
        Calculates the perigee from SemiMajor Axis and Eccentricity
        """
        return float((1 - eccentricity) * semi_major_axis)

    def calc_eccentricity(apogee, perigee):
        """
        Calculates the Eccentricity from Apogee and Perigee
        """
        return float((apogee - perigee) / (apogee + perigee))
