"""Acceptance gates for the published results (see docs/ACCEPTANCE.md).

These tests rebuild the exact setup of ``Capstone File.ipynb`` from the
pinned public dataset and assert that the README results table is still
reproducible. Thresholds sit deliberately below the reported point
estimates (0.930 accuracy, 0.967 ROC-AUC, 0.883 dropout recall) so that
minor library-version variance passes while a real regression fails.

Run locally with: python -m pytest tests/test_acceptance.py
"""

import urllib.request
from pathlib import Path

import numpy as np
import pandas as pd
import pytest
from sklearn.compose import ColumnTransformer
from sklearn.dummy import DummyClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, recall_score, roc_auc_score
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler

# Gate 1: pinned, immutable data source. The notebooks load this CSV from
# the main branch of n8mauer/SQL_projects; the tests pin it to a specific
# commit SHA so upstream edits cannot silently change what CI verifies.
# SHA resolved 2026-08-12 via: git ls-remote https://github.com/n8mauer/SQL_projects.git main
DATA_COMMIT_SHA = "f0096ac316feb799ec4f76fb039aee3989117a8a"
DATA_URL = (
    "https://raw.githubusercontent.com/n8mauer/SQL_projects/"
    f"{DATA_COMMIT_SHA}/student_data_analysis/Datasets/dataset.csv"
)

REPO_ROOT = Path(__file__).resolve().parent.parent
CACHE_PATH = REPO_ROOT / "data" / "dataset.csv"  # gitignored

RANDOM_STATE = 42

# Course code to name mapping from the dataset codebook (Capstone File.ipynb).
COURSE_NAMES = {
    1: "Biofuel Production Technologies",
    2: "Animation and Multimedia Design",
    3: "Social Service (evening)",
    4: "Agronomy",
    5: "Communication Design",
    6: "Veterinary Nursing",
    7: "Informatics Engineering",
    8: "Equinculture",
    9: "Management",
    10: "Social Service",
    11: "Tourism",
    12: "Nursing",
    13: "Oral Hygiene",
    14: "Advertising and Marketing Management",
    15: "Journalism and Communication",
    16: "Basic Education",
    17: "Management (evening)",
}

BINARY_FEATURES = [
    "Gender",
    "Debtor",
    "Tuition fees up to date",
    "Scholarship holder",
    "Displaced",
    "Daytime/Evening Program",
    "International",
]
MACRO_FEATURES = ["Unemployment rate", "Inflation rate", "GDP"]
CONTINUOUS_COLS = [
    "Age at enrollment",
    "Curricular units 1st sem (enrolled)",
    "Curricular units 1st sem (evaluations)",
    "Curricular units 1st sem (approved)",
    "Curricular units 1st sem (grade)",
    "Curricular units 2nd sem (enrolled)",
    "Curricular units 2nd sem (evaluations)",
    "Curricular units 2nd sem (approved)",
    "Curricular units 2nd sem (grade)",
]


def download_dataset(cache_path: Path = CACHE_PATH, url: str = DATA_URL) -> Path:
    """Download the pinned CSV once and reuse the cached copy afterward."""
    if not cache_path.exists():
        cache_path.parent.mkdir(parents=True, exist_ok=True)
        with urllib.request.urlopen(url, timeout=60) as response:
            cache_path.write_bytes(response.read())
    return cache_path


def build_features(csv_path: Path):
    """Rebuild the notebook's target, features, and transformations.

    Mirrors Capstone File.ipynb exactly: rename columns, exclude Enrolled
    students, apply log1p only where it reduces absolute skewness
    (rebuilt from the data per ADR-002, not hardcoded), and one-hot
    encode the course by codebook name.
    """
    student_data = pd.read_csv(csv_path)
    student_data = student_data.rename(
        columns={
            "Daytime/evening attendance": "Daytime/Evening Program",
            "Nacionality": "Nationality",
            "Target": "Outcome",
        }
    )

    model_data = student_data[student_data["Outcome"] != "Enrolled"].copy()
    model_data["Dropout"] = (model_data["Outcome"] == "Dropout").astype(int)

    skew_before = model_data[CONTINUOUS_COLS].skew()
    skew_after = np.log1p(model_data[CONTINUOUS_COLS]).skew()
    log_cols = [
        c for c in CONTINUOUS_COLS if abs(skew_after[c]) < abs(skew_before[c])
    ]

    for col in log_cols:
        model_data[f"log1p {col}"] = np.log1p(model_data[col])
    raw_continuous = [c for c in CONTINUOUS_COLS if c not in log_cols]
    model_data["Course name"] = model_data["Course"].map(COURSE_NAMES)

    numeric_features = (
        BINARY_FEATURES
        + MACRO_FEATURES
        + raw_continuous
        + [f"log1p {c}" for c in log_cols]
    )
    X = model_data[numeric_features + ["Course name"]]
    y = model_data["Dropout"]
    return X, y, numeric_features, log_cols


def build_logreg_pipeline(numeric_features):
    """The notebook's logistic regression pipeline, unchanged."""
    preprocess = ColumnTransformer(
        [
            ("num", StandardScaler(), numeric_features),
            ("course", OneHotEncoder(handle_unknown="ignore"), ["Course name"]),
        ]
    )
    return Pipeline(
        [
            ("prep", preprocess),
            ("clf", LogisticRegression(max_iter=1000, random_state=RANDOM_STATE)),
        ]
    )


@pytest.fixture(scope="session")
def fitted():
    """Shared setup: download, rebuild features, split, and fit once."""
    csv_path = download_dataset()
    X, y, numeric_features, log_cols = build_features(csv_path)

    # Gate 2: reproduced target, features, and split.
    assert len(X) == 3630, "Excluding Enrolled students must leave 3,630 rows"
    assert y.mean() == pytest.approx(0.391, abs=0.001), "Dropout rate must be 39.1 percent"
    assert log_cols == ["Age at enrollment"], (
        "log1p must be kept only for age at enrollment (the only column "
        "where it reduces absolute skewness)"
    )

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.3, random_state=RANDOM_STATE, stratify=y
    )
    assert len(X_train) == 2541 and len(X_test) == 1089

    logreg = build_logreg_pipeline(numeric_features)
    logreg.fit(X_train, y_train)
    baseline = DummyClassifier(strategy="most_frequent").fit(X_train, y_train)

    return {
        "logreg": logreg,
        "baseline": baseline,
        "X_train": X_train,
        "X_test": X_test,
        "y_train": y_train,
        "y_test": y_test,
    }


def test_majority_baseline(fitted):
    """Gate 3: most-frequent-class baseline scores 0.609 within 0.01."""
    baseline_acc = fitted["baseline"].score(fitted["X_test"], fitted["y_test"])
    assert baseline_acc == pytest.approx(0.609, abs=0.01)


def test_accuracy(fitted):
    """Gate 4: logistic regression test accuracy >= 0.92."""
    pred = fitted["logreg"].predict(fitted["X_test"])
    assert accuracy_score(fitted["y_test"], pred) >= 0.92


def test_roc_auc(fitted):
    """Gate 5: logistic regression test ROC-AUC >= 0.96."""
    proba = fitted["logreg"].predict_proba(fitted["X_test"])[:, 1]
    assert roc_auc_score(fitted["y_test"], proba) >= 0.96


def test_dropout_recall(fitted):
    """Gate 6: recall on the Dropout class >= 0.86."""
    pred = fitted["logreg"].predict(fitted["X_test"])
    assert recall_score(fitted["y_test"], pred) >= 0.86
