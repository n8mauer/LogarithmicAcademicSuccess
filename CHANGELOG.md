# Changelog

All notable changes to this project are documented in this file.

The format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/), and the project uses [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2026-08-12

First versioned release. The repository history before this release consists of a single initial commit containing the analysis itself; this release adds the product documentation, acceptance gates, and CI scaffolding around it.

### Added

* `Exploratory Data Analysis.ipynb`: outcome distribution, graduation rates by gender and course, continuous variable distributions, the before/after skewness table that motivates the selective log1p decision, and a correlation analysis restricted to columns where Pearson correlation is meaningful (part of the initial commit).
* `Capstone File.ipynb`: binary Dropout-versus-Graduate model (Enrolled students excluded, 3,630 students, 39.1 percent dropout), skew-driven log1p selection (age at enrollment only), stratified 70/30 split with `random_state=42`, majority baseline, logistic regression pipeline (0.930 accuracy, 0.883 dropout recall, 0.967 ROC-AUC on the test set), grid-searched decision tree (0.899 accuracy, 0.939 ROC-AUC), coefficient interpretation, and an application-mode robustness check (part of the initial commit).
* `README.md` project report with executive summary, methodology, results table, and limitations; `LICENSE`; `requirements.txt` (part of the initial commit).
* Product documentation set (2026-08-12): `docs/PRD.md`, `docs/decisions/ADR-001-exclude-enrolled-students.md`, `docs/decisions/ADR-002-selective-log1p-transformation.md`, `docs/decisions/ADR-003-one-hot-course-exclude-nominal-codes.md`, `docs/ACCEPTANCE.md`, `docs/RESULTS.md`, `ROADMAP.md`, and this changelog.
* CI acceptance tests and demo assets (2026-08-12): `tests/test_acceptance.py` pinning the public dataset to an immutable commit-SHA URL and enforcing the metric gates from `docs/ACCEPTANCE.md`; `.github/workflows/ci.yml` running those gates and the demo on every push and pull request; `requirements.lock` with the exact dependency pins CI installs; `demo.py` reproducing the results table and printing the top-10 intervention list; `scripts/extract_figures.py` and the two README figures it extracts from the committed notebook outputs into `docs/images/`; `.gitignore` covering the virtual environment, caches, and the downloaded dataset.

### Changed

* `README.md` (2026-08-12): added a Product documentation section and a results provenance pointer to `docs/RESULTS.md`.
