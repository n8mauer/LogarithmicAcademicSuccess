"""One-command demo: reproduce the README results table from the pinned dataset.

Downloads the dataset (or reuses the cached copy under data/), rebuilds
the notebook's features and 70/30 split, fits the logistic regression
pipeline, and prints the measured metrics next to the majority baseline
and the numbers claimed in README.md. It then prints the ten test-set
students with the highest predicted dropout probability, the shape of
the intervention list an early warning system would produce.

Run with: python demo.py
"""

import sys
import time
from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.dummy import DummyClassifier
from sklearn.metrics import accuracy_score, f1_score, recall_score, roc_auc_score
from sklearn.model_selection import train_test_split

sys.path.insert(0, str(Path(__file__).resolve().parent / "tests"))
from test_acceptance import (  # noqa: E402
    DATA_COMMIT_SHA,
    RANDOM_STATE,
    build_features,
    build_logreg_pipeline,
    download_dataset,
)

# Point estimates from the README results table (saved notebook outputs).
CLAIMED = {"Accuracy": 0.930, "Dropout recall": 0.883, "Dropout F1": 0.908, "ROC-AUC": 0.967}


def main() -> int:
    start = time.time()

    print(f"Dataset pinned to n8mauer/SQL_projects @ {DATA_COMMIT_SHA[:12]}")
    csv_path = download_dataset()
    print(f"Using CSV at {csv_path}")

    X, y, numeric_features, log_cols = build_features(csv_path)
    print(f"{len(X)} students after excluding Enrolled "
          f"(dropout rate {y.mean():.1%}); log1p kept for: {', '.join(log_cols)}")

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.3, random_state=RANDOM_STATE, stratify=y
    )
    print(f"Split: {len(X_train)} train / {len(X_test)} test (stratified, "
          f"random_state={RANDOM_STATE})")

    baseline = DummyClassifier(strategy="most_frequent").fit(X_train, y_train)
    logreg = build_logreg_pipeline(numeric_features).fit(X_train, y_train)

    pred = logreg.predict(X_test)
    proba = logreg.predict_proba(X_test)[:, 1]
    measured = {
        "Accuracy": accuracy_score(y_test, pred),
        "Dropout recall": recall_score(y_test, pred),
        "Dropout F1": f1_score(y_test, pred),
        "ROC-AUC": roc_auc_score(y_test, proba),
    }
    base = {
        "Accuracy": baseline.score(X_test, y_test),
        "Dropout recall": 0.0,
        "Dropout F1": 0.0,
        "ROC-AUC": 0.5,
    }

    print()
    print(f"{'Metric':<16} {'Baseline':>9} {'LogReg (measured)':>18} {'README (claimed)':>17}")
    for metric in CLAIMED:
        print(f"{metric:<16} {base[metric]:>9.3f} {measured[metric]:>18.3f} "
              f"{CLAIMED[metric]:>17.3f}")

    print()
    print("Intervention list: 10 highest-risk students in the test set")
    risk = pd.DataFrame(
        {
            "P(dropout)": proba,
            "Age": np.rint(np.expm1(X_test["log1p Age at enrollment"])).astype(int).to_numpy(),
            "Course": X_test["Course name"].to_numpy(),
            "Actual outcome": y_test.map({1: "Dropout", 0: "Graduate"}).to_numpy(),
        },
        index=X_test.index,
    )
    top = risk.sort_values("P(dropout)", ascending=False).head(10)
    print(f"{'Student row':>11} {'P(dropout)':>11} {'Age':>4} {'Actual':>9}  Course")
    for idx, row in top.iterrows():
        # The model is near-certain about the very top of the list, so a
        # plain 3-decimal format would round to a misleading 1.000.
        p = row["P(dropout)"]
        p_text = ">0.999" if p > 0.9995 else f"{p:.3f}"
        print(f"{idx:>11} {p_text:>11} {row['Age']:>4} "
              f"{row['Actual outcome']:>9}  {row['Course']}")

    print()
    print(f"Done in {time.time() - start:.1f}s")
    return 0


if __name__ == "__main__":
    sys.exit(main())
