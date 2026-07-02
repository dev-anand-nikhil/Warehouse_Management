# FreshTrack Setup Guide

This document is for users who clone the FreshTrack repository and want to run the application locally.

## Prerequisites

Before you begin, make sure you have:

- Docker installed and running
- Docker Compose available (usually bundled with Docker Desktop)
- Git installed

## Clone the repository

```bash
git clone <repo-url>
cd FreshTrack
```

## Start the application

The application is containerized with Docker Compose. From the repository root, run:

```bash
docker compose up --build
```

This will start:

- Backend API on `http://localhost:8000`
- Frontend app on `http://localhost:5173`
- PostgreSQL database on `localhost:5432`

## Verify the services

- Backend health: `http://localhost:8000/health`
- Swagger docs: `http://localhost:8000/docs`
- Frontend app: `http://localhost:5173`

## Stop the application

When you are finished, stop the containers with:

```bash
docker compose down
```

## Troubleshooting

### Docker Compose command not found

If `docker compose` is not available, try:

```bash
docker-compose up --build
```

### Docker daemon not running

Start Docker Desktop or your Docker service before running compose.

### Rebuild after code changes

If you update backend dependencies or Docker configuration, rebuild the containers:

```bash
docker compose up --build --force-recreate
```

## Notes

- Backend code lives in the `app/` folder.
- Frontend code lives in the `frontend/` folder.
- The repository also includes `.gitignore` to exclude local build artifacts, node_modules, and Python cache files.
