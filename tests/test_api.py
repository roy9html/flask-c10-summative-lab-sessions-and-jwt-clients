import pytest
import os
from app import create_app, db
from app.models import User, Note

@pytest.fixture
def client():
    """Create a test client for the app"""
    # Use an absolute path for the test database
    base_dir = os.path.abspath(os.path.dirname(__file__))
    instance_dir = os.path.join(os.path.dirname(base_dir), 'instance')
    db_path = os.path.join(instance_dir, 'test.db')
    
    # Ensure instance directory exists
    os.makedirs(instance_dir, exist_ok=True)
    
    app = create_app()
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_path}'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    with app.app_context():
        db.create_all()
        # Create test user
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
    if os.path.exists(db_path):
        os.remove(db_path)

def get_token(client, username='testuser', password='password123'):
    """Helper function to get auth token"""
    response = client.post('/auth/login', json={
        'username': username,
        'password': password
    })
    if response.status_code == 200:
        return response.json.get('access_token')
    return None

# ==================== AUTH TESTS ====================

def test_signup_success(client):
    """Test successful user registration"""
    response = client.post('/auth/signup', json={
        'username': 'newuser',
        'email': 'new@example.com',
        'password': 'password123'
    })
    assert response.status_code == 201
    assert 'access_token' in response.json
    assert response.json['user']['username'] == 'newuser'

def test_signup_duplicate_username(client):
    """Test signup with duplicate username"""
    response = client.post('/auth/signup', json={
        'username': 'testuser',
        'email': 'test2@example.com',
        'password': 'password123'
    })
    assert response.status_code == 400
    assert 'error' in response.json

def test_login_success(client):
    """Test successful login"""
    response = client.post('/auth/login', json={
        'username': 'testuser',
        'password': 'password123'
    })
    assert response.status_code == 200
    assert 'access_token' in response.json
    assert 'refresh_token' in response.json

def test_login_failure_wrong_password(client):
    """Test login with wrong password"""
    response = client.post('/auth/login', json={
        'username': 'testuser',
        'password': 'wrongpassword'
    })
    assert response.status_code == 401
    assert 'error' in response.json

def test_me_endpoint(client):
    """Test getting current user info"""
    token = get_token(client)
    if not token:
        pytest.skip("Login failed")
    response = client.get('/auth/me', headers={
        'Authorization': f'Bearer {token}'
    })
    assert response.status_code == 200
    assert response.json['username'] == 'testuser'

def test_me_endpoint_unauthorized(client):
    """Test me endpoint without token"""
    response = client.get('/auth/me')
    assert response.status_code == 401

# ==================== NOTES TESTS ====================

def test_create_note(client):
    """Test creating a note"""
    token = get_token(client)
    if not token:
        pytest.skip("Login failed")
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

def test_create_note_unauthorized(client):
    """Test creating note without token"""
    response = client.post('/api/notes', json={
        'title': 'Test Note',
        'content': 'Test content'
    })
    assert response.status_code == 401

def test_get_notes(client):
    """Test getting all notes with pagination"""
    token = get_token(client)
    if not token:
        pytest.skip("Login failed")
    
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
    
    response = client.get('/api/notes?page=1&per_page=2',
        headers={'Authorization': f'Bearer {token}'}
    )
    assert response.status_code == 200
    assert 'notes' in response.json
    assert 'pagination' in response.json
    assert len(response.json['notes']) == 2

def test_get_single_note(client):
    """Test getting a single note by ID"""
    token = get_token(client)
    if not token:
        pytest.skip("Login failed")
    
    # Create a note
    create_response = client.post('/api/notes',
        headers={'Authorization': f'Bearer {token}'},
        json={
            'title': 'Single Note',
            'content': 'Single content',
            'category': 'Test'
        }
    )
    note_id = create_response.json['id']
    
    # Get the note
    response = client.get(f'/api/notes/{note_id}',
        headers={'Authorization': f'Bearer {token}'}
    )
    assert response.status_code == 200
    assert response.json['title'] == 'Single Note'

