#!/bin/bash

echo "=========================================="
echo "  Setting Up Database"
echo "=========================================="

# 1. Set Flask app
export FLASK_APP=app.py

# 2. Create instance directory
mkdir -p instance
chmod 755 instance

# 3. Initialize migrations
echo "Initializing migrations..."
flask db init 2>/dev/null || echo "Migrations already initialized"

# 4. Create migration
echo "Creating migration..."
flask db migrate -m "Initial migration" 2>/dev/null || echo "Migration already exists"

# 5. Apply migration
echo "Applying migration..."
flask db upgrade

# 6. Seed database
echo "Seeding database..."
python seed.py

# 7. Verify
echo ""
echo "Database tables:"
sqlite3 instance/app.db ".tables"

echo ""
echo "Users:"
sqlite3 instance/app.db "SELECT id, username, email FROM users;"

echo ""
echo "Notes count per user:"
sqlite3 instance/app.db "SELECT user_id, COUNT(*) FROM notes GROUP BY user_id;"

echo ""
echo "=========================================="
echo "  Database Setup Complete!"
echo "=========================================="
echo ""
echo "To run the app: python app.py"
