# ADR-001: Exclude Enrolled students and reframe the three-class label as binary

Date: 2026-08-12
Status: Accepted

## Context

The dataset's target column takes three values: Dropout, Enrolled, and Graduate. `Exploratory Data Analysis.ipynb` measures the split at 49.9 percent Graduate, 32.1 percent Dropout, and 17.9 percent Enrolled. Students recorded as Enrolled were still studying when the data was collected, so their final outcome is unknown: some will graduate, some will drop out. Treating Enrolled as a third class would train the model to predict an administrative snapshot rather than an outcome.

## Decision

`Capstone File.ipynb` filters out every row where the outcome is Enrolled and defines a binary target: Dropout mapped to 1, Graduate mapped to 0. This leaves 3,630 students (2,209 Graduate, 1,421 Dropout) with a 39.1 percent dropout rate, and every downstream metric (accuracy, dropout recall, dropout F1, ROC-AUC) is computed on that binary problem.

## Consequences

* The label is clean: every training example has a known final outcome, and standard binary metrics apply directly.
* The 0.609 majority baseline and all reported results are defined against this filtered population, and the acceptance gates in `docs/ACCEPTANCE.md` reproduce the same filter before checking any metric.
* Given up: 794 of the 4,424 students (18 percent of the data) are discarded from training and evaluation.
* Given up: the model's performance on currently enrolled students is unmeasured. Ironically, those students are the natural scoring target for an early-warning watch list; scoring them is listed as a planned follow-up in the README and `ROADMAP.md`, not a delivered feature.
* If the Enrolled population differs systematically from students with known outcomes, the model may be miscalibrated for exactly the group an institution wants to score. External validation is future work.
