import json
import os

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

    for issue in results:
        text = issue.get("issue_text", "")
        severity, suggestion = classify_and_suggest(text)

        comment += f"### ⚠️ {severity}\n"
        comment += f"- **Issue**: {text}\n"
        comment += f"- **Fix**: {suggestion}\n\n"

        if severity in ["HIGH", "CRITICAL"]:
            final_decision = "FAIL"

    comment += f"\n**Final Decision:** {final_decision}\n"

    # Save comment to file
    with open("comment.txt", "w", encoding="utf-8") as f:

        f.write(comment)

    print(comment)

    if final_decision == "FAIL":
        exit(1)
    else:
        exit(0)

if __name__ == "__main__":
    analyze_bandit_report()
