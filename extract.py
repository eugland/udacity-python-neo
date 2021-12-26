#!/usr/bin/python
# -*- coding: utf-8 -*-
"""Extract data on near-Earth objects and close approaches from CSV and
JSON files.

The `load_neos` function extracts NEO data from a CSV file, formatted as
described in the project instructions, into a collection of `NearEarthObject`s.

The `load_approaches` function extracts close approach data from a JSON file,
formatted as described in the project instructions, into a collection of
`CloseApproach` objects.

The main module calls these functions with the arguments provided at the
command line, and uses the resulting collections to build an `NEODatabase`.

You'll edit this file in Task 2.
"""

import csv
import json

from models import NearEarthObject, CloseApproach

# neos_id is map where key = neo designation and value = neos list index
neos_id = {}

# store all neos
neos = []

# store all approaces
approaches = []


def load_neos(neo_csv_path):
    """Read near-Earth object information from a CSV file.

    :param neo_csv_path: A path to a CSV file containing data about near-Earth
    objects.
    :return: A collection of `NearEarthObject`s.
    """

    # TODO: Load NEO data from the given CSV file.

    if not neo_csv_path:
        raise Exception('Cannot load data, no filename provided')
    """
    read request csv file and get required data  from each row
    and create neo Object and store into neos list
    """
    filename = neo_csv_path
    with open(filename, 'r') as f:
        csvfile = csv.DictReader(f, delimiter=',')
        for row in csvfile:
            neo_data = {
                'name': row['name'],
                'pha': row['pha'],
                'diameter': row['diameter'],
                'pdes': row['pdes'],
                }
            neo = NearEarthObject(**neo_data)
            """
            check neo is already added or not in neos list
            """
            if neo.designation not in neos_id:
                neos_id[neo.designation] = len(neos)
                neos.append(neo)
    return set(neos)


def load_approaches(cad_json_path):
    with open(cad_json_path, 'r') as infile:
        contents = json.load(infile)
    fields = contents['fields']

    """approaches are stored in approaches list where get
    reuired data and create CloseApproach object and stroe
    into appproaces list
    """
    # key for get index in  json  data for object
    key = {}
    for i in range(len(fields)):
        key[fields[i]] = i
    data = contents['data']
    count = 0
    for approach in data:
        approach_data = {
            'des': approach[key['des']],
            'cd': approach[key['cd']],
            'dist': approach[key['dist']],
            'v_rel': approach[key['v_rel']],
            }
        cad = CloseApproach(**approach_data)

        """check if that cad designation neos is eist or not
        if exist then refernece tha cad to neo and vice vers
        """
        if cad._designation in neos_id:
            neo_index = neos_id[cad._designation]
            neo = neos[neo_index]
            cad.setNeo(neo)
            neo.addCad(cad)
            neos[neo_index] = neo

        approaches.append(cad)
    return list(set(approaches))
