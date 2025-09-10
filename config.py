import os


os.makedirs('github_users', exist_ok=True)

CSV_FOLDER = "github_users"
REDIS_URL = os.getenv('REDIS_URL', 'redis://redis:6379/0')
CELERY_BACKEND = os.getenv("CELERY_BACKEND", REDIS_URL)
GITHUB_API_URL = "https://api.github.com/users"

USERS_PER_PAGE = int(os.getenv('USERS_PER_PAGE', '30'))
API_TIMEOUT = int(os.getenv('API_TIMEOUT', '30'))