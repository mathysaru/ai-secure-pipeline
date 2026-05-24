import json
import os
import joblib

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

    if "hardcoded" in text:
        return "HIGH", "Use environment variables instead of hardcoding secrets."
    elif "eval" in text:
        return "CRITICAL", "Replace eval() with ast.literal_eval()."
    elif "shell" in text or "os.system" in text:
        return "CRITICAL", "Use subprocess.run() instead of os.system()."
    elif "md5" in text:
        return "MEDIUM", "Use SHA-256 instead of MD5."
    else:
        return "LOW", "Review manually."

def analyze_bandit_report():

    with open("bandit-report.json") as f:
        data = json.load(f)

    results = data.get("results", [])

    final_decision = "PASS"

    comment = "## AI Security Report\n\n"

    # NEW JSON STORAGE
    issues_data = []

    for issue in results:

        text = issue.get("issue_text", "")

        try:
            severity, suggestion = ai_classify(text)
        except:
            severity, suggestion = classify_and_suggest(text)

        comment += f"### 🤖 AI Severity: {severity}\n"        
        comment += f"- **Issue**: {text}\n"
        comment += f"- **Fix**: {suggestion}\n\n"

        # STORE DATA FOR DASHBOARD
        issues_data.append({
            "issue_text": text,
            "severity": severity,
            "ai_analysis": suggestion
        })

        if severity in ["HIGH", "CRITICAL"]:
            final_decision = "FAIL"

    comment += f"\n**Final Decision:** {final_decision}\n"

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

    with open("ai-report.json", "w") as f:
        json.dump(final_data, f, indent=4)

    print(comment)

    if final_decision == "FAIL":
        exit(1)
    else:
        exit(0)
if __name__ == "__main__":
    analyze_bandit_report()
