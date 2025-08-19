from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Integer, ForeignKey, DateTime, Boolean, JSON, BigInteger, UniqueConstraint, func
from app.database import Base
class Org(Base):
tablename = "orgs"
id: Mapped[int] = mapped_column(primary_key=True)
name: Mapped[str] = mapped_column(String(120), unique=True, index=True)
plan: Mapped[str] = mapped_column(String(50), default="essential")
api_keys = relationship("APIKey", back_populates="org")
class APIKey(Base):
tablename = "api_keys"
id: Mapped[int] = mapped_column(primary_key=True)
org_id: Mapped[int] = mapped_column(ForeignKey("orgs.id", ondelete="CASCADE"))
key: Mapped[str] = mapped_column(String(64), unique=True, index=True)
active: Mapped[bool] = mapped_column(Boolean, default=True)
created_at: Mapped[DateTime] = mapped_column(DateTime(timezone=True), default=func.now())
org = relationship("Org", back_populates="api_keys")
class QuantumKey(Base):
tablename = "quantum_keys"
id: Mapped[int] = mapped_column(primary_key=True)
alg: Mapped[str] = mapped_column(String(50))
pub: Mapped[str] = mapped_column(String(4096))
priv: Mapped[str] = mapped_column(String(4096))
rotated_at: Mapped[DateTime] = mapped_column(DateTime(timezone=True), server_default=func.now())
class ThreatCheck(Base):
tablename = "threat_checks"
id: Mapped[int] = mapped_column(primary_key=True)
org_id: Mapped[int] = mapped_column(ForeignKey("orgs.id", ondelete="CASCADE"))
subject: Mapped[str] = mapped_column(String(256))
subject_type: Mapped[str] = mapped_column(String(30))
result: Mapped[dict] = mapped_column(JSON)
malicious: Mapped[bool] = mapped_column(Boolean, default=False)
created_at: Mapped[DateTime] = mapped_column(DateTime(timezone=True), server_default=func.now())
table_args = (UniqueConstraint("org_id", "subject", "subject_type", "created_at"),)
class DecisionLog(Base):
tablename = "decision_logs"
id: Mapped[int] = mapped_column(primary_key=True)
org_id: Mapped[int] = mapped_column(ForeignKey("orgs.id", ondelete="CASCADE"))
action: Mapped[str] = mapped_column(String(30))
reason: Mapped[dict] = mapped_column(JSON)
created_at: Mapped[DateTime] = mapped_column(DateTime(timezone=True), server_default=func.now())
class Counters(Base):
tablename = "counters"
id: Mapped[int] = mapped_column(primary_key=True)
live_threats: Mapped[int] = mapped_column(BigInteger, default=302928)
threats_blocked_today: Mapped[int] = mapped_column(BigInteger, default=298193)
ai_decisions_hour: Mapped[int] = mapped_column(BigInteger, default=2495)
quantum_keys_active: Mapped[int] = mapped_column(Integer, default=855)
