# Product Requirements: Predicting Undergraduate Academic Success

Date: 2026-08-12

## Persona

**Primary: student-success or institutional-research officer.** Works at a university, owns retention numbers, and needs an early-warning list of students likely to drop out so advising and financial-aid staff can intervene before a student leaves. Comfortable reading a metrics table and a coefficient chart; does not write scikit-learn pipelines from scratch but can run a notebook and swap a data URL.

**Secondary: ML reviewer.** Checks that the project's "logarithmic" framing is applied honestly: that log transformations are kept only where they measurably help, rather than applied decoratively to justify the name.

## User Workflow

1. Install dependencies with `pip install -r requirements.txt` (pandas, numpy, scikit-learn, matplotlib, seaborn, notebook).
2. Open `Exploratory Data Analysis.ipynb` and run all cells. The CSV loads over the network from the public copy in the n8mauer/SQL_projects repository (the notebooks read the main branch; the acceptance tests pin a specific commit), so no download step is needed. Review the outcome distribution (49.9 percent Graduate, 32.1 percent Dropout, 17.9 percent Enrolled), the graduation rates by gender and course, and the skewness table that motivates the log decision.
3. Open `Capstone File.ipynb` and run all cells to reproduce the full modeling pipeline: target definition (Enrolled excluded, 3,630 students, 39.1 percent dropout), skew-driven log1p selection, stratified 70/30 split with `random_state=42`, majority baseline, logistic regression, and a grid-searched decision tree.
4. Read the model comparison table and confusion matrices. Dropout recall is the metric that matters most for this persona: a missed at-risk student costs more than a false alarm.
5. Read the coefficient interpretation to separate risk markers from intervention levers. The notebook explicitly flags tuition status and the debtor flag as timing-ambiguous: students who leave stop paying, so those flags should not be read as causes.
6. To apply the model to their own institution, replace `DATA_URL` in either notebook with an extract that matches the dataset schema and rerun. No code changes are needed if the column names match.
7. (Planned, not yet implemented) Score the students recorded as Enrolled to produce a ranked watch list. This is listed under Next Steps in the README and in `ROADMAP.md`; the current notebooks stop at model evaluation.

## Problem

Undergraduate attrition is expensive for students and institutions. Retention staff typically learn a student is at risk only after the student has already disengaged. This project tests whether enrollment records and first-year academic performance are enough to predict, with usable recall, which students will drop out rather than graduate, using the public "Predict Students' Dropout and Academic Success" dataset of 4,424 students at a Portuguese higher-education institution.

## Success Metrics

All four metrics are measured on the 30 percent held-out test set produced by the notebook's stratified split (`random_state=42`) and are enforced as acceptance gates by `tests/test_acceptance.py` (see `docs/ACCEPTANCE.md`). Thresholds sit deliberately below the point estimates reported in the README (0.930 accuracy, 0.967 ROC-AUC, 0.883 dropout recall) to absorb minor library-version variance without letting a real regression pass.

| Metric | Threshold | README point estimate |
| --- | --- | --- |
| Test accuracy | >= 0.92 | 0.930 |
| Test ROC-AUC | >= 0.96 | 0.967 |
| Dropout recall | >= 0.86 | 0.883 |
| Majority baseline accuracy | 0.609 within 0.01 | 0.609 |

A run that fails any gate means the published results are no longer reproducible from the pinned dataset and must not be shipped.

## Non-goals

* **No causal claims.** Coefficients are associations. The notebook itself warns that the financial flags are recorded during the year, not at enrollment.
* **No production scoring service.** Deliverables are notebooks and documentation, not an API or a dashboard.
* **No enrollment-time (day-one) model.** The current model uses first-year semester performance. A model restricted to enrollment-time features is a planned follow-up, not part of this release.
* **No generalization claims beyond one institution.** The data covers a single Portuguese institution; external validation is future work.
* **No committed dataset copy.** The notebooks load the CSV from the sibling n8mauer/SQL_projects repository; this repository stays data-free.
* **No fairness audit.** The EDA breaks graduation rates down by gender and course, but no formal fairness analysis is claimed.
