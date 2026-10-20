# QE Foundations

## Project 1 milestone - Week 2, Monday
### What Exists Now
Organized utility functions into the utils subpackag in qe_foundations. Separated functions into modules for string, number, dates, and
data generation. Added runtime dependencies in requirements.txt and development dependencies in requirements-dev.txt.

### What is coming Tuesday - Friday
Tuesday: Create subpackage ingestion in qe_foundations
Wednesday: Will add logging and unit tests in tests/
Thursday: Will add sql/ validation queries
Friday: Will join validation + integration

## Setup
1. python -m venv .venv
2. .venv\Scripts\Activate.ps1
3. python -m pip install -r requirements.txt
4. python smoke_utils.py

Running this should print something similar to this:
requests version: 2.34.2
PASS  slugify
PASS  is_valid_email
PASS  mask_email
PASS  clamp
PASS  add_days
PASS  days_between
PASS  make_users is repeatable
7/7 checks passed