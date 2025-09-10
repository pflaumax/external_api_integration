import csv
import requests
import logging
from datetime import datetime
from celery import Celery
from config import GITHUB_API_URL, CSV_FOLDER, REDIS_URL, CELERY_BACKEND


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

celery_app = Celery(
    'tasks',
    broker=REDIS_URL,
    backend=CELERY_BACKEND
)

@celery_app.task
def fetch_users_and_save() :
    """Fetch users from GitHub API and save to CSV"""
    logger.info("Starting fetch task")

    try:
        response = requests.get(f"{GITHUB_API_URL}?per_page=30")
        response.raise_for_status()
        users = response.json()

        logger.info(f"Received {len(users)} users from GitHub API")

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        csv_file_path = f"{CSV_FOLDER}/github_users_{timestamp}.csv"

        with open(csv_file_path, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(['ID', 'Name', 'URL'])

            for user in users:
                writer.writerow([
                    user.get('id', ''),
                    user.get('login', ''),
                    user.get('html_url', '')
                ])

        logger.info(f"Task completed successfully. Data saved to {csv_file_path}")

        return {
            'status': 'success',
            'message': f"Successfully fetched and saved {len(users)} GitHub users",
            'file_path': csv_file_path,
            'timestamp': timestamp
        }

    except requests.RequestException as e:
        return f'Error fetching data from GitHub API: {str(e)}'
    except Exception as e:
        return f'Unexpected error: {str(e)}'