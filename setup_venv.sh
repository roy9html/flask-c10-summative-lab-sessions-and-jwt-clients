#!/bin/bash

echo "=========================================="
echo "  Setting up Virtual Environment"
echo "=========================================="

# 1. Set Python 3.8
echo "Setting Python 3.8..."
pyenv shell 3.8.13
python --version

# 2. Remove old venv
echo "Removing old virtual environments..."
rm -rf venv38 venv .venv

# 3. Create new venv
echo "Creating virtual environment..."
python -m venv venv38

# 4. Activate venv
echo "Activating virtual environment..."
source venv38/bin/activate

# 5. Verify venv
echo "Virtual environment path: $(which python)"

# 6. Upgrade pip
echo "Upgrading pip..."
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
pip install pytest==7.2.0
pip install pytest-cov==4.0.0

# 8. Verify installations
echo ""
echo "Installed packages:"
pip list | grep -E "flask|pytest|faker|marshmallow"

# 9. Create config.py if missing
if [ ! -f config.py ]; then
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
