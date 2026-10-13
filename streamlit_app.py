"""Bank Customer Churn — interactive analytics dashboard.

Run locally:  streamlit run streamlit_app.py
Deployed on Streamlit Community Cloud (free tier).
"""

from pathlib import Path

import pandas as pd
import plotly.express as px
import streamlit as st

from src import load_data, clean_data, add_features, get_model_data

st.set_page_config(page_title="Bank Customer Churn Analytics", layout="wide")

# ---------------------------------------------------------------- data
@st.cache_data
def get_data() -> pd.DataFrame:
    return add_features(clean_data(load_data()))


@st.cache_resource
def get_model():
    """Load the saved Random Forest, or train one on the fly as fallback."""
    import pickle

    model_path = Path(__file__).parent / "models" / "random_forest.pkl"
    if model_path.exists():
        with open(model_path, "rb") as f:
            saved = pickle.load(f)
        return saved["model"], saved["features"]
    # Fallback: train quickly (10k rows, a few seconds) so the app never breaks.
    from sklearn.ensemble import RandomForestClassifier

    df = get_data()
    X, y, features = get_model_data(df)
    model = RandomForestClassifier(
        n_estimators=100, max_depth=12, random_state=42, n_jobs=-1,
        class_weight="balanced",
    )
    model.fit(X, y)
    return model, features


df = get_data()

# ---------------------------------------------------------------- header
st.title("🏦 Bank Customer Churn Analytics")
st.caption("10,000 customers · France / Germany / Spain · interactive EDA + churn-risk scoring")

# ---------------------------------------------------------------- sidebar filters
st.sidebar.header("Filters")
geo = st.sidebar.multiselect("Geography", sorted(df["Geography"].unique()),
                             default=sorted(df["Geography"].unique()))
gender = st.sidebar.multiselect("Gender", sorted(df["Gender"].unique()),
                                default=sorted(df["Gender"].unique()))
age_min, age_max = int(df["Age"].min()), int(df["Age"].max())
age_range = st.sidebar.slider("Age range", age_min, age_max, (age_min, age_max))
active_only = st.sidebar.checkbox("Active members only", value=False)

fdf = df[
    df["Geography"].isin(geo)
    & df["Gender"].isin(gender)
    & df["Age"].between(age_range[0], age_range[1])
]
if active_only:
    fdf = fdf[fdf["IsActiveMember"] == 1]

if fdf.empty:
    st.warning("No customers match the current filters — widen them in the sidebar.")
    st.stop()

# ---------------------------------------------------------------- KPI cards
churn_rate = fdf["Churn"].mean() * 100
col1, col2, col3, col4 = st.columns(4)
col1.metric("Customers", f"{len(fdf):,}")
col2.metric("Churn rate", f"{churn_rate:.2f}%")
col3.metric("Churned", f"{int(fdf['Churn'].sum()):,}")
col4.metric(
    "Avg balance of churned",
    f"€{fdf.loc[fdf['Churn'] == 1, 'Balance'].mean():,.0f}"
    if fdf["Churn"].sum() else "—",
)

# ---------------------------------------------------------------- charts row 1
c1, c2 = st.columns(2)
with c1:
    g = fdf.groupby("Geography", observed=True)["Churn"].mean().mul(100).round(2).reset_index()
    fig = px.bar(g, x="Geography", y="Churn", text="Churn", title="Churn rate by country",
                 labels={"Churn": "Churn rate (%)"})
    fig.update_traces(texttemplate="%{text:.1f}%", textposition="outside")
    st.plotly_chart(fig, use_container_width=True)
with c2:
    g = fdf.groupby("AgeBand", observed=True)["Churn"].mean().mul(100).round(2).reset_index()
    order = ["<30", "30-40", "40-50", "50-60", "60+"]
    g["AgeBand"] = pd.Categorical(g["AgeBand"], categories=order, ordered=True)
    g = g.sort_values("AgeBand")
    fig = px.bar(g, x="AgeBand", y="Churn", text="Churn", title="Churn rate by age band",
                 labels={"AgeBand": "", "Churn": "Churn rate (%)"})
    fig.update_traces(texttemplate="%{text:.1f}%", textposition="outside")
    st.plotly_chart(fig, use_container_width=True)

# ---------------------------------------------------------------- charts row 2
c3, c4 = st.columns(2)
with c3:
    g = (fdf.groupby("NumOfProducts", observed=True)["Churn"]
         .mean().mul(100).round(2).reset_index())
    fig = px.bar(g, x="NumOfProducts", y="Churn", text="Churn",
                 title="Churn rate by products held (2 = loyalty sweet spot)",
                 labels={"NumOfProducts": "Products held", "Churn": "Churn rate (%)"})
    fig.update_traces(texttemplate="%{text:.1f}%", textposition="outside")
    st.plotly_chart(fig, use_container_width=True)
with c4:
    fig = px.histogram(
        fdf, x="Balance", color=fdf["Churn"].map({0: "Retained", 1: "Exited"}),
        nbins=40, barmode="overlay", opacity=0.6,
        title="Balance distribution: exited vs retained", labels={"color": "Outcome"})
    st.plotly_chart(fig, use_container_width=True)

# ---------------------------------------------------------------- model: feature importance
st.subheader("🤖 What drives churn? (Random Forest)")
model, features = get_model()
imp = (pd.DataFrame({"feature": features, "importance": model.feature_importances_})
       .sort_values("importance", ascending=False).head(10))
fig = px.bar(imp, x="importance", y="feature", orientation="h",
             title="Top churn drivers", labels={"feature": ""})
fig.update_layout(yaxis={"categoryorder": "total ascending"})
st.plotly_chart(fig, use_container_width=True)

# ---------------------------------------------------------------- at-risk explorer
st.subheader("🚨 At-risk customer explorer")
st.caption("Customers ranked by the model's predicted churn probability. "
           "Call the top of this list first.")

X_all, _, _ = get_model_data(df)
proba = model.predict_proba(X_all)[:, 1]
scored = df[["Age", "Geography", "Gender", "Balance", "NumOfProducts",
             "IsActiveMember", "CreditScore", "Tenure"]].copy()
scored["ChurnProbability"] = (proba * 100).round(1)
scored["Status"] = df["Churn"].map({0: "Retained", 1: "Exited"})
scored = scored.sort_values("ChurnProbability", ascending=False)

threshold = st.slider("Minimum churn probability (%)", 0, 100, 50)
risky = scored[scored["ChurnProbability"] >= threshold]
st.write(f"**{len(risky):,} customers** at or above {threshold}% churn probability")
st.dataframe(risky.head(200), use_container_width=True)

st.divider()
st.caption("Data: public Kaggle Bank Customer Churn dataset · "
           "Built with Python, pandas, scikit-learn, Plotly & Streamlit")
