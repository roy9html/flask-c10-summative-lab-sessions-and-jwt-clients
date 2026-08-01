
# Flask Notes API with JWT Authentication

## Project Description

A secure RESTful Flask API for managing personal notes with JWT-based authentication and full CRUD operations. Users can create, read, update, and delete their own notes with pagination support. The API ensures that users can only access and modify their own data, providing robust security and data isolation.

## Features

- JWT-based authentication (signup, login, refresh token)
- Full CRUD operations for notes
- User-specific data isolation
- Pagination for notes listing
- Note categories and archiving
- Input validation with Marshmallow
- Database seeding with sample data
- Comprehensive test suite

## Tech Stack

- Flask 2.2.2
- Flask-SQLAlchemy 3.0.3
- Flask-Migrate 4.0.0
- Flask-JWT-Extended 4.5.2
- Flask-Bcrypt 1.0.1
- Marshmallow 3.20.1
- SQLite (development)
- Pytest 7.2.0

## Installation

### Prerequisites

- Python 3.8+
- Pipenv or pip
- Git

### Setup Instructions

```bash
# 1. Clone the repository
git clone https://github.com/roy9html/flask-c10-summative-lab-sessions-and-jwt-clients.git
cd flask-c10-summative-lab-sessions-and-jwt-clients

# 2. Create and activate virtual environment
python -m venv venv38
source venv38/bin/activate  # On Windows: venv38\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt
# OR if using Pipenv:
# pipenv install
# pipenv shell

# 4. Set up environment variables
export FLASK_APP=app.py
export FLASK_ENV=development

# 5. Initialize database
flask db init
flask db migrate -m "Initial migration"
flask db upgrade

# 6. Seed the database with sample data
python seed.py

# 7. Run the application
python app.py
Running the Application
bash
# Start the Flask development server
python app.py

# The API will be available at:
# http://localhost:5000
To run in production, use a production WSGI server like Gunicorn:

bash
gunicorn app:app
API Endpoints
Authentication Endpoints
Method	Endpoint	Description	Authentication
POST	/auth/signup	Register a new user	None
POST	/auth/login	Login and get JWT tokens	None
POST	/auth/refresh	Refresh access token	Refresh token required
GET	/auth/me	Get current user information	Access token required
POST	/auth/logout	Logout user (client discards token)	Access token required
Notes Endpoints (Requires Authentication)
Method	Endpoint	Description	Query Parameters
GET	/api/notes	Get all notes for current user	page (default: 1), per_page (default: 10, max: 100)
POST	/api/notes	Create a new note	None
GET	/api/notes/<id>	Get a specific note by ID	None
PUT	/api/notes/<id>	Update a note by ID	None
DELETE	/api/notes/<id>	Delete a note by ID	None
PUT	/api/notes/archive/<id>	Toggle archive status of a note	None
GET	/api/notes/categories	Get all categories used by user	None
API Usage Examples
1. Register a New User
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
5. Get All Notes (with Pagination)
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
bash
curl -X PUT http://localhost:5000/api/notes/1 \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Updated Note Title",
    "content": "Updated content"
  }'
7. Archive a Note
bash
curl -X PUT http://localhost:5000/api/notes/archive/1 \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
8. Delete a Note
bash
curl -X DELETE http://localhost:5000/api/notes/1 \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
9. Get All Categories
bash
curl -X GET http://localhost:5000/api/notes/categories \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
Response:

json
{
  "categories": ["Personal", "Work", "Study", "Ideas"]
}
Testing
bash
# Run all tests
python -m pytest tests/ -v

# Run tests with coverage report
python -m pytest tests/ -v --cov=app --cov-report=term

# Run specific test file
python -m pytest tests/test_api.py -v

# Run specific test function
python -m pytest tests/test_api.py::test_login_success -v
Database Seeding
bash
# Seed the database with sample data
python seed.py
The seed script creates:

5 users with unique usernames and emails

10 notes per user with random categories

Test users with password: password123

Error Handling
The API returns appropriate HTTP status codes:

Status Code	Description
200	Success
201	Created
400	Bad Request (validation error)
401	Unauthorized (missing or invalid token)
404	Not Found
500	Internal Server Error
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

Project Structure
text
flask-c10-summative-lab-sessions-and-jwt-clients/
├── app/
│   ├── __init__.py          # Flask app factory
│   ├── models.py            # Database models (User, Note)
│   ├── schemas.py           # Marshmallow schemas
│   └── routes/
│       ├── __init__.py
│       ├── auth.py          # Authentication routes
│       └── notes.py         # Notes CRUD routes
├── migrations/              # Database migrations
├── tests/                   # Test files
├── instance/                # Database file
├── app.py                   # Application entry point
├── config.py               # Configuration
├── seed.py                 # Database seeding script
├── requirements.txt        # Python dependencies
├── Pipfile                 # Pipenv dependencies
├── .gitignore              # Git ignore file
└── README.md              # Documentation
Security Features
Passwords hashed using Bcrypt

JWT tokens with expiration

User-specific data isolation

Input validation and sanitization

Protected routes requiring authentication

CORS support configured

License
MIT

Contributors
Brenden Nyaga

