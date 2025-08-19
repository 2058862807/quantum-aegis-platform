import os
from pydantic import BaseModel
from dotenv import load_dotenv
load_dotenv()
class Settings(BaseModel):
database_url: str = os.getenv("DATABASE_URL", "sqlite+aiosqlite:///./qa.db")
redis_url: str = os.getenv("REDIS_URL", "redis://localhost:6379/0")
jwt_secret: str = os.getenv("JWT_SECRET", "dev-secret")
jwt_issuer: str = os.getenv("JWT_ISSUER", "quantum-aegis")
jwt_audience: str = os.getenv("JWT_AUDIENCE", "quantum-aegis-clients")
jwt_expire_min: int = int(os.getenv("JWT_EXPIRE_MIN", "60"))
vt_api_key: str | None = os.getenv("VT_API_KEY") or None
shodan_api_key: str | None = os.getenv("SHODAN_API_KEY") or None
abuse_api_key: str | None = os.getenv("ABUSEIPDB_API_KEY") or None
demo_mode: bool = os.getenv("DEMO_MODE", "true").lower() == "true"
pqc_enable: bool = os.getenv("PQC_ENABLE", "true").lower() == "true"
key_rotation_min: int = int(os.getenv("KEY_ROTATION_MIN", "15"))
settings = Settings()
