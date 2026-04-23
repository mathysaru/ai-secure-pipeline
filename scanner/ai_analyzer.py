import json
import requests
import os

API_KEY = os.getenv("OPENAI_API_KEY")
print("DEBUG API KEY:", API_KEY)
def get_ai_suggestion(issue_text):
    prompt = f"""
    You are a cybersecurity expert.

    Analyze this vulnerability and provide:
    1. Severity (LOW, MEDIUM, HIGH, CRITICAL)
    2. Fix suggestion

    Vulnerability:
    {issue_text}
    """

    try:
        response = requests.post(
            "https://api.openai.com/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {API_KEY}",
                "Content-Type": "application/json"
            },
            json={
                "model": "gpt-4o-mini",
                "messages": [{"role": "user", "content": prompt}],
                "temperature": 0.3
            }
        )

        data = response.json()

        if "error" in data:
            print("❌ API ERROR:", data["error"])
            return None

        return data["choices"][0]["message"]["content"]

    except Exception as e:
        print("❌ EXCEPTION:", str(e))
        return None

def analyze_bandit_report():
    with open("bandit-report.json") as f:
        data = json.load(f)

    results = data.get("results", [])
    final_decision = "PASS"

    comment = "## 🔐 AI Security Report (Dynamic)\n\n"

    for issue in results:
        text = issue.get("issue_text", "")

        ai_output = get_ai_suggestion(text)

        if ai_output is None:
            ai_output = "Fallback: Manual review required. Potential high risk vulnerability."
            final_decision = "FAIL"   # 🔥 important

        comment += f"### 🔍 Issue\n{text}\n\n"
        comment += f"🤖 AI Analysis:\n{ai_output}\n\n"

        if any(word in ai_output.lower() for word in ["critical", "high"]):
            final_decision = "FAIL"
        if len(results) > 0 and final_decision != "FAIL":
            final_decision = "FAIL"



    comment += f"\n🚦 Final Decision: {final_decision}\n"

    with open("comment.txt", "w") as f:
        f.write(comment)

    print(comment)

    if final_decision == "FAIL":
        exit(1)
    else:
        exit(0)

if __name__ == "__main__":
    analyze_bandit_report()
