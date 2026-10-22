"""qe_foundations/ingestion/loader.py  -  TASK 6 (about 30 min)

Ties everything together:
    file -> reader (format) -> validate_record (rules) -> IngestionReport

Error POLICY (the heart of the milestone):
    SourceError            -> the whole file is unusable -> let it propagate (raise)
    RecordValidationError  -> one record is bad          -> COLLECT it and carry on

Already done for you: the IngestionReport and BatchResult classes' constructors
and the READERS lookup table. You write the TODOs.
"""

import csv
from pathlib import Path

from .contexts import LoadSession
from .exceptions import (
    DuplicateIdError,
    RecordValidationError,
    SourceError,
    SourceNotFoundError,
    UnsupportedFormatError,
)
from .readers import read_csv_records, read_json_records, read_xml_records
from .validation import validate_record

# Which reader handles which file extension (always compare lower-case suffixes).
READERS = {
    ".csv": read_csv_records,
    ".json": read_json_records,
    ".xml": read_xml_records,
}


class IngestionReport:
    """Result of loading ONE file: the valid records AND every rejected one."""

    def __init__(self, source, rows_seen=0):
        self.source = source
        self.rows_seen = rows_seen
        self.valid = []       # clean dicts returned by validate_record
        self.rejected = []    # RecordValidationError instances

    def summary(self):
        """TODO (6A): one line, EXACTLY this shape:

            test_cases_messy.csv: 10 rows seen, 3 valid, 7 rejected
        """
        # raise NotImplementedError("Task 6A: write IngestionReport.summary")
        return f"{self.source}: {self.rows_seen} rows seen, {len(self.valid)} valid, {len(self.rejected)} rejected"


    def rejected_rows(self):
        """TODO (6A): the rejected records as plain dicts, ordered by row number.

        Each dict has exactly the keys: "source", "row", "field", "reason"
        ("reason" is the text of the exception, str(error)).
        """
        # raise NotImplementedError("Task 6A: write IngestionReport.rejected_rows")
        rejected_rows = []
        for r in self.rejected:
            rejected_rows.append({
                "source": self.source,
                "row": r.row,
                "field": r.field,
                "reason": str(r),
            })
        return sorted(rejected_rows, key=lambda x: x["row"])


    def check_invariants(self):
        """TODO (6B): use `assert` statements to check OUR OWN bookkeeping.

        Three invariants (README Task 6B). Each assert gets a helpful message.
        A failure here would be a BUG in this module, not bad input data.
        """
        # raise NotImplementedError("Task 6B: write IngestionReport.check_invariants")
        assert self.rows_seen == len(self.valid) + len(self.rejected), "Rows seen does not match"
        
        valid_ids = []

        for v in self.valid:
            valid_ids.append(v["id"])

        assert len(valid_ids) == len(set(valid_ids))

        assert all(isinstance(error, RecordValidationError) for error in self.rejected)


class BatchResult:
    """Result of loading a whole folder."""

    def __init__(self):
        self.reports = []           # IngestionReport, one per file that could be read
        self.failed_sources = []    # SourceError instances, one per unusable file

    def totals(self):
        """TODO (6D): return a dict with exactly these keys:

            "files_ok", "files_failed", "valid", "rejected"
        """
        # raise NotImplementedError("Task 6D: write BatchResult.totals")
        total_valid = 0
        total_rejected = 0
        for r in self.reports:
            total_valid += len(r.valid)
            total_rejected += len(r.rejected)
        return({
            "files_ok": len(self.reports),
            "files_failed": len(self.failed_sources),
            "valid": total_valid,
            "rejected": total_rejected,
        })


def load_test_cases(path):
    """Load one CSV/JSON/XML file into an IngestionReport (TODO 6C).

    * Wrap the whole job in `with LoadSession(path):`
    * unknown extension -> raise UnsupportedFormatError
    * SourceError subclasses from the readers must propagate unchanged
    * rows are numbered from 1 (the header line of a CSV does not count)
    * bad records are COLLECTED in report.rejected, good ones go to report.valid
    * a repeated id -> DuplicateIdError for the LATER occurrence (the first one stays valid)
    * call report.check_invariants() before returning
    """
    # raise NotImplementedError("Task 6C: write load_test_cases")
    with LoadSession(path):
        path = Path(path)
        suffix = path.suffix.lower()
        reader = READERS.get(suffix)

        if reader is None:
            raise UnsupportedFormatError(path, suffix)

        raw_records = reader(path)

        seen_ids = set()
        report = IngestionReport(path.name, rows_seen=len(raw_records))

        for row, raw in enumerate(raw_records, start=1):
            try:
                clean_record = validate_record(row, raw)
                c_id = clean_record["id"]

                if(c_id in seen_ids):
                        raise DuplicateIdError(row, c_id)
                else:
                    seen_ids.add(c_id)
                    report.valid.append(clean_record)

            except RecordValidationError as error:
                report.rejected.append(error)

        report.check_invariants()
        return report




def load_directory(folder):
    """Load every file directly inside `folder` (TODO 6D).

    * sorted by file name; sub-folders are skipped
    * a bad FILE never stops the batch: collect its SourceError in failed_sources
    * a folder that does not exist (or is not a folder) -> raise SourceNotFoundError(folder)
    """
    folder = Path(folder)

    if not folder.is_dir():
        raise SourceNotFoundError(folder)

    batch = BatchResult()

    for p in sorted(folder.glob("*")):
        if not p.is_file():
            continue
        try:
            report = load_test_cases(p)
        except SourceError as error:
            batch.failed_sources.append(error)
        else:
            batch.reports.append(report)

    return batch
    # raise NotImplementedError("Task 6D: write load_directory")


def write_rejected_csv(report, out_path):
    """Write report.rejected_rows() to a CSV file (TODO 6E) and return the Path.

    Header exactly: source,row,field,reason     (use csv.DictWriter)
    Create the parent folder if needed. Open the file with newline="".
    """
    out = Path(out_path)

    out.parent.mkdir(parents=True, exist_ok=True)

    rows = report.rejected_rows()

    with out.open("w", encoding="utf-8", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=["source", "row", "field", "reason"])
        writer.writeheader()
        writer.writerows(rows)

    return out
