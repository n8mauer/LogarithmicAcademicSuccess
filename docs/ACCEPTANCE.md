# Acceptance Criteria

Date: 2026-08-12

These gates define what "the published results are reproducible" means for this repository. They are implemented as pytest tests in `tests/test_acceptance.py` and run in CI on ubuntu-latest with Python 3.11. Every gate also runs locally with `python -m pytest tests/test_acceptance.py`; there are no local-only gates. The first run needs network access to download the dataset, after which the cached copy is used.

Thresholds sit deliberately below the point estimates reported in `README.md` (0.930 accuracy, 0.967 ROC-AUC, 0.883 dropout recall) so that minor library-version variance passes while a real regression fails.

## Gate 1: Pinned, immutable data source

**Statement:** The test downloads `dataset.csv` from the same source the notebooks use (`student_data_analysis/Datasets/dataset.csv` in n8mauer/SQL_projects), but pinned to an immutable `raw.githubusercontent.com` URL that names a specific commit SHA rather than the `main` branch, so upstream edits cannot silently change what this repository verifies. The download is cached inside this repository's directory and the cache path is gitignored.

**Enforced by:** `tests/test_acceptance.py` (module-level constants `DATA_COMMIT_SHA` and `DATA_URL`, plus a cached download fixture). As of 2026-08-12, `git ls-remote` resolves `main` of n8mauer/SQL_projects to commit `f0096ac316feb799ec4f76fb039aee3989117a8a`, and the test constants record exactly that SHA. If the upstream file ever moves, re-resolve the SHA and update the constant.

## Gate 2: Reproduced target, features, and split

**Statement:** The test rebuilds the notebook's exact setup: rows with outcome Enrolled are excluded (leaving 3,630 students at a 39.1 percent dropout rate), the target is Dropout=1 versus Graduate=0, log1p is applied only to continuous columns whose absolute skewness it reduces (rebuilt from the data, per ADR-002, not hardcoded), Course is one-hot encoded by codebook name, and the data is split 70/30 stratified with `random_state=42`, matching `Capstone File.ipynb`.

**Enforced by:** `tests/test_acceptance.py` (setup shared by all metric assertions; asserted row count and split sizes of 2,541 train / 1,089 test).

## Gate 3: Majority baseline

**Statement:** A most-frequent-class baseline on the same split scores an accuracy of 0.609 on the test set, within 0.01. This anchors the class balance: if the baseline moves, the data or the split changed.

**Enforced by:** `tests/test_acceptance.py::test_majority_baseline`

## Gate 4: Test accuracy

**Statement:** The logistic regression pipeline (StandardScaler on numeric features, OneHotEncoder on course, `LogisticRegression(max_iter=1000, random_state=42)`), fit on the training split, reaches accuracy >= 0.92 on the held-out test set.

**Enforced by:** `tests/test_acceptance.py::test_accuracy`

## Gate 5: Test ROC-AUC

**Statement:** The same fitted pipeline reaches ROC-AUC >= 0.96 on the held-out test set, scored on predicted dropout probabilities.

**Enforced by:** `tests/test_acceptance.py::test_roc_auc`

## Gate 6: Dropout recall

**Statement:** The same fitted pipeline reaches recall >= 0.86 on the Dropout class of the held-out test set. This is the gate the primary persona cares about most: it bounds how many truly at-risk students the model misses.

**Enforced by:** `tests/test_acceptance.py::test_dropout_recall`

## CI integration

A GitHub Actions workflow runs all gates on every push and pull request (ubuntu-latest, Python 3.11). A red run means the README results table can no longer be reproduced from the pinned dataset and must not be merged over.
