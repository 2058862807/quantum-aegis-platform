from pydantic import BaseModel, Field
class IPCheckRequest(BaseModel):
ip: str
org_key: str | None = None
class DecisionResponse(BaseModel):
decision: str
risk_score: float = Field(ge=0, le=1)
signals: dict
cached: bool = False
class Metrics(BaseModel):
live_threats: int
threats_blocked_today: int
ai_decisions_hour: int
quantum_keys_active: int
