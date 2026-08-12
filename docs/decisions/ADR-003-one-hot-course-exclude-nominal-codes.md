# ADR-003: One-hot encode course by codebook name, exclude the other nominal code columns

Date: 2026-08-12
Status: Accepted

## Context

Several columns in the dataset are nominal categories stored as arbitrary integer codes: course, application mode, marital status, nationality, previous qualification, and the parental qualification and occupation columns. Feeding these codes to a linear model as numbers would invent an ordering that does not exist; the EDA notebook excludes them from its correlation matrix for the same reason. One-hot encoding all of them would balloon the feature count and blur the coefficient story, while some of them plausibly carry real signal.

## Decision

`Capstone File.ipynb` one-hot encodes exactly one nominal column, `Course`, after mapping its 17 integer codes to human-readable program names from the dataset codebook (`course_names` in the notebook). The remaining nominal code columns are excluded to keep the feature set compact. The exclusion is stress-tested by a robustness check: the notebook adds application mode, the strongest of the excluded columns, back as a second one-hot block and reruns five-fold cross-validation. The cross-validated ROC-AUC stays at 0.948 with or without it, so the compact feature set leaves nothing measurable on the table for this model.

## Consequences

* Course coefficients are directly readable as program names in the interpretation plot (for example, Informatics Engineering at 1.46 leans toward dropout, Social Service at -1.23 leans toward graduation), which is the payoff the primary persona needs.
* Given up: any signal in the other excluded nominal columns is unused. The robustness check covers only application mode, the strongest candidate, not every excluded column.
* Given up: the conclusion is conditional on semester performance being in the model. The notebook itself notes that an enrollment-time model without the semester columns would likely need application mode back; that follow-up is tracked in `ROADMAP.md`.
* The encoder uses `handle_unknown='ignore'`, so a new program code at scoring time maps to an all-zero course block rather than an error.
