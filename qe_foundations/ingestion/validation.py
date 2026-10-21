"""qe_foundations/ingestion/validation.py  -  TASK 5 (about 25 min)

validate_record() decides whether ONE raw record is acceptable.

IMPORTANT: this is VALIDATION OF EXTERNAL DATA. Raise exceptions here.
Do NOT use `assert` in this file (assertions can be switched off with `python -O`).
See README Task 5 for the exact rules.
"""
import math
from .exceptions import InvalidValueError, MissingFieldError

REQUIRED_FIELDS = ("id", "title", "status", "duration")
VALID_STATUSES = ("pass", "fail", "blocked")


def validate_record(row, raw):
    """Turn one raw record into a clean dict, or raise a RecordValidationError.

    row : 1-based record number in the file (used in error messages)
    raw : whatever the reader produced for that record (usually a dict)

    Returns {"id": str, "title": str, "status": str, "duration": float}.
    """
    # raise NotImplementedError("Task 5: write validate_record")
    if not isinstance(raw, dict):
        raise InvalidValueError(row, "record", raw, "an object with the test fields")
    
    for name in REQUIRED_FIELDS:
        value = raw.get(name)
        if value is None or str(value).strip() == "":
            raise MissingFieldError(row, name)
    
    id_raw = str(raw["id"]).strip()
    title = raw.get("title").strip()

    status = str(raw["status"]).strip().lower()
    if status not in VALID_STATUSES:
        raise InvalidValueError(row, "status", raw, "invalid status")

    duration = raw["duration"]

    if isinstance(duration, bool):
        raise InvalidValueError(row, "duration", raw, "duration is a bool")
    f_duration = 0.0

    try:
        f_duration = float(duration)

    except ValueError as error:
        raise InvalidValueError(row, "duration", raw, "invalid duration") from error

    except TypeError as error:
        raise InvalidValueError(row, "duration", raw, "invalid duration") from error

    if not math.isfinite(f_duration) or f_duration < 0:
        raise InvalidValueError(row, "duration", raw, "infinite or negative number")

    return {
        "id" : id_raw,
        "title" : title,
        "status" : status,
        "duration" : f_duration
    }

        

