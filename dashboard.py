import streamlit as st
import json
import pandas as pd
import matplotlib.pyplot as plt
from streamlit_autorefresh import st_autorefresh

# -----------------------------
# PAGE CONFIG
# -----------------------------

st.set_page_config(
    page_title="AI Secure Pipeline",
    layout="wide"
)

# -----------------------------
# AUTO REFRESH
# -----------------------------

st_autorefresh(interval=5000, key="refresh")

# -----------------------------
# CUSTOM CSS (JENKINS STYLE)
# -----------------------------

st.markdown("""
<style>

body {
    background-color: #f4f7fc;
}

.main {
    background-color: #f4f7fc;
}

.big-title {
    font-size: 40px;
    font-weight: bold;
    color: #1f2937;
}

.card {
    background-color: white;
    padding: 20px;
    border-radius: 12px;
    box-shadow: 0px 2px 8px rgba(0,0,0,0.1);
    margin-bottom: 20px;
}

.success {
    color: green;
    font-weight: bold;
    font-size: 24px;
}

.fail {
    color: red;
    font-weight: bold;
    font-size: 24px;
}

.issue-box {
    background-color: #fff5f5;
    border-left: 6px solid red;
    padding: 15px;
    border-radius: 10px;
    margin-bottom: 15px;
}

.ai-box {
    background-color: #f3f4f6;
    padding: 10px;
    border-radius: 8px;
    margin-top: 10px;
}

</style>
""", unsafe_allow_html=True)

# -----------------------------
# TITLE
# -----------------------------

st.markdown(
    "<div class='big-title'>🔐 AI Automated Security Dashboard</div>",
    unsafe_allow_html=True
)

st.write("Live CI/CD Vulnerability Monitoring Dashboard")
st.success("AI Model Enabled: Dynamic Vulnerability Classification")
st.info("Model: TF-IDF + Naive Bayes")
# -----------------------------
# LOAD REPORT
# -----------------------------

try:
    st.cache_data.clear()

    with open("reports/final-report.json") as f:
        data = json.load(f)

except:
    st.error("ai-report.json not found")
    st.stop()

# -----------------------------
# METRICS
# -----------------------------

total = len(data["issues"])

high = 0
medium = 0
low = 0

for issue in data["issues"]:

    severity = issue["severity"].lower()

    if severity == "high":
        high += 1

    elif severity == "medium":
        medium += 1

    else:
        low += 1


# -----------------------------
# PIPELINE STATUS
# -----------------------------

st.markdown("## 🚦 Pipeline Decision")

decision = data["final_decision"]

if decision == "FAIL":
    st.markdown(
        "<div class='fail'>❌ BUILD FAILED</div>",
        unsafe_allow_html=True
    )
else:
    st.markdown(
        "<div class='success'>✅ BUILD PASSED</div>",
        unsafe_allow_html=True
    )

# -----------------------------
# ISSUES
# -----------------------------

if decision == "FAIL":

    st.markdown("## 🔍 Detected Vulnerabilities")

    for issue in data["issues"]:

        st.markdown(f"""
        <div class='issue-box'>

        <h4>{issue['issue_text']}</h4>

        <b>Severity:</b> {issue['severity']}

        <div class='ai-box'>
        🤖 <b>AI Analysis:</b><br>
        {issue['ai_analysis']}
        </div>

        </div>
        """, unsafe_allow_html=True)

else:

    st.success("✅ No vulnerabilities detected. Secure build passed.")
# -----------------------------
# TOP CARDS
# -----------------------------

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("Total Issues", total)

with col2:
    st.metric("High Risk", high)

with col3:
    st.metric("Medium Risk", medium)

with col4:
    st.metric("Low Risk", low)

# -----------------------------
# CHARTS
# -----------------------------

col1, col2 = st.columns(2)

# PIE CHART

with col1:

    st.markdown("# Vulnerability Distribution")

    labels = ['High', 'Medium', 'Low']
    values = [high, medium, low]

    fig1, ax1 = plt.subplots()

    ax1.pie(
        values,
        labels=labels,
        autopct='%1.1f%%'
    )

    st.pyplot(fig1)

# BAR GRAPH

with col2:

    st.markdown("### Severity Analysis")

    fig2, ax2 = plt.subplots()

    ax2.bar(labels, values)

    st.pyplot(fig2)
