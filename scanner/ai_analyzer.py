import json
import os

# Try importing OpenAI safely
try:
    from openai import OpenAI
    api_key = os.getenv("OPENAI_API_KEY")
    client = OpenAI(api_key=api_key) if api_key else None
except Exception:
    client = None

def get_ai_suggestion(issue_text):
    # ✅ If API key exists → use real AI
    if client:
        try:
            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": "You are a cybersecurity expert."},
                    {"role": "user", "content": f"Vulnerability: {issue_text}. Give severity and fix."}
                ],
                max_tokens=150
            )

            output = response.choices[0].message.content

            if "CRITICAL" in output:
                severity = "CRITICAL"
            elif "HIGH" in output:
                severity = "HIGH"
            elif "MEDIUM" in output:
                severity = "MEDIUM"
            else:
                severity = "LOW"

            return severity, output

        except Exception:
            pass  # fallback if API fails

    # ✅ FALLBACK (ALWAYS WORKS — VERY IMPORTANT FOR DEMO)
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
        return "LOW", "Manual review required."


def analyze_bandit_report():
    with open("bandit-report.json") as f:
        data = json.load(f)

    results = data.get("results", [])
    final_decision = "PASS"

    comment = "## 🔐 AI Security Report (Dynamic AI)\n\n"

    for issue in results:
        text = issue.get("issue_text", "")

        severity, suggestion = get_ai_suggestion(text)

        comment += f"### ⚠️ {severity}\n"
        comment += f"- **Issue**: {text}\n"
        comment += f"- **AI Suggestion**: {suggestion}\n\n"

        if severity in ["HIGH", "CRITICAL"]:
            final_decision = "FAIL"

    comment += f"\n🚦 **Final Decision:** {final_decision}\n"

    with open("comment.txt", "w") as f:
        f.write(comment)

    print(comment)

    if final_decision == "FAIL":
        exit(1)
    else:
        exit(0)


if __name__ == "__main__":
    analyze_bandit_report()
