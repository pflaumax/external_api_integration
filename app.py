from fastapi import FastAPI
from tasks import fetch_users_and_save


app = FastAPI(title="External Github API integration", version="0.0.1")

@app.get("/")
def main_page():
    """Main page endpoint message"""
    return {"message": "Welcome to the external Github API integration"}

@app.post("/fetch_users")
def fetch_users():
    """Start the celery task to fetch users and save to CSV"""
    task = fetch_users_and_save.delay()
    return {
        "message": "GitHub users fetch task started",
        "task_id": task.id,
        "status": "Task added to queue"
    }

@app.get("/check_status")
def status_check():
    """Check status that endpoint is started and running"""
    return {"status": "OK"}
