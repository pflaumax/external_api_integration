import csv
import requests
from celery import Celery
from config import GITHUB_API_URL, CSV_FILE_PATH, REDIS_URL

celery_app = Celery(
    'tasks',
    broker=REDIS_URL,
    # backend='redis://redis:6379/0'
)

@celery_app.task
def fetch_users_and_save():
    """Fetch users from GitHub API and save to CSV"""
    try:
        response = requests.get(f"{GITHUB_API_URL}?per_page=10")
        response.raise_for_status()
        users = response.json()


        with open(CSV_FILE_PATH, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(['id', 'name', 'url'])

            for user in users:
                writer.writerow([
                    user.get('id', ''),
                    user.get('login', ''),
                    user.get('html_url', '')
                ])

        return f"Successfully fetched and saved {len(users)} GitHub users to {CSV_FILE_PATH}"

    except requests.RequestException as e:
        return f'Error fetching data from GitHub API: {str(e)}'
    except Exception as e:
        return f'Unexpected error: {str(e)}'