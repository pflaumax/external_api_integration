import csv
import requests
import logging
from datetime import datetime
from typing import List, Dict, Any
from celery import Celery
from config import GITHUB_API_URL, CSV_FOLDER, REDIS_URL, CELERY_BACKEND, USERS_PER_PAGE, API_TIMEOUT


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

celery_app = Celery(
    'tasks',
    broker=REDIS_URL,
    backend=CELERY_BACKEND
)


def fetch_github_users() -> List[Dict[str, Any]]:
    """Fetch users from GitHub API"""
    logger.info("Fetching users from GitHub API")

    response = requests.get(
        f"{GITHUB_API_URL}?per_page={USERS_PER_PAGE}",
        timeout=API_TIMEOUT
    )
    response.raise_for_status()
    users = response.json()

    logger.info(f"Received {len(users)} users from GitHub API")
    return users


def save_users_to_csv(users: List[Dict[str, Any]], file_path: str) -> None:
    """Save users data to CSV file"""
    logger.info(f"Saving {len(users)} users to CSV file: {file_path}")

    with open(file_path, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['ID', 'Name', 'URL'])

        for user in users:
            writer.writerow([
                user.get('id', ''),
                user.get('login', ''),
                user.get('html_url', '')
            ])


@celery_app.task
def fetch_users_and_save() -> Dict[str, Any]:
    """Fetch users from GitHub API and save to CSV"""
    logger.info("Starting fetch task")

    try:
        users = fetch_github_users()

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        csv_file_path = f"{CSV_FOLDER}/github_users_{timestamp}.csv"
        save_users_to_csv(users, csv_file_path)

        logger.info("Task completed successfully")

        return {
            'status': 'success',
            'message': f"Successfully fetched and saved {len(users)} GitHub users",
            'file_path': csv_file_path,
            'timestamp': timestamp
        }

    except requests.exceptions.Timeout:
        error_msg = f"API request timeout after {API_TIMEOUT} seconds"
        logger.error(error_msg)
        return {'status': 'error', 'message': error_msg}

    except requests.RequestException as e:
        error_msg = f'Error fetching data from GitHub API: {str(e)}'
        logger.error(error_msg)
        return {'status': 'error', 'message': error_msg}

    except Exception as e:
        error_msg = f'Unexpected error: {str(e)}'
        logger.error(error_msg)
        return {'status': 'error', 'message': error_msg}