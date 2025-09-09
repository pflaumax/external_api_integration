import os
from datetime import datetime

os.makedirs('github_users', exist_ok=True)
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

CSV_FILE_PATH = f"github_users/users_{timestamp}.csv"
REDIS_URL = os.getenv('REDIS_URL', 'redis://redis:6379/0')
GITHUB_API_URL = "https://api.github.com/users"