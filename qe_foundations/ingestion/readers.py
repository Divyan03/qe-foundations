"""qe_foundations/ingestion/readers.py  -  TASK 4 (about 35 min)

One reader per format. Each returns a LIST OF RAW RECORDS and only deals with
FORMAT problems (is this valid CSV / JSON / XML? are the columns there?).
Business rules (is the status allowed? is the duration negative?) belong to
validation.py, NOT here.

Always open files through open_source() from contexts.py.
See README Task 4 for the exact contract of each reader.
"""

import csv
import json
import xml.etree.ElementTree as ET

from .contexts import open_source
from .exceptions import MalformedSourceError, MissingColumnsError
from .validation import REQUIRED_FIELDS


def read_csv_records(path):
    """CSV -> list of raw dicts, one per data row (use csv.DictReader)."""
    # raise NotImplementedError("Task 4A: write read_csv_records")
    with open_source(path) as file:
        reader = csv.DictReader(file)
        field_names = reader.fieldnames or []
        missing = []

        # if len(reader) == 0:
        #     raise MissingColumnsError(path, f"Header-only file")
        for r in REQUIRED_FIELDS:
            if r not in field_names:
                missing.append(r)
        if len(missing) > 0:
            raise MissingColumnsError(path, missing)
        return list(reader)

def read_json_records(path):
    """JSON -> list of raw records. Expected shape: {"suite": ..., "tests": [...]}."""
    # raise NotImplementedError("Task 4B: write read_json_records")
        # raise NotImplementedError("Task 4A: write read_csv_records")
    with open_source(path) as handle:
        try:
            data = json.load(handle)
        except json.JSONDecodeError as error:
            raise MalformedSourceError(path, f"invalid JSON at line {error.lineno}, column {error.colno}") from error

    if not isinstance(data, dict):
        raise MalformedSourceError(path, "top-level JSON value must be an object")

    if "tests" not in data:
        raise MalformedSourceError(path, "missing 'tests' field")

    if not isinstance(data["tests"], list):
        raise MalformedSourceError(path, "'tests' must be a list")

    return data["tests"]
    


def read_xml_records(path):
    """XML -> list of raw dicts, one per <testcase> element at ANY depth."""
    # raise NotImplementedError("Task 4C: write read_xml_records")
    tree = None
    records = []
    try:
        with open_source(path) as handle:
            tree = ET.parse(handle)
    except ET.ParseError as error:
        lin, col = error.position
        raise MalformedSourceError(path, f"invalid XML at line {lin}, column {col}") from error
    
    root = tree.getroot()

    for case in root.iter("testcase"):
        record = {}
        record["id"] = case.get("id")
        record["status"] = case.get("status")
        record["title"] = case.findtext("title")
        record["duration"] = case.findtext("duration")
        records.append(record)

    return records

    

