import pytest
import os
import sys
from app import create_app, db
from app.models import User, Note

# Use a simple file-based database
TEST_DB_PATH = os.path.join(os.getcwd(), 'instance', 'test_simple.db')

@pytest.fixture(scope='function')
def client():
    """Create a test client"""
    # Ensure instance directory exists
    os.makedirs(os.path.dirname(TEST_DB_PATH), exist_ok=True)
    
    # Remove old test database if exists
    if os.path.exists(TEST_DB_PATH):
        os.remove(TEST_DB_PATH)
    
    app = create_app()
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{TEST_DB_PATH}'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    # Create tables and test user
    with app.app_context():
        db.create_all()
        user = User(
            username='testuser',
            email='test@example.com'
        )
        user.set_password('password123')
        db.session.add(user)
        db.session.commit()
    
    with app.test_client() as client:
        yield client
    
    # Cleanup
    with app.app_context():
        db.drop_all()
    if os.path.exists(TEST_DB_PATH):
        os.remove(TEST_DB_PATH)

def test_basic(client):
    """Basic test to verify everything works"""
    response = client.get('/auth/me')
    assert response.status_code == 401  # Unauthorized

def test_signup(client):
    """Test signup endpoint"""
    response = client.post('/auth/signup', json={
        'username': 'newuser',
        'email': 'new@example.com',
        'password': 'password123'
    })
    assert response.status_code == 201
    assert 'access_token' in response.json

def test_login(client):
    """Test login endpoint"""
    response = client.post('/auth/login', json={
        'username': 'testuser',
        'password': 'password123'
    })
    assert response.status_code == 200
    assert 'access_token' in response.json

def test_me_endpoint(client):
    """Test me endpoint"""
    # Login first
    login = client.post('/auth/login', json={
        'username': 'testuser',
        'password': 'password123'
    })
    token = login.json.get('access_token')
    
    # Test me endpoint
    response = client.get('/auth/me', headers={
        'Authorization': f'Bearer {token}'
    })
    assert response.status_code == 200
    assert response.json['username'] == 'testuser'

def test_create_note(client):
    """Test creating a note"""
    # Login
    login = client.post('/auth/login', json={
        'username': 'testuser',
        'password': 'password123'
    })
    token = login.json.get('access_token')
    
    # Create note
    response = client.post('/api/notes',
        headers={'Authorization': f'Bearer {token}'},
        json={
            'title': 'Test Note',
            'content': 'This is a test note',
            'category': 'Test'
        }
    )
    assert response.status_code == 201
    assert response.json['title'] == 'Test Note'

def test_get_notes(client):
    """Test getting notes with pagination"""
    # Login
    login = client.post('/auth/login', json={
        'username': 'testuser',
        'password': 'password123'
    })
    token = login.json.get('access_token')
    
    # Create some notes
    for i in range(3):
        client.post('/api/notes',
            headers={'Authorization': f'Bearer {token}'},
            json={
                'title': f'Note {i}',
                'content': f'Content {i}',
                'category': 'Test'
            }
        )
    
    # Get notes
    response = client.get('/api/notes?page=1&per_page=2',
        headers={'Authorization': f'Bearer {token}'}
    )
    assert response.status_code == 200
    assert 'notes' in response.json
    assert 'pagination' in response.json
    assert len(response.json['notes']) == 2
