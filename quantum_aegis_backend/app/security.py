import time, jwt, secrets
from passlib.hash import bcrypt
from app.config import settings
def create_api_key() -> str: return secrets.token_hex(24)
def hash_password(p: str) -> str: return bcrypt.hash(p)
def verify_password(p: str, h: str) -> bool: return bcrypt.verify(p, h)
def jwt_encode(sub: str, scopes: list[str]) -> str:
now = int(time.time())
payload = {"iss": settings.jwt_issuer, "aud": settings.jwt_audience, "sub": sub, "scopes": scopes, "iat": now, "exp": now + 60 * settings.jwt_expire_min}
return jwt.encode(payload, settings.jwt_secret, algorithm="HS256")
