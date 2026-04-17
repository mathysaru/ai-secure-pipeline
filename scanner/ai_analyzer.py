import json

def classify_vulnerability(issue_text):
    issue_text = issue_text.lower()

    if "hardcoded" in issue_text:
        return "HIGH"
    elif "eval" in issue_text:
        return "CRITICAL"
    elif "shell" in issue_text or "os.system" in issue_text:
        return "CRITICAL"
    elif "md5" in issue_text:
        return "MEDIUM"
    else:
        return "LOW"

def analyze_bandit_report():
    with open("bandit-report.json") as f:
        data = json.load(f)

    results = data.get("results", [])

    final_decision = "PASS"

    print("\n🔍 AI ANALYSIS RESULT:\n")

    for issue in results:
        text = issue.get("issue_text", "")
        severity = classify_vulnerability(text)

        print(f"Issue: {text}")
        print(f"AI Severity: {severity}\n")

        if severity in ["HIGH", "CRITICAL"]:
            final_decision = "FAIL"

    print("🚦 FINAL PIPELINE DECISION:", final_decision)

    if final_decision == "FAIL":
        exit(1)  # This will break pipeline
    else:
        exit(0)

if __name__ == "__main__":
    analyze_bandit_report()
