import json
import os
import joblib
import datetime
SEVERITY_SCORES = {
    "CRITICAL": 90,
    "HIGH": 70,
    "MEDIUM": 40,
    "LOW": 10
}
CVSS_MAPPING = {
    "CRITICAL": 9.5,
    "HIGH": 8.0,
    "MEDIUM": 5.5,
    "LOW": 2.0
}
# Load trained AI model
model = joblib.load("scanner/vulnerability_model.pkl")
def ai_classify(issue_text):
    prediction = model.predict([issue_text])[0]

    suggestions = {
        "CRITICAL": "Immediate fix required. Avoid dangerous execution patterns.",
        "HIGH": "Secure the code and validate inputs properly.",
        "MEDIUM": "Use stronger cryptographic or secure coding practices.",
        "LOW": "Review manually and improve coding standards."
    }

    return prediction, suggestions.get(prediction, "Review manually.") 
def classify_and_suggest(issue_text):
    text = issue_text.lower()

    # Hardcoded secrets
    if "hardcoded" in text:
        return "HIGH", "Use environment variables instead of hardcoding secrets."

    # Dangerous eval
    elif "eval" in text:
        return "CRITICAL", "Replace eval() with ast.literal_eval()."

    # os.system usage
    elif "os.system" in text:
        return "CRITICAL", "Use subprocess.run() instead of os.system()."

    # Weak hashing
    elif "md5" in text:
        return "MEDIUM", "Use SHA-256 instead of MD5."

    # Safe subprocess handling
    elif "subprocess" in text:

        # Only fail if actual shell execution exists
        if "shell=true" in text:
            return "CRITICAL", "Avoid shell=True in subprocess."

        # Otherwise treat as informational
        return "LOW", "Safe subprocess usage detected."

    else:
        return "LOW", "Review manually."
def analyze_bandit_report():

    with open("bandit-report.json") as f:
        data = json.load(f)

    results = data.get("results", [])
    # Save historical reports
    import datetime

    timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

    with open(f"history/report_{timestamp}.json", "w") as history_file:
        json.dump(results, history_file, indent=4)

    final_decision = "PASS"

    comment = "## AI Security Report\n\n"

    # NEW JSON STORAGE
    issues_data = []

    for issue in results:

        text = issue.get("issue_text", "")
        # severity, suggestion = classify_and_suggest(text)
        # risk_score = SEVERITY_SCORES.get(severity, 0)
        try:
            severity, suggestion = ai_classify(text)

            lower_text = text.lower()

            # SAFE subprocess override
            if "subprocess" in lower_text:
                if "shell=true" not in lower_text:
                    severity = "LOW"
                    suggestion = "Safe subprocess usage detected."

            # Partial executable path override
            if "partial executable path" in lower_text:
                severity = "LOW"
                suggestion = "Controlled executable usage detected."

            # SAFE ast.literal_eval override
            if "literal_eval" in lower_text:
                severity = "LOW"
                suggestion = "Safe evaluation method used."

            # SAFE sha256 override
            if "sha256" in lower_text:
                severity = "LOW"
                suggestion = "Strong hashing algorithm used."

            risk_score = SEVERITY_SCORES.get(severity, 0)

        except Exception:
            severity, suggestion = classify_and_suggest(text)
            risk_score = SEVERITY_SCORES.get(severity, 0)

        comment += f"# 🤖 AI Severity: {severity}\n"        
        comment += f"- *Issue*: {text}\n"
        comment += f"- *Risk Score*: {risk_score}/100\n"
        comment += f"- *Fix*: {suggestion}\n\n"

        # STORE DATA FOR DASHBOARD
        issues_data.append({
            "issue_text": text,
            "severity": severity,
            "ai_analysis": suggestion
        })
        cvss_score = CVSS_MAPPING.get(severity, 0)
        if severity in ["HIGH", "CRITICAL"]:
            final_decision = "FAIL"

    comment += f"\n*Final Decision:* {final_decision}\n"
    comment += f"- *CVSS Score* {cvss_score}\n"


    # SAVE COMMENT FILE
    with open("comment.txt", "w", encoding="utf-8") as f:
        f.write(comment)

    # ----------------------------
    # NEW JSON OUTPUT FOR UI
    # ----------------------------

    final_data = {
        "issues": issues_data,
        "final_decision": final_decision
    }
    

    with open("reports/final-report.json", "w") as f:
        json.dump(final_data, f, indent=4)

    print(comment)

    if final_decision == "FAIL":
        exit(1)
    else:
        exit(0)

if __name__ == "__main__":
    analyze_bandit_report()
