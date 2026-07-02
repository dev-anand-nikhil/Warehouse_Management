# FreshTrack

FreshTrack is an inbound fruit & vegetable receiving system. The application includes:

- Backend: FastAPI, SQLAlchemy, PostgreSQL, JWT authentication, Pydantic v2
- Frontend: React, Vite, TypeScript, Tailwind CSS
- Containerized local development with Docker Compose

## Architecture

The repository is structured with two main folders:

- `app/` - FastAPI service with domain models, repositories, services, and API routers
- `frontend/` - React/Vite application with pages, components, hooks, and service layer

## Features

- JWT authentication with Central Admin and Hub User roles
- Warehouse CRUD operations and user-to-warehouse assignments
- Invoice upload via CSV with validation and duplicate prevention
- Scan workflow with atomic quantity updates and row locking
- Manual quantity adjustments with audit logging
- Reconciliation reporting with date, warehouse, and vendor filters
- Swagger documentation available automatically via FastAPI

## Prerequisites

- Docker
- Docker Compose

## Setup Documentation

See `SETUP.md` for step-by-step instructions for users cloning this repository.

## Environment

The application uses the following default development environment values:

- `DATABASE_URL`: `postgresql+psycopg2://freshtrack:freshtrack@db:5432/freshtrack`
- `JWT_SECRET`: `supersecret`
- `JWT_EXPIRATION_MINUTES`: `60`

These are configured in `docker-compose.yml` for local development.

## Running Locally

From the repository root:

```bash
docker compose up --build
```

This command will start:

- Backend API on `http://localhost:8000`
- Frontend app on `http://localhost:5173`
- PostgreSQL on `localhost:5432`

## Backend API

The backend exposes the following main endpoints:

- `POST /api/auth/login` - Authenticate users and return JWT
- `POST /api/auth/register` - Create new users
- `GET /api/warehouses` - List warehouses
- `POST /api/warehouses` - Create a warehouse
- `DELETE /api/warehouses/{warehouse_id}` - Delete a warehouse
- `POST /api/invoices/upload` - Upload invoice CSV file
- `GET /api/invoices/warehouse/{warehouse_id}` - List invoices for a warehouse
- `POST /api/scan` - Scan barcode and increment received quantities
- `POST /api/adjust` - Manual quantity adjustment for scanned items
- `POST /api/reports/reconciliation` - Generate reconciliation reports

### API Documentation

Swagger UI is available at:

- `http://localhost:8000/docs`
- See `REQUIREMENTS.md` for detailed business and technical requirements

## Frontend

The frontend supports:

- Login
- Dashboard overview
- Invoice upload
- Warehouse management pages
- Invoice list and scan screen
- Report filtering and export placeholders

## Development Notes

- The backend is implemented using a layered architecture with `repositories`, `services`, and `api` routers.
- JWT authentication is handled by `app.services.auth_service` and request validation by `app.core.security`.
- Invoice scanning and manual adjustments use row locking to prevent race conditions.
- Audit logs capture every scan and adjustment with timestamp, user, old/new quantities, and reason.

## Running Tests

From the repository root, run:

```bash
cd app
pytest
```

## Seed Data

A simple seed script is available at `app/seed.py` to create an initial admin user and a default warehouse.

## Assumptions and Trade-offs

- Barcode decoding is implemented as `SKU-{sku}` for simplicity.
- Invoice uploads currently support CSV and validate required fields.
- Frontend is scaffolded with page navigation and upload/scan flows; further UI polish is planned.
- Role-based protections are implemented in backend dependencies but can be extended to more granular policies.

## Future Improvements

- Add Excel invoice upload support
- Implement full RBAC middleware with route-level permissions
- Add robust reporting export formats and UI filters
- Expand frontend pages with real-time warehouse selection and assigned warehouse views
- Add more comprehensive automated tests and database migrations via Alembic
