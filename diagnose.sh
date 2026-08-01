#!/bin/bash

echo "=========================================="
echo "  PROJECT DIAGNOSIS"
echo "=========================================="

# 1. Project Structure
echo -e "\n[1] PROJECT STRUCTURE"
echo "Working directory: $(pwd)"

echo -e "\nRequired files:"
for file in app.py config.py seed.py Pipfile README.md; do
    if [ -f "$file" ]; then
        echo "  [OK] $file"
    else
        echo "  [MISSING] $file"
    fi
done

echo -e "\nApp files:"
for file in app/__init__.py app/models.py app/schemas.py; do
    if [ -f "$file" ]; then
        echo "  [OK] $file"
    else
        echo "  [MISSING] $file"
    fi
done

echo -e "\nRoute files:"
for file in app/routes/__init__.py app/routes/auth.py app/routes/notes.py; do
    if [ -f "$file" ]; then
        echo "  [OK] $file"
    else
        echo "  [MISSING] $file"
    fi
done

# 2. Python Environment
echo -e "\n[2] PYTHON ENVIRONMENT"
echo "Python: $(python --version 2>&1)"
echo "Virtual env: ${VIRTUAL_ENV:-Not active}"

echo -e "\nPackages:"
for pkg in flask flask-sqlalchemy flask-migrate flask-jwt-extended pytest faker; do
    if pip show $pkg > /dev/null 2>&1; then
        echo "  [OK] $pkg"
    else
        echo "  [MISSING] $pkg"
    fi
done

# 3. Database
echo -e "\n[3] DATABASE"
if [ -d "instance" ]; then
    echo "  [OK] instance directory exists"
    ls -la instance/ 2>/dev/null
else
    echo "  [MISSING] instance directory"
fi

# 4. Test Database Connection
echo -e "\n[4] DATABASE CONNECTION"
python -c "
from app import create_app, db
app = create_app()
with app.app_context():
    try:
        db.create_all()
        print('  Database connection: OK')
        from sqlalchemy import inspect
        inspector = inspect(db.engine)
        tables = inspector.get_table_names()
        print(f'  Tables: {tables}')
    except Exception as e:
        print(f'  Database error: {e}')
" 2>&1

# 5. Flask App
echo -e "\n[5] FLASK APP"
python -c "
from app import create_app
try:
    app = create_app()
    print('  Flask app: OK')
    print('  Routes:')
    for rule in app.url_map.iter_rules():
        methods = ', '.join(rule.methods - {'HEAD', 'OPTIONS'})
        print(f'    {rule.rule} ({methods})')
except Exception as e:
    print(f'  Flask app error: {e}')
" 2>&1 | head -20

# 6. Git Status
echo -e "\n[6] GIT STATUS"
echo "Current branch: $(git branch --show-current 2>/dev/null || echo 'Not a git repo')"
echo "Branches:"
git branch -a 2>/dev/null | head -10

# 7. Summary
echo -e "\n[7] SUMMARY"
echo "Project status:"

if [ -f "app.py" ] && [ -f "config.py" ] && [ -d "app" ]; then
    echo "  [OK] Flask application structure is present"
else
    echo "  [INCOMPLETE] Flask application structure"
fi

if [ -f "Pipfile" ]; then
    echo "  [OK] Pipfile exists"
else
    echo "  [MISSING] Pipfile"
fi

if [ -f "README.md" ]; then
    echo "  [OK] README.md exists"
else
    echo "  [MISSING] README.md"
fi

if [ -d "tests" ]; then
    echo "  [OK] Tests directory exists"
else
    echo "  [WARNING] No tests directory"
fi

echo -e "\n=========================================="
echo "  DIAGNOSIS COMPLETE"
echo "=========================================="
