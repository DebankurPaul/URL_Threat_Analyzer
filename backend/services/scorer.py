from models.schemas import VirusTotalResult, SSLResult

def calculate_risk_score(
    vt:  VirusTotalResult | None,
    ssl: SSLResult | None,
) -> tuple[int, str]:
    """
    Returns (score 0-100, label) where:
    100 = completely Safe
    0   = completely Dangerous
    """
    score = 100

    # --- VirusTotal signals (max 60 pts deduction) ---
    if vt and vt.total_engines > 0:
        if vt.malicious > 0:
            malicious_ratio = vt.malicious / vt.total_engines
            ratio_deduction = int(malicious_ratio * 70)
            count_deduction = min(60, vt.malicious * 7)
            vt_deduction = max(count_deduction, ratio_deduction)
            score -= min(60, max(5, vt_deduction))

        if vt.suspicious > 0:
            suspicious_deduction = min(20, vt.suspicious * 4)
            score -= suspicious_deduction

    # --- SSL signals (max 40 pts deduction) ---
    if ssl:
        if not ssl.has_ssl:
            score -= 30   # plain HTTP — no encryption
        elif not ssl.is_valid:
            score -= 40   # HTTPS but cert invalid or untrusted
        elif ssl.days_remaining is not None and ssl.days_remaining < 7:
            score -= 10   # expiring in under 7 days

    score = max(0, min(100, score))   # clamp between 0 and 100

    # Map score to human-readable label
    if score >= 85:
        label = "Safe"
    elif score >= 50:
        label = "Suspicious"
    else:
        label = "Dangerous"

    return score, label