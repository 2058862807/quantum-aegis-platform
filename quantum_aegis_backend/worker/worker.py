﻿from redis import Redis
from rq import Queue
from app.config import settings
redis = Redis.from_url(settings.redis_url)
q = Queue("threat-jobs", connection=redis)
