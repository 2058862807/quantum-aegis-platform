from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_db
from app.models import Counters
from app.schemas import Metrics
router = APIRouter(prefix="/metrics", tags=["metrics"])
@router.get("", response_model=Metrics)
async def get_metrics(db: AsyncSession = Depends(get_db)):
res = await db.execute(select(Counters).limit(1))
row = res.scalar_one_or_none()
if not row:
row = Counters()
db.add(row)
await db.commit()
await db.refresh(row)
return Metrics(live_threats=row.live_threats, threats_blocked_today=row.threats_blocked_today, ai_decisions_hour=row.ai_decisions_hour, quantum_keys_active=row.quantum_keys_active)
