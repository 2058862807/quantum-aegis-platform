from fastapi import APIRouter, Depends
from app.schemas import IPCheckRequest, DecisionResponse
from app.services import cache, intel_vt, intel_shodan, intel_abuse, decision_engine
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.database import get_db
from app.models import DecisionLog, Counters
import asyncio
router = APIRouter(prefix="/intel", tags=["intel"])
@router.post("/ip-check", response_model=DecisionResponse)
async def ip_check(payload: IPCheckRequest, db: AsyncSession = Depends(get_db)):
ck = f"ipcache:{payload.ip}"
cached = cache.get(ck)
if cached:
return DecisionResponse(**cached, cached=True)
vt, sh, ab = await asyncio.gather(
intel_vt.ip_report(payload.ip),
intel_shodan.ip_report(payload.ip),
intel_abuse.ip_report(payload.ip),
)
signals = {"virustotal": vt, "shodan": sh, "abuseipdb": ab}
risk, reasons, decision = decision_engine.score(signals)
res = await db.execute(select(Counters).limit(1))
row = res.scalar_one_or_none()
if not row:
row = Counters()
db.add(row)
row.ai_decisions_hour += 1
if decision == "deny":
row.threats_blocked_today += 1
await db.commit()
resp = DecisionResponse(decision=decision, risk_score=risk, signals={"reasons": reasons, **signals}, cached=False).model_dump()
cache.setex(ck, resp, ttl=86400)
db.add(DecisionLog(org_id=1, action=decision, reason=resp))
await db.commit()
return DecisionResponse(**resp)
