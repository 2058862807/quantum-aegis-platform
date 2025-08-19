from fastapi import FastAPI
from app.database import engine, Base
from app.routers import metrics, intel
from app.scheduler import start_scheduler
app = FastAPI(title="Quantum Aegis Backend", version="1.0.0")
@app.on_event("startup")
async def on_start():
async with engine.begin() as conn:
await conn.run_sync(Base.metadata.create_all)
start_scheduler()
app.include_router(metrics.router)
app.include_router(intel.router)
@app.get("/healthz")
async def healthz(): return {"ok": True}
