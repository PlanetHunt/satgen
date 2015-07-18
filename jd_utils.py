"""
Functions for converting dates to/from JD and MJD. Assumes dates are historical
dates, including the transition from the Julian calendar to the Gregorian
calendar in 1582. No support for proleptic Gregorian/Julian calendars.

:Author: Matt Davis
:Website: http://github.com/jiffyclub

"""

import math
import datetime as dt

# Note: The Python datetime module assumes an infinitely valid Gregorian
# calendar.
# The Gregorian calendar took effect after 10-15-1582 and the dates 1
# 0-05 through
# 10-14-1582 never occurred. Python datetime objects will produce incorrect
# time deltas if one date is from before 10-15-1582.


class JD:

    def mjd_to_jd(self, mjd):
        """
        Convert Modified Julian Day to Julian Day.

        Parameters
        ----------
        mjd : float
        Modified Julian Day

        Returns
        -------
        jd : float
        Julian Day
        """
        return mjd + 2400000.5

    def jd_to_date(self, jd):
        """
        Convert Julian Day to date.

        Algorithm from 'Practical Astronomy with your Calculator or
         Spreadsheet',4th ed., Duffet-Smith and Zwart, 2011.

        Parameters
        ----------
        jd : float
        Julian Day

        Returns
        -------
        year : int
        Year as integer. Years preceding 1 A.D. should be 0 or negative.
        The year before 1 A.D. is 0, 10 B.C. is year -9.

        month : int
        Month as integer, Jan = 1, Feb. = 2, etc.

        day : float
        Day, may contain fractional part.

        Examples
        --------
        Convert Julian Day 2446113.75 to year, month, and day.

        >>> jd_to_date(2446113.75)
        (1985, 2, 17.25)

        """
        jd = jd + 0.5

        F, I = math.modf(jd)
        I = int(I)

        A = math.trunc((I - 1867216.25) / 36524.25)

        if I > 2299160:
            B = I + 1 + A - math.trunc(A / 4.)
        else:
            B = I

        C = B + 1524

        D = math.trunc((C - 122.1) / 365.25)

        E = math.trunc(365.25 * D)

        G = math.trunc((C - E) / 30.6001)

        day = C - E + F - math.trunc(30.6001 * G)

        if G < 13.5:
            month = G - 1
        else:
            month = G - 13

        if month > 2.5:
            year = D - 4716
        else:
            year = D - 4715

        return year, month, day
