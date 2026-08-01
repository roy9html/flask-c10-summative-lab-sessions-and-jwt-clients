#!/bin/bash

echo "=========================================="
echo "  Running Flask API Tests"
echo "=========================================="

# Ensure we're in the virtual environment
source venv38/bin/activate

# Set Flask app
export FLASK_APP=app.py

# Ensure instance directory exists
mkdir -p instance
chmod 755 instance

# Run tests with pytest
python -m pytest tests/test_api.py -v --tb=short --maxfail=5

# Run with coverage (optional)
# python -m pytest tests/test_api.py -v --cov=app --cov-report=term --cov-report=html

echo ""
echo "=========================================="
echo "  Tests Complete!"
echo "=========================================="
