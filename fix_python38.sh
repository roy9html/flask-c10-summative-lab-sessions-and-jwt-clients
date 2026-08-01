#!/bin/bash

echo "=========================================="
echo "  Fixing Python 3.8 Environment"
echo "=========================================="

# 1. Switch to Python 3.8
echo "Switching to Python 3.8..."
pyenv shell 3.8.13

# 2. Verify Python version
python --version

# 3. Remove old venv if exists
rm -rf venv38

# 4. Create new venv with Python 3.8
echo "Creating virtual environment with Python 3.8..."
python -m venv venv38

# 5. Activate venv
source venv38/bin/activate

# 6. Upgrade pip
pip install --upgrade pip

# 7. Install packages
echo "Installing packages..."
pip install flask==2.2.2
pip install werkzeug==2.2.2
pip install flask-sqlalchemy==3.0.3
pip install flask-migrate==4.0.0
pip install flask-bcrypt==1.0.1
pip install flask-jwt-extended==4.5.2
pip install flask-cors==3.0.10
pip install marshmallow==3.20.1
pip install faker==15.3.2
pip install python-dotenv==0.21.0

# 8. Create config.py
echo "Creating config.py..."
cat > config.py << 'EOF'
import os
from datetime import timedelta

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-in-production'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///instance/app.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY') or 'jwt-secret-key-change-in-production'
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=1)
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(days=30)
