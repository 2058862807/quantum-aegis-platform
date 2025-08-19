def score(signals: dict):
vt = signals.get("virustotal", {})
sh = signals.get("shodan", {})
ab = signals.get("abuseipdb", {})
vt_bad = float(vt.get("malicious", 0))
vt_total = max(1.0, vt_bad + float(vt.get("harmless", 0)))
vt_score = vt_bad / vt_total
sh_score = 0.0
if 445 in sh.get("open_ports", []): sh_score = 0.5
sh_score += min(0.5, 0.1 * float(sh.get("vuln_count", 0)))
ab_score = float(ab.get("confidence_score", 0)) / 100.0
risk = min(1.0, 0.5 * vt_score + 0.3 * sh_score + 0.2 * ab_score)
decision = "deny" if risk >= 0.6 else "flag" if risk >= 0.3 else "allow"
reasons = {"vt": vt_score, "shodan": sh_score, "abuse": ab_score}
return risk, reasons, decision
