# ADR-002: Apply log1p only where it reduces absolute skewness

Date: 2026-08-12
Status: Accepted

## Context

The project's name promises modeling on a logarithmic scale, so the temptation was to log-transform every continuous column and declare the theme satisfied. The dataset has nine genuinely continuous columns: age at enrollment plus the curricular unit counts (enrolled, evaluations, approved) and grades for both semesters. `Exploratory Data Analysis.ipynb` compares the skewness of each column before and after a log1p transformation (log of one plus the value, defined at zero). Only age improves: its skew drops from 2.05 to 1.51. Log1p overcorrects the unit counts into strong negative skew and makes the already left-skewed grades worse.

## Decision

`Capstone File.ipynb` encodes the selection as a rule rather than a hand-picked list: for each continuous column, keep the log1p version only if the absolute skewness after transformation is smaller than before. The cell computes the before/after table, builds `log_cols` from the comparison, and prints which columns pass. On this dataset the rule selects exactly one column, `Age at enrollment`. Binary flags are never candidates (a log of a 0/1 indicator is meaningless), and the macroeconomic columns stay raw because GDP is a growth rate that takes negative values, where a log is undefined.

## Consequences

* The logarithmic framing is honest and auditable: a reviewer can rerun the skew cell and see that the transformation earns its place rather than decorating the project name.
* Given up: uniformity. The feature set mixes raw and log-scale columns, and the coefficient interpretation must note that the log1p age coefficient responds to proportional rather than absolute changes (the notebook's interpretation section does).
* The rule is data-dependent: on a different institution's extract, a different set of columns could pass. Any reimplementation (including `tests/test_acceptance.py`) must rebuild the rule from the data rather than hardcode "age only".
