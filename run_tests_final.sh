#!/bin/bash

echo "=========================================="
echo "  Running Flask API Tests"
echo "=========================================="

# Ensure we're in the virtual environment
source venv38/bin/activate

# Set Flask app
export FLASK_APP=app.py

# Create instance directory
mkdir -p instance
chmod 755 instance

# Run tests with pytest
python -m pytest tests/test_api.py -v --tb=short --maxfail=5

# Check exit code
if [ $? -eq 0 ]; then
    echo ""
    echo "=========================================="
    echo "  All Tests Passed! ✅"
    echo "=========================================="
else
    echo ""
    echo "=========================================="
    echo "  Some Tests Failed! ❌"
    echo "=========================================="
    echo ""
    echo "To run a specific test:"
    echo "  python -m pytest tests/test_api.py::test_signup_success -v"
    echo ""
    echo "To run with coverage:"
    echo "  python -m pytest tests/test_api.py -v --cov=app --cov-report=term"
fi
