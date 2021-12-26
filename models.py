"""Represent models for near-Earth objects and their close approaches.

The `NearEarthObject` class represents a near-Earth object. Each has a unique
primary designation, an optional unique name, an optional diameter, and a flag
for whether the object is potentially hazardous.

The `CloseApproach` class represents a close approach to Earth by an NEO. Each
has an approach datetime, a nominal approach distance, and a relative approach
velocity.

A `NearEarthObject` maintains a collection of its close approaches, and a
`CloseApproach` maintains a reference to its NEO.

The functions that construct these objects use information extracted from the
data files from NASA, so these objects should be able to handle all of the
quirks of the data set, such as missing names and unknown diameters.

You'll edit this file in Task 1.
"""
from helpers import cd_to_datetime, datetime_to_str
from json import JSONEncoder
import datetime


class NearEarthObject(JSONEncoder):
    """A near-Earth object (NEO).

    An NEO encapsulates semantic and physical parameters about the object,
    such as its primary designation (required, unique), IAU name (optional),
    diameter in kilometers (optional - sometimes unknown), and whether it's
    marked as potentially hazardous to Earth.

    A `NearEarthObject` also maintains a collection of its close approaches -
    initialized to an empty collection, but eventually populated in the
    `NEODatabase` constructor.
    """
    def __init__(self, **info):
        """Create a new `NearEarthObject`.

        :param info: A dictionary of excess keyword arguments supplied to the
            constructor.
        """
        # check info is empty or not
        if (bool(info)):
            # check if info has required keys or not for all
            self.designation = info['pdes'] if 'pdes' in info else None
            self.name = info["name"] if (
                'name' in info and self.isBlank(info['name'])) else None
            self.hazardous = True if info["pha"] in ('Y', 'y') else False
            self.diameter = float(info["diameter"]) if (self.isBlank(
                info["diameter"])) else float('nan')
            # Create an empty initial collection of linked approaches.
            self.approaches = []
        else:
            self.designation = None
            self.name = None
            self.hazardous = False
            self.diameter = float('nan')
            self.approaches = []

    def addCad(self, approach):
        """ update CAD to in neo object"""
        self.approaches.append(approach)
        self.approaches = list(set(self.approaches))

    def isBlank(self, object):
        return bool(object and object.strip())

    @property
    def fullname(self):
        """Return a representation of the full name of this NEO."""
        return (f"{self.designation}"
                f"({self.name if self.name is not None else ''})")

    def __str__(self):
        """Return `str(self)`."""
        return (
            f"NEO {self.fullname} has a diameter of {self.diameter:.3f} km"
            f" and is {'' if self.hazardous else 'not '}potentially hazardous."
        )

    def __repr__(self):
        """Return `repr(self)`, a computer-readable string representation of
        this object."""
        return (f"NearEarthObject("
                f"designation={self.designation!r}, "
                f"name={self.name!r}, "
                f"diameter={self.diameter:.3f}, "
                f"hazardous={self.hazardous!r})")


class CloseApproach(JSONEncoder):
    """A close approach to Earth by an NEO.

    A `CloseApproach` encapsulates information about the NEO's close
    approach to Earth, such as the date and time (in UTC) of closest
    approach, the nominal approach distance in astronomical units, and
    the relative approach velocity in kilometers per second.

    A `CloseApproach` also maintains a reference to its `NearEarthObject` -
    initally, this information (the NEO's primary designation) is saved in a
    private attribute, but the referenced NEO is eventually replaced in the
    `NEODatabase` constructor.
    """
    def __init__(self, **info):
        """Create a new `CloseApproach`.

        :param info: A dictionary of excess keyword arguments supplied to
            the constructor.
        """
        self._designation = info["des"]
        self.time = cd_to_datetime(info["cd"])
        self.distance = float(info["dist"])
        self.velocity = float(info["v_rel"])

        # Create an attribute for the referenced NEO, originally None.
        self.neo = None

    def setNeo(self, neo):
        self.neo = neo

    @property
    def time_str(self):
        """Return a formatted representation of this `CloseApproach`'s
        approach time.

        The value in `self.time` should be a Python `datetime` object.
        While a `datetime` object has a string representation, the default
        representation includes seconds - significant figures that don't
        exist in our input data set.

        The `datetime_to_str` method converts a `datetime` object to a
        formatted string that can be used in human-readable representations and
        in serialization to CSV and JSON files.
        """
        return datetime_to_str(self.time)

    def __str__(self):
        """Return `str(self)`."""
        return (f"On {self.time_str}, "
                f"'{self.neo.fullname}'"
                f"approaches Earth at a distance of {self.distance:.2f}au "
                f"and a velocity of {self.velocity:.2f} km/s.")

    def __repr__(self):
        """Return `repr(self)`, a computer-readable string representation of
            this object."""
        return (f"CloseApproach(time={self.time_str!r}, "
                f"distance={self.distance:.2f}, "
                f"velocity={self.velocity:.2f}, "
                f"neo={self.neo!r})")