def test_get_note_not_found(client):
    """Test getting a note that doesn't exist"""
    token = get_token(client)
    if not token:
        pytest.skip("Login failed")
    response = client.get('/api/notes/9999',
        headers={'Authorization': f'Bearer {token}'}
    )
    assert response.status_code == 404

def test_update_note(client):
    """Test updating a note"""
    token = get_token(client)
    if not token:
        pytest.skip("Login failed")
    
    # Create a note
    create_response = client.post('/api/notes',
        headers={'Authorization': f'Bearer {token}'},
        json={
            'title': 'Original Title',
            'content': 'Original content',
            'category': 'Test'
        }
    )
    note_id = create_response.json['id']
    
    # Update the note
    response = client.put(f'/api/notes/{note_id}',
        headers={'Authorization': f'Bearer {token}'},
        json={
            'title': 'Updated Title',
            'content': 'Updated content'
        }
    )
    assert response.status_code == 200
    assert response.json['title'] == 'Updated Title'

def test_delete_note(client):
    """Test deleting a note"""
    token = get_token(client)
    if not token:
        pytest.skip("Login failed")
    
    # Create a note
    create_response = client.post('/api/notes',
        headers={'Authorization': f'Bearer {token}'},
        json={
            'title': 'To Delete',
            'content': 'Delete me',
            'category': 'Test'
        }
    )
    note_id = create_response.json['id']
    
    # Delete the note
    response = client.delete(f'/api/notes/{note_id}',
        headers={'Authorization': f'Bearer {token}'}
    )
    assert response.status_code == 200
    assert response.json['message'] == 'Note deleted successfully'

def test_archive_note(client):
    """Test archiving a note"""
    token = get_token(client)
    if not token:
        pytest.skip("Login failed")
    
    # Create a note
    create_response = client.post('/api/notes',
        headers={'Authorization': f'Bearer {token}'},
        json={
            'title': 'Archive Me',
            'content': 'Archive content',
            'category': 'Test'
        }
    )
    note_id = create_response.json['id']
    
    # Archive the note
    response = client.put(f'/api/notes/archive/{note_id}',
        headers={'Authorization': f'Bearer {token}'}
    )
    assert response.status_code == 200
    assert response.json['is_archived'] == True

def test_get_categories(client):
    """Test getting categories"""
    token = get_token(client)
    if not token:
        pytest.skip("Login failed")
    
    # Create notes with different categories
    categories = ['Work', 'Personal', 'Study']
    for category in categories:
        client.post('/api/notes',
            headers={'Authorization': f'Bearer {token}'},
            json={
                'title': f'Note in {category}',
                'content': f'Content for {category}',
                'category': category
            }
        )
    
    response = client.get('/api/notes/categories',
        headers={'Authorization': f'Bearer {token}'}
    )
    assert response.status_code == 200
    assert 'categories' in response.json

# ==================== ACCESS CONTROL TESTS ====================

def test_user_cannot_access_other_users_note(client):
    """Test that a user cannot access another user's note"""
    # Create first user
    client.post('/auth/signup', json={
        'username': 'user1',
        'email': 'user1@example.com',
        'password': 'password123'
    })
    
    # Login as user1
    token1 = get_token(client, 'user1')
    if not token1:
        pytest.skip("Login failed")
    
    # Create note as user1
    create_response = client.post('/api/notes',
        headers={'Authorization': f'Bearer {token1}'},
        json={
            'title': 'User1 Note',
            'content': 'User1 content',
            'category': 'Test'
        }
    )
    note_id = create_response.json['id']
    
    # Create and login as user2
    client.post('/auth/signup', json={
        'username': 'user2',
        'email': 'user2@example.com',
        'password': 'password123'
    })
    token2 = get_token(client, 'user2')
    if not token2:
        pytest.skip("Login failed")
    
    # Try to access user1's note as user2
    response = client.get(f'/api/notes/{note_id}',
        headers={'Authorization': f'Bearer {token2}'}
    )
    assert response.status_code == 404
