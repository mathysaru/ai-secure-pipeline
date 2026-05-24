import json

class SecurityEngine:

    def calculate_pipeline_risk(self, vulnerabilities):
        total = 0

        for v in vulnerabilities:
            total += v["risk_score"]

        if total > 200:
            return "FAIL"

        return "PASS"

    def generate_summary(self, vulnerabilities):

        critical = len([v for v in vulnerabilities if v["severity"] == "CRITICAL"])
        high = len([v for v in vulnerabilities if v["severity"] == "HIGH"])

        return {
            "critical": critical,
            "high": high,
            "total": len(vulnerabilities)
        }