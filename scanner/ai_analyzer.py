import json
import os
from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def get_ai_analysis(issue_text):
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "system",
                    "content": "You are a cybersecurity expert. Classify vulnerability severity (LOW, MEDIUM, HIGH, CRITICAL) and suggest a secure fix."
                },
                {
                    "role": "user",
                    "content": f"Analyze this vulnerability:\n{issue_text}"
                }
            ],
            temperature=0.3,
            max_tokens=120
        )

        output = response.choices[0].message.content.strip()

        # Extract severity (simple parsing)
        if "CRITICAL" in output:
            severity = "CRITICAL"
        elif "HIGH" in output:
            severity = "HIGH"
        elif "MEDIUM" in output:
            severity = "MEDIUM"
        else:
            severity = "LOW"

        return severity, output

    except Exception as e:
        return "MEDIUM", f"AI unavailable: {str(e)}"


def analyze_bandit_report():
    with open("bandit-report.json") as f:
        data = json.load(f)

    results = data.get("results", [])
    final_decision = "PASS"

    comment = "## 🔐 AI Security Report (Dynamic AI)\n\n"

    for issue in results:
        text = issue.get("issue_text", "")

        severity, suggestion = get_ai_analysis(text)

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
