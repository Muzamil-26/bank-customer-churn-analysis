"""Reusable data loading / cleaning / feature helpers.

Used by the Jupyter notebooks and the Streamlit dashboard so the same
transformations are applied everywhere (no code duplication).
"""

from pathlib import Path

import pandas as pd

# Absolute path to the dataset — resolves relative to this file,
# so it works from notebooks, the app, and plain scripts.
# Points at the 2,000-row seeded demo sample (data_sample/); the full 10,000-row
# dataset used for the analysis lives in data/ (see README "Live demo data").
DATA_PATH = Path(__file__).resolve().parent.parent / "data_sample" / "churn_sample.csv"

# Friendly column names: the raw file uses human labels with spaces
# (e.g. "Num Of Products"). Rename once here for easier downstream code.
RENAME_MAP = {
    "Num Of Products": "NumOfProducts",
    "Has Credit Card": "HasCrCard",
    "Is Active Member": "IsActiveMember",
    "Estimated Salary": "EstimatedSalary",
}


def load_data(path: str | Path = DATA_PATH) -> pd.DataFrame:
    """Load the raw churn CSV exactly as shipped in data/."""
    return pd.read_csv(path)


def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    """Apply light, transparent cleaning.

    - Rename columns to snake-free camelCase without spaces.
    - Drop identifier / free-text columns (CustomerId, Surname) — they
      carry no signal for churn analysis and would leak into models.
    - The dataset ships with zero missing values; keep a fill-forward
      guard so the pipeline stays robust if the file is ever refreshed.
    """
    df = df.copy()
    df = df.rename(columns=RENAME_MAP)
    df = df.drop(columns=["CustomerId", "Surname"], errors="ignore")
    # Defensive: dataset currently has no nulls, but stay safe.
    for col in ["Age", "Tenure", "NumOfProducts", "HasCrCard", "IsActiveMember"]:
        if col in df.columns:
            df[col] = df[col].fillna(df[col].median())
    for col in ["CreditScore", "Balance", "EstimatedSalary"]:
        if col in df.columns:
            df[col] = df[col].fillna(df[col].median())
    return df


def add_features(df: pd.DataFrame) -> pd.DataFrame:
    """Add analysis-friendly derived columns (purely from existing data)."""
    df = df.copy()
    # Age bands used across EDA, SQL and the dashboard.
    df["AgeBand"] = pd.cut(
        df["Age"],
        bins=[0, 30, 40, 50, 60, 120],
        labels=["<30", "30-40", "40-50", "50-60", "60+"],
    ).astype(str)
    # Credit-score bands (FICO-style cut points).
    df["CreditBand"] = pd.cut(
        df["CreditScore"],
        bins=[0, 579, 669, 739, 850],
        labels=["Poor (<580)", "Fair (580-669)", "Good (670-739)", "Very Good (740+)"],
    ).astype(str)
    # Tenure buckets: new, established, loyal.
    df["TenureBand"] = pd.cut(
        df["Tenure"],
        bins=[-1, 2, 7, 10],
        labels=["New (0-2y)", "Established (3-7y)", "Loyal (8-10y)"],
    ).astype(str)
    # Flags useful for segmentation.
    df["ZeroBalance"] = (df["Balance"] == 0).astype(int)
    df["BalanceSalaryRatio"] = df["Balance"] / df["EstimatedSalary"].replace(0, pd.NA)
    df["BalanceSalaryRatio"] = df["BalanceSalaryRatio"].fillna(0)
    return df


def get_model_data(df: pd.DataFrame):
    """Return (X, y, feature_names) ready for scikit-learn.

    One-hot encodes Geography/Gender, keeps AgeBand/derived columns out of
    the model (they are functions of Age, which is already included).
    """
    df = df.copy()
    feature_cols = [
        "CreditScore", "Age", "Tenure", "Balance", "NumOfProducts",
        "HasCrCard", "IsActiveMember", "EstimatedSalary", "ZeroBalance",
    ]
    X = pd.get_dummies(
        df[feature_cols + ["Geography", "Gender"]],
        columns=["Geography", "Gender"],
        drop_first=True,
    )
    y = df["Churn"].astype(int)
    return X, y, list(X.columns)
