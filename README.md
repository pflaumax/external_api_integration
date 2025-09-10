# External API Integration

Simple project to fetch users from a public API and save them into a CSV file using FastAPI, Celery, and Redis.

## What the project does

1. Fetches a list of users from GitHub public API [https://api.github.com/users](https://api.github.com/users)
2. Saves the data to a CSV file (ID, Name, URL)
3. Executes tasks asynchronously using Celery
4. Redis as a message broker
5. Runs all components in Docker containers

## Project structure

```
external_api_integration/
├── docker-compose.yml     # Docker configuration
├── Dockerfile             # Images for FastAPI, Celery and Redis
├── requirements.txt       # Python dependencies
├── config.py              # File configuration 
├── app.py                 # FastAPI application
├── tasks.py               # Celery tasks
├── README.md              # This file
└── github_users/          # Folder for CSV files
```

## How to run

### 1. Clone and go to the folder

```bash
git clone https://github.com/pflaumax/external_api_integration.git
cd external_api_integration
```

### 2. Build and Run with Docker Compose

```bash
docker compose up --build
```
For runs after build, you can simply start containers in detached mode:
```bash
docker compose up -d
```
### 3. Check that everything works

Open a browser and go to [http://localhost:8000/check_status](http://localhost:8000/check_status)

And main page showing:

```json
{"status":"OK"}
```

## How to use

### Run the user fetching task

Send a POST request to `/fetch_users` by:

```bash
curl -X POST http://localhost:8000/fetch_users
```

Or open [http://localhost:8000/docs](http://localhost:8000/docs) Fetch Users and use `Try it out` and `Execute`.

### Result

After the task is completed, a CSV file will appear in the `github_users/` folder named like `github_users_20250910_130828.csv` with time stamp and containing data:

```csv
ID,Name,URL
1,mojombo,https://github.com/mojombo
2,defunkt,https://github.com/defunkt
3,pjhyett,https://github.com/pjhyett
...
```

## API Endpoints

* `GET /` - Main page
* `POST /fetch_users` - Start the user fetching task
* `GET /check_status"` - Check status that endpoint is working
* `GET /docs` - Documentation Swagger UI
* `GET/redoc` - Documentation ReDoc

## Stop the project

```bash
docker compose down
```
