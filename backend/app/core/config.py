import os

# Database
DATABASE_URL = "sqlite+aiosqlite:///titanic.db"

# Redis
# NOTE: uses docker-compose REDIS_HOST
REDIS_URL = f"redis://{os.getenv('REDIS_HOST', 'localhost')}:6379"
REDIS_CACHE_TTL = 600  # 10 mins

# CORS
ALLOWED_ORIGINS = ["http://localhost:3000"]  # React Server
