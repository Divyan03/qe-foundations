# Ingestion module - design notes (Week 2, Day 2)

Answer in your own words, 2-4 sentences each. Replace every line that starts with

## 1. Exceptions or assertions?
In `validate_record` I raise exceptions for a negative duration, but in
`IngestionReport.check_invariants` I use `assert`. Why is each the right tool there?

I raise exceptions for negative duration because bad input is expected and needs to be handled.
For check_invariants(), I use assert because the check is to determine if there is a bug in the program's code.

## 2. Stop or collect?
Why is a malformed JSON file a `SourceError` that stops loading, while a record with
a bad status is a `RecordValidationError` that is collected? Who benefits from this split?

A malformed JSON file is a SourceError because it cannot be read or interpeted consistently, so loading the file must be terminated. A record with a bad status is a RecordValidationError because the file is still readable, and other records can still be read. This split benefits those who want to identify invalid records while still keeping the valid ones.

## 3. What did the context managers buy you?
Name two things that `open_source` / `LoadSession` do for the caller that you would otherwise
have to remember to do at every call site.

open_source() ensures that files are closed after being read. LoadSession tracks how long a load takes.

## 4. Your hardest bad-input case
Which sample file or record took you longest to handle, and what was the cause?

The case that took me the longest to validate was durations. This is due to the way float numbers behave. I would have to consider values such as NaN, inf, booleans, and negative values. NaN and infinity being considered as float made things a bit trickier.