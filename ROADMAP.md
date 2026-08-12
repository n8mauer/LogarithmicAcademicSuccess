# Roadmap

Last updated: 2026-08-12. Statuses: Done, In progress, Planned. Every Done item names its evidence in this repository.

## Milestones

| # | Milestone | Status | Evidence / notes |
| --- | --- | --- | --- |
| 1 | Exploratory data analysis: outcome distribution, graduation rates by gender and course, continuous distributions, skew check for log1p, correlation analysis restricted to meaningful columns | Done | `Exploratory Data Analysis.ipynb` (committed with outputs) |
| 2 | Binary dropout model: Enrolled excluded, skew-driven log1p selection, stratified 70/30 split, majority baseline, logistic regression, grid-searched decision tree, coefficient interpretation, application-mode robustness check | Done | `Capstone File.ipynb` (committed with outputs); results table in `README.md` |
| 3 | Project report with results and limitations | Done | `README.md` |
| 4 | Product documentation: PRD, architecture decision records, acceptance criteria, results provenance, changelog | Done | `docs/PRD.md`, `docs/decisions/ADR-001` through `ADR-003`, `docs/ACCEPTANCE.md`, `docs/RESULTS.md`, `CHANGELOG.md` (added 2026-08-12) |
| 5 | CI acceptance tests: pin the dataset to an immutable commit-SHA URL, rebuild the notebook pipeline, and enforce the metric gates in GitHub Actions | Done | Gates specified in `docs/ACCEPTANCE.md` and implemented in `tests/test_acceptance.py`; workflow in `.github/workflows/ci.yml`; locked dependencies in `requirements.lock` (all 2026-08-12) |
| 6 | Demo and screenshot assets for the README | Done | `demo.py` plus the README Demo section; figures in `docs/images/` extracted from the committed notebook outputs by `scripts/extract_figures.py` (all 2026-08-12) |
| 7 | Enrollment-time model: drop semester performance and financial flags, add application mode back, measure day-one predictive power | Planned | Listed under Next Steps in `README.md`; motivated in `docs/decisions/ADR-003-one-hot-course-exclude-nominal-codes.md` |
| 8 | Watch list: score the students recorded as Enrolled and produce a ranked early-warning list | Planned | Listed under Next Steps in `README.md`; the natural product for the primary persona in `docs/PRD.md` |
| 9 | External validation on data from other institutions before treating coefficients as general | Planned | Listed under Next Steps in `README.md` |

## Ordering rationale

Milestones 5 and 6 protect what already exists: with the acceptance gates running in CI, the README results table stops being a static claim and becomes a continuously verified one. Milestones 7 and 8 are the two halves of the actual product for the primary persona (predict earlier, then hand staff a ranked list), and milestone 9 is the prerequisite for using either beyond the original institution.
