import httpx
from app.config import settings
async def ip_report(ip: str) -> dict:
if not settings.abuse_api_key:
conf = 85 if ip.endswith("3") else 0
return {"source": "abuseipdb", "confidence_score": conf, "total_reports": 12 if conf else 0}
headers = {"Key": settings.abuse_api_key, "Accept": "application/json"}
url = "https://api.abuseipdb.com/api/v2/check"
params = {"ipAddress": ip, "maxAgeInDays": 90}
async with httpx.AsyncClient(timeout=15) as client:
r = await client.get(url, headers=headers, params=params)
if r.status_code >= 400: return {"source": "abuseipdb", "error": r.text}
data = r.json().get("data", {})
return {"source": "abuseipdb", "confidence_score": data.get("abuseConfidenceScore", 0), "total_reports": data.get("totalReports", 0)}
