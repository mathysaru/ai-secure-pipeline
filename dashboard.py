import streamlit as st
import json
import plotly.express as px
from streamlit_autorefresh import st_autorefresh
import os

st.set_page_config(page_title="AI Security Dashboard", layout="wide")

st.title("🔐 AI Automated Security Dashboard (Live)")

# 🔄 Auto-refresh every 5 sec
st_autorefresh(interval=5000, key="refresh")

# Load report
file_path = "bandit-report.json"

if not os.path.exists(file_path):
    st.error("bandit-report.json not found. Run Bandit first.")
    st.stop()

with open(file_path) as f:
    data = json.load(f)

results = data.get("results", [])

# Counters
critical, high, medium, low = 0, 0, 0, 0

def classify(issue):
    text = issue.lower()
    if "eval" in text or "shell" in text:
        return "CRITICAL"
    elif "hardcoded" in text:
        return "HIGH"
    elif "md5" in text:
        return "MEDIUM"
    else:
        return "LOW"

def suggestion(issue):
    text = issue.lower()
    if "eval" in text:
        return "Use ast.literal_eval()"
    elif "shell" in text:
        return "Avoid os.system()"
    elif "hardcoded" in text:
        return "Use env variables"
    elif "md5" in text:
        return "Use SHA-256"
    else:
        return "Manual review"

table_data = []

for issue in results:
    text = issue.get("issue_text", "")
    severity = classify(text)
    fix = suggestion(text)

    if severity == "CRITICAL":
        critical += 1
    elif severity == "HIGH":
        high += 1
    elif severity == "MEDIUM":
        medium += 1
    else:
        low += 1

    table_data.append({
        "Issue": text,
        "Severity": severity,
        "Fix": fix
    })

# Metrics
col1, col2, col3, col4 = st.columns(4)
col1.metric("CRITICAL", critical)
col2.metric("HIGH", high)
col3.metric("MEDIUM", medium)
col4.metric("LOW", low)

st.divider()

# Data for charts
labels = ["CRITICAL", "HIGH", "MEDIUM", "LOW"]
values = [critical, high, medium, low]

# Final Decision
if critical > 0 or high > 0:
    st.error("FINAL DECISION: FAIL")
else:
    st.success("FINAL DECISION: PASS")

# Animated Pie Chart
st.subheader("Vulnerability Distribution")

pie_fig = px.pie(
    names=labels,
    values=values,
    title="Severity Distribution",
    hole=0.3
)

st.plotly_chart(pie_fig, use_container_width=True)

# Animated Bar Chart
st.subheader("Severity Count")

bar_fig = px.bar(
    x=labels,
    y=values,
    title="Severity Count",
    text=values
)

bar_fig.update_traces(textposition='outside')

st.plotly_chart(bar_fig, use_container_width=True)

# Table
st.subheader("📋 Vulnerability Details")
st.dataframe(table_data, use_container_width=True)
