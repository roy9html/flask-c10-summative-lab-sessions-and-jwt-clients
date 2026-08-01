# Flask Notes API with JWT Authentication

## Project Description

A secure RESTful Flask API for managing personal notes with JWT-based authentication and full CRUD operations. Users can create, read, update, and delete their own notes with pagination support. The API ensures that users can only access and modify their own data, providing robust security and data isolation. This project was built as a summative lab for a backend engineering course, demonstrating best practices in API development, authentication, and database management.

## Features

- JWT-based authentication with access and refresh tokens
- Full CRUD operations for notes (Create, Read, Update, Delete)
- User-specific data isolation - users can only access their own notes
- Pagination for efficient data retrieval with page and per_page parameters
- Note categories for organizing notes
- Archive and unarchive functionality for notes
- Input validation using Marshmallow schemas
- Database migrations with Flask-Migrate
- Database seeding with sample data for testing
- Comprehensive test suite with 22 passing tests and 81% code coverage
- Proper error handling with appropriate HTTP status codes

## Tech Stack

- Flask 2.2.2 - Web framework
- Flask-SQLAlchemy 3.0.3 - ORM for database operations
- Flask-Migrate 4.0.0 - Database migration management
- Flask-JWT-Extended 4.5.2 - JWT token authentication
- Flask-Bcrypt 1.0.1 - Password hashing
- Marshmallow 3.20.1 - Data validation and serialization
- SQLite - Development database
- Pytest 7.2.0 - Testing framework
- Faker 15.3.2 - Sample data generation

## Project Structure
flask-c10-summative-lab-sessions-and-jwt-clients/
├── app/
│ ├── init.py # Flask app factory
│ ├── models.py # Database models (User, Note)
│ ├── schemas.py # Marshmallow validation schemas
│ └── routes/
│ ├── init.py
│ ├── auth.py # Authentication routes
│ └── notes.py # Notes CRUD routes
├── migrations/ # Database migration files
├── tests/ # Test suite
│ ├── init.py
│ ├── test_api.py # Comprehensive API tests
│ └── test_api_simple.py # Simple API tests
├── instance/ # Database file storage
├── app.py # Application entry point
├── config.py # Application configuration
├── seed.py # Database seeding script
├── requirements.txt # Python dependencies
├── Pipfile # Pipenv dependencies
├── pytest.ini # Pytest configuration
├── .gitignore # Git ignore file
└── README.md # Project documentation

text

## Installation

### Prerequisites

- Python 3.8 or higher
- Pipenv or pip
- Git

### Setup Instructions

1. Clone the repository

