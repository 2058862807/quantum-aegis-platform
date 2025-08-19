import redis, json
from app.config import settings
_redis = redis.from_url(settings.redis_url, decode_responses=True)
def get(key: str):
val = _redis.get(key)
if not val: return None
try: return json.loads(val)
except Exception: return val
def setex(key: str, value, ttl: int):
_redis.setex(key, ttl, json.dumps(value))
