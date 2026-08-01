import pytest
from app import create_app, db
from app.models import User
import tempfile
import os

@pytest.fixture
def app():
    db_fd, db_path = tempfile.mkstemp(suffix='.db')
    app = create_app()
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_path}'
    
    with app.app_context():
        db.create_all()
        yield app
    
    os.close(db_fd)
    os.unlink(db_path)

def test_app_creation(app):
    assert app is not None
    
def test_db_connection(app):
    with app.app_context():
        user = User(username='test', email='test@test.com')
        user.set_password('password')
        db.session.add(user)
        db.session.commit()
        assert User.query.count() == 1
