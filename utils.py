
def run_health_checks(log_data):
    issues = []
    if "CRITICAL" in log_data:
        issues.append("🔴 Critical errors found in logs.")
    if "unauthorized access" in log_data.lower():
        issues.append("🛑 Unauthorized access attempt detected.")
    if "firewall disabled" in log_data.lower():
        issues.append("⚠️ Firewall appears to be disabled.")
    if not issues:
        issues.append("✅ No critical issues found.")
    return issues
