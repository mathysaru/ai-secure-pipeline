import json

def classify_and_suggest(issue_text):
    issue_text_lower = issue_text.lower()

    if "hardcoded" in issue_text_lower:
        return "HIGH", "Use environment variables instead of hardcoding secrets."

    elif "eval" in issue_text_lower:
        return "CRITICAL", "Replace eval() with ast.literal_eval() for safe evaluation."

    elif "shell" in issue_text_lower or "os.system" in issue_text_lower:
        return "CRITICAL", "Avoid os.system(). Use subprocess.run() with argument list."

    elif "md5" in issue_text_lower:
        return "MEDIUM", "Replace MD5 with SHA-256 for secure hashing."

    else:
        return "LOW", "Review code manually."

def analyze_bandit_report():
    with open("bandit-report.json") as f:
        data = json.load(f)

    results = data.get("results", [])
    final_decision = "PASS"

    print("\n🔍 AI ANALYSIS + FIX SUGGESTIONS:\n")

    for issue in results:
        text = issue.get("issue_text", "")

        severity, suggestion = classify_and_suggest(text)

        print(f"Issue: {text}")
        print(f"AI Severity: {severity}")
        print(f"💡 Suggested Fix: {suggestion}\n")

        if severity in ["HIGH", "CRITICAL"]:
            final_decision = "FAIL"

    print("🚦 FINAL PIPELINE DECISION:", final_decision)

    if final_decision == "FAIL":
        print("\n⚠️ Developer Action Required: Please fix the above issues.\n")
        exit(1)
    else:
        print("\n✅ Code is secure. Ready for deployment.\n")
        exit(0)

if __name__ == "__main__":
    analyze_bandit_report()
