import httpx
from app.config import settings
async def ip_report(ip: str) -> dict:
if not settings.vt_api_key:
return {"source": "virustotal", "harmless": 70, "malicious": 1 if ip.endswith("7") else 0}
headers = {"x-apikey": settings.vt_api_key}
url = f"https://www.virustotal.com/api/v3/ip_addresses/{ip}"
async with httpx.AsyncClient(timeout=15) as client:
r = await client.get(url, headers=headers)
if r.status_code >= 400: return {"source": "virustotal", "error": r.text}
data = r.json()
stats = data.get("data", {}).get("attributes", {}).get("last_analysis_stats", {})
return {"source": "virustotal", **stats}