```bash
git clone https://github.com/roy9html/flask-c10-summative-lab-sessions-and-jwt-clients.git
cd flask-c10-summative-lab-sessions-and-jwt-clients
Create and activate virtual environment

bash
python -m venv venv38
source venv38/bin/activate  # On Windows: venv38\Scripts\activate
Install dependencies

Using pip:

bash
pip install -r requirements.txt
Or using Pipenv:

bash
pipenv install
pipenv shell
Set up environment variables

bash
export FLASK_APP=app.py
export FLASK_ENV=development
Initialize database

bash
flask db init
flask db migrate -m "Initial migration"
flask db upgrade
Seed the database with sample data

bash
python seed.py
Run the application

bash
python app.py
The API will be available at http://localhost:5000

Running the Application
Development Mode
bash
python app.py
Production Mode (with Gunicorn)
bash
gunicorn app:app
API Endpoints
Authentication Endpoints
Method	Endpoint	Description	Authentication
POST	/auth/signup	Register a new user	None
POST	/auth/login	Login and get JWT tokens	None
POST	/auth/refresh	Refresh access token	Refresh token required
GET	/auth/me	Get current user information	Access token required
POST	/auth/logout	Logout user	Access token required
Notes Endpoints (Requires Authentication)
Method	Endpoint	Description	Query Parameters
GET	/api/notes	Get all notes for current user	page (default: 1), per_page (default: 10, max: 100)
POST	/api/notes	Create a new note	None
GET	/api/notes/<id>	Get a specific note by ID	None
PUT	/api/notes/<id>	Update a note by ID	None
DELETE	/api/notes/<id>	Delete a note by ID	None
PUT	/api/notes/archive/<id>	Toggle archive status	None
GET	/api/notes/categories	Get all categories used by user	None
API Usage Examples
1. Register a New User
Request:

bash
curl -X POST http://localhost:5000/auth/signup \
  -H "Content-Type: application/json" \
  -d '{
    "username": "john_doe",
    "email": "john@example.com",
    "password": "securepassword123"
  }'
Response:

json
{
  "user": {
    "id": 1,
    "username": "john_doe",
    "email": "john@example.com",
    "created_at": "2024-01-15T10:30:00"
  },
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
}
2. Login
Request:

bash
curl -X POST http://localhost:5000/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "username": "john_doe",
    "password": "securepassword123"
  }'
Response:

json
{
  "user": {
    "id": 1,
    "username": "john_doe",
    "email": "john@example.com"
  },
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
}
3. Get Current User Info
Request:

bash
curl -X GET http://localhost:5000/auth/me \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
Response:

json
{
  "id": 1,
  "username": "john_doe",
  "email": "john@example.com",
  "created_at": "2024-01-15T10:30:00"
}
4. Create a Note
Request:

bash
curl -X POST http://localhost:5000/api/notes \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "My First Note",
    "content": "This is the content of my first note.",
    "category": "Personal"
  }'
Response:

json
{
  "id": 1,
  "title": "My First Note",
  "content": "This is the content of my first note.",
  "category": "Personal",
  "is_archived": false,
  "created_at": "2024-01-15T10:35:00",
  "updated_at": "2024-01-15T10:35:00",
  "user_id": 1
}
5. Get All Notes with Pagination
Request:

bash
curl -X GET "http://localhost:5000/api/notes?page=1&per_page=5" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
Response:

json
{
  "notes": [
    {
      "id": 1,
      "title": "My First Note",
      "content": "This is the content of my first note.",
      "category": "Personal",
      "is_archived": false,
      "created_at": "2024-01-15T10:35:00",
      "updated_at": "2024-01-15T10:35:00",
      "user_id": 1
    }
  ],
  "pagination": {
    "page": 1,
    "per_page": 5,
    "total": 10,
    "pages": 2,
    "has_prev": false,
    "has_next": true
  }
}
6. Update a Note
Request:

bash
curl -X PUT http://localhost:5000/api/notes/1 \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Updated Note Title",
    "content": "Updated content"
  }'
Response:

json
{
  "id": 1,
  "title": "Updated Note Title",
  "content": "Updated content",
  "category": "Personal",
  "is_archived": false,
  "created_at": "2024-01-15T10:35:00",
  "updated_at": "2024-01-15T10:40:00",
  "user_id": 1
}
7. Archive a Note
Request:

bash
curl -X PUT http://localhost:5000/api/notes/archive/1 \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
Response:

json
{
  "id": 1,
  "title": "Updated Note Title",
  "content": "Updated content",
  "category": "Personal",
  "is_archived": true,
  "created_at": "2024-01-15T10:35:00",
  "updated_at": "2024-01-15T10:40:00",
  "user_id": 1
}
8. Delete a Note
Request:

bash
curl -X DELETE http://localhost:5000/api/notes/1 \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
Response:

json
{
  "message": "Note deleted successfully"
}
9. Get All Categories
Request:

bash
curl -X GET http://localhost:5000/api/notes/categories \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
Response:

json
{
  "categories": ["Personal", "Work", "Study", "Ideas"]
}
Testing
Run All Tests
bash
python -m pytest tests/ -v
Run Tests with Coverage Report
bash
python -m pytest tests/ -v --cov=app --cov-report=term
Run Specific Test File
bash
python -m pytest tests/test_api.py -v
Run Specific Test Function
bash
python -m pytest tests/test_api.py::test_login_success -v
Test Results
text
22 passed, 4 warnings in 11.80s
Coverage: 81%
Database Seeding
The seed script creates sample data for testing:

bash
python seed.py
What gets created:

5 users with unique usernames and emails

10 notes per user with random categories

Test users with password: password123

Sample Users:

sheltonwanda@example.net

bartlettbryan@example.net

lisawood@example.net

woodconnie@example.net

sedwards@example.net

Error Handling
The API returns appropriate HTTP status codes and error messages:

Status Code	Description
200	Success (GET, PUT, DELETE)
201	Created (POST)
400	Bad Request (validation error)
401	Unauthorized (missing or invalid token)
403	Forbidden (insufficient permissions)
404	Not Found (resource doesn't exist)
500	Internal Server Error
Error Response Format
json
{
  "error": "Error message description",
  "errors": {
    "field_name": ["Validation error message"]
  }
}
Development
Running Migrations
bash
# Create a new migration
flask db migrate -m "Description of changes"

# Apply migrations
flask db upgrade

# Rollback migration
flask db downgrade
Adding New Models
Add model class to app/models.py

Create migration: flask db migrate -m "Added new model"

Apply migration: flask db upgrade

Adding New Routes
Create new route file in app/routes/

Register blueprint in app/init.py

Add tests in tests/

Security Features
Password Hashing: Passwords are hashed using Bcrypt before storage

JWT Tokens: Access tokens expire after 1 hour, refresh tokens after 30 days

User Isolation: Users can only access their own data through foreign key constraints

Input Validation: All inputs are validated using Marshmallow schemas

Protected Routes: All sensitive endpoints require authentication

CORS: Cross-Origin Resource Sharing configured for security

Environment Variables: Sensitive configuration stored in environment variables