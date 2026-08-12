# Results provenance

Date: 2026-08-12

This project is the capstone for the UC Berkeley Professional Certificate in Machine Learning and Artificial Intelligence. Every claim in this repository falls into exactly one of the three tiers below.

## Verified in this repository

The results table in `README.md` is Tier 1: recomputable by anyone from public artifacts.

| Model | Accuracy | Dropout recall | Dropout F1 | ROC-AUC |
| --- | --- | --- | --- | --- |
| Baseline (majority class) | 0.609 | 0.000 | 0.000 | 0.500 |
| Logistic regression | 0.930 | 0.883 | 0.908 | 0.967 |
| Decision tree (tuned) | 0.899 | 0.845 | 0.867 | 0.939 |

Evidence chain:

* The numbers appear in the saved outputs of `Capstone File.ipynb`, committed in this repository.
* The dataset is public. The notebooks load it from the n8mauer/SQL_projects repository, and `tests/test_acceptance.py` pins that CSV to an immutable commit-SHA URL so the verification target cannot drift.
* `tests/test_acceptance.py` rebuilds the notebook's target definition, features, and split (`random_state=42`), refits the logistic regression pipeline, and asserts accuracy >= 0.92, ROC-AUC >= 0.96, dropout recall >= 0.86, and a majority baseline of 0.609 within 0.01, in CI on every push. Thresholds sit below the point estimates above to absorb library-version variance; see `docs/ACCEPTANCE.md` for the exact gates.
* The supporting cross-validation figure (five-fold CV ROC-AUC of 0.948 plus or minus 0.014) and the application-mode robustness check (CV AUC 0.948 with or without it) are likewise visible in the committed notebook outputs and rerunnable from the pinned data.

## Self-reported operational results

None. This model has not been deployed at any institution, and no operational outcomes (interventions triggered, students retained, staff hours saved) are claimed.

## Resume-only and proprietary outcomes

None claimed for this project. Everything asserted about it is either verifiable from this repository (Tier 1) or not asserted at all.
