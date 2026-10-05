# Secure Backend API

A secure REST API built with **FastAPI, PostgreSQL, SQLAlchemy, JWT authentication, role-based access control (RBAC), password hashing, secure file uploads, logging, automated testing, and Docker**.

## Features

- JWT-based authentication
- User registration and login
- Secure password hashing with Argon2 via `pwdlib`
- Role-based access control with `user` and `admin` roles
- Protected API endpoints
- User CRUD operations
- File upload, listing, download, and deletion
- File type and size validation
- PostgreSQL database
- SQLAlchemy ORM
- Pydantic validation
- API logging
- Pytest API tests
- Docker and Docker Compose support
- Interactive Swagger API documentation

## Tech Stack

| Technology | Purpose |
|---|---|
| Python | Backend language |
| FastAPI | REST API framework |
| PostgreSQL | Relational database |
| SQLAlchemy | ORM and database access |
| Pydantic | Request/response validation |
| PyJWT | JWT token generation and validation |
| pwdlib + Argon2 | Password hashing |
| Pytest | Automated testing |
| Docker | Containerization |
| Docker Compose | API + database orchestration |

## Project Structure

```text
secure-backend-api/
│
├── app/
│   ├── __init__.py
│   ├── main.py
│   │
│   ├── core/
│   │   ├── __init__.py
│   │   ├── config.py
│   │   ├── security.py
│   │   └── logging_config.py
│   │
│   ├── db/
│   │   ├── __init__.py
│   │   ├── database.py
│   │   └── models.py
│   │
│   ├── dependencies/
│   │   ├── __init__.py
│   │   └── auth.py
│   │
│   ├── routers/
│   │   ├── __init__.py
│   │   ├── auth.py
│   │   ├── users.py
│   │   ├── files.py
│   │   └── admin.py
│   │
│   ├── schemas/
│   │   ├── __init__.py
│   │   ├── user.py
│   │   ├── auth.py
│   │   └── file.py
│   │
│   └── services/
│       ├── __init__.py
│       └── file_service.py
│
├── tests/
│   ├── __init__.py
│   ├── conftest.py
│   ├── test_auth.py
│   ├── test_users.py
│   └── test_files.py
│
├── uploads/
├── .env
├── .env.example
├── .dockerignore
├── .gitignore
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
└── README.md
```

## API Endpoints

### Authentication

| Method | Endpoint | Access |
|---|---|---|
| POST | `/auth/register` | Public |
| POST | `/auth/login` | Public |
| GET | `/auth/me` | Authenticated |

### Users

| Method | Endpoint | Access |
|---|---|---|
| GET | `/users/` | Authenticated |
| GET | `/users/{user_id}` | Authenticated |
| PUT | `/users/{user_id}` | Owner/Admin |
| DELETE | `/users/{user_id}` | Owner/Admin |

### Files

| Method | Endpoint | Access |
|---|---|---|
| POST | `/files/upload` | Authenticated |
| GET | `/files/` | Authenticated |
| GET | `/files/{filename}` | Authenticated |
| DELETE | `/files/{filename}` | Authenticated |

### Admin

| Method | Endpoint | Access |
|---|---|---|
| GET | `/admin/users` | Admin |
| DELETE | `/admin/users/{user_id}` | Admin |

### System

| Method | Endpoint | Access |
|---|---|---|
| GET | `/` | Public |
| GET | `/health` | Public |
| GET | `/db-test` | Public |

## Authentication Flow

```text
Register
   ↓
Login with username + password
   ↓
Receive JWT access token
   ↓
Authorize using Bearer token
   ↓
Access protected endpoints
   ↓
RBAC checks user role for admin operations
```

## RBAC

The application uses two roles:

- `user` — standard authenticated user
- `admin` — administrative access

Admin endpoints reject normal users with `403 Forbidden`.

## File Upload Security

Uploaded files are validated before being stored:

- Allowed extensions are restricted.
- Maximum file size is enforced.
- Filenames are sanitized with `os.path.basename()`.
- Files are stored in the `uploads/` directory.

## Environment Variables

Create a `.env` file in the project root:

```env
DATABASE_URL=postgresql+psycopg2://postgres:1234@db:5432/secure_db
SECRET_KEY=change-this-to-a-long-random-secret-key
ACCESS_TOKEN_EXPIRE_MINUTES=30
MAX_FILE_SIZE=5242880
UPLOAD_DIR=uploads
```

> Do not commit `.env` or production secrets to GitHub.

## Run with Docker

Make sure Docker Desktop is running.

### Start the application

```powershell
docker compose up -d
```

### Check containers

```powershell
docker ps
```

Expected containers:

```text
secure_db_api
secure_db
```

### View API logs

```powershell
docker compose logs -f api
```

### Stop the application

```powershell
docker compose down
```

### Rebuild from scratch

```powershell
docker compose down
docker compose build --no-cache
docker compose up -d
```

## API Documentation

After starting the application, open:

**Swagger UI**

```text
http://localhost:8000/docs
```

**OpenAPI JSON**

```text
http://localhost:8000/openapi.json
```

## Testing

Run the test suite from the project root:

```powershell
pytest
```

The tests cover basic API availability and authentication requirements for protected endpoints.

## Database Access

Open a PostgreSQL shell inside the database container:

```powershell
docker exec -it secure_db psql -U postgres -d secure_db
```

List tables:

```sql
\dt
```

View users:

```sql
SELECT id, username, email, role FROM users;
```

Exit PostgreSQL:

```sql
\q
```

## Example Usage

### 1. Register

`POST /auth/register`

```json
{
  "username": "harsha",
  "email": "harsha@gmail.com",
  "password": "Test@12345"
}
```

### 2. Login

`POST /auth/login`

Use the Swagger form fields:

```text
username: harsha
password: Test@12345
```

The API returns:

```json
{
  "access_token": "<JWT_TOKEN>",
  "token_type": "bearer"
}
```

### 3. Authorize

Click **Authorize** in Swagger and authenticate with the login credentials. Swagger then sends the JWT as a Bearer token for protected endpoints.

### 4. Current User

`GET /auth/me`

Example response:

```json
{
  "id": 1,
  "username": "harsha",
  "email": "harsha@gmail.com",
  "role": "user"
}
```

## Security Notes

For production use, replace the development secret with a strong random secret, use HTTPS, avoid hard-coded database credentials, add stricter filename/content validation, configure CORS deliberately, and use database migrations such as Alembic instead of `create_all()` for schema management.

## Author

**Harsha Vardhan Basati**

GitHub: [harshavardhanbasati](https://github.com/harshavardhanbasati)

## Repository

[Secure Backend API](https://github.com/harshavardhanbasati/Secure-Backend-API)

## License

This project is intended for learning, portfolio, and demonstration purposes.
