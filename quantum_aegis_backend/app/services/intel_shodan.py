import httpx
from app.config import settings
async def ip_report(ip: str) -> dict:
if not settings.shodan_api_key:
open_ports = [22, 80, 443] if int(ip.split(".")[-1]) % 2 == 0 else [445]
return {"source": "shodan", "open_ports": open_ports, "vuln_count": 1 if 445 in open_ports else 0}
params = {"key": settings.shodan_api_key}
url = f"https://api.shodan.io/shodan/host/{ip}"
async with httpx.AsyncClient(timeout=15) as client:
r = await client.get(url, params=params)
if r.status_code >= 400: return {"source": "shodan", "error": r.text}
data = r.json()
ports = data.get("ports", [])
vulns = data.get("vulns", {})
return {"source": "shodan", "open_ports": ports, "vuln_count": len(vulns)}
