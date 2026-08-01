# Flask Notes API with JWT Authentication

A secure RESTful Flask API for managing personal notes with JWT authentication.

## Installation
```bash
pipenv install
pipenv shell
flask db upgrade
python seed.py
python app.py
```

## API Endpoints
- POST /auth/signup - Register
- POST /auth/login - Login
- GET /auth/me - Get user info
- GET /api/notes - Get notes
- POST /api/notes - Create note
- GET /api/notes/<id> - Get note
- PUT /api/notes/<id> - Update note
- DELETE /api/notes/<id> - Delete note

## License
MIT
