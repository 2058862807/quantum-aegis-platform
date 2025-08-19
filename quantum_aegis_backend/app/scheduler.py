from apscheduler.schedulers.background import BackgroundScheduler
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.database import SessionLocal
from app.models import QuantumKey, Counters
from app.services.pqc import generate_keypair
from app.config import settings
sched = BackgroundScheduler()
def rotate_keys():
async def _run():
async with SessionLocal() as db:
alg, pub, priv = generate_keypair()
qk = QuantumKey(alg=alg, pub=pub, priv=priv)
db.add(qk)
res = await db.execute(select(Counters).limit(1))
row = res.scalar_one_or_none()
if not row:
row = Counters()
db.add(row)
row.quantum_keys_active += 1
await db.commit()
import asyncio
asyncio.get_event_loop().create_task(_run())
def start_scheduler():
sched.add_job(rotate_keys, "interval", minutes=settings.key_rotation_min, id="key_rotation", replace_existing=True)
if not sched.running: sched.start()
