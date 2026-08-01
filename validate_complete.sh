#!/bin/bash

echo "=========================================="
echo "  COMPLETE PROJECT VALIDATION"
echo "=========================================="

# 1. Check endpoints
echo -e "\n[1] API Endpoints:"
python -c "
from app import create_app
app = create_app()
for rule in app.url_map.iter_rules():
    methods = ', '.join(rule.methods - {'HEAD', 'OPTIONS'})
    print(f'  {methods:20} {rule.rule}')
"

# 2. Check models
echo -e "\n[2] Models:"
python -c "
from app.models import User, Note
print('  User model: OK')
print('  Note model: OK')
print('  Relationships: User -> Note (one-to-many)')
"

# 3. Check database
echo -e "\n[3] Database:"
sqlite3 instance/app.db "SELECT name FROM sqlite_master WHERE type='table';" | while read table; do
    count=$(sqlite3 instance/app.db "SELECT COUNT(*) FROM $table;")
    echo "  $table: $count rows"
done

# 4. Check seed data
echo -e "\n[4] Seed Data:"
echo "  Users:"
sqlite3 instance/app.db "SELECT id, username, email FROM users LIMIT 3;" | while IFS='|' read id username email; do
    echo "    $id. $username ($email)"
done
echo "  ...and more"

# 5. Check tests
echo -e "\n[5] Tests:"
if [ -d "tests" ]; then
    test_count=$(ls tests/*.py 2>/dev/null | wc -l)
    echo "  Test files: $test_count"
    python -m pytest tests/ -v --tb=no 2>&1 | tail -3
else
    echo "  No tests directory found"
fi

# 6. Check files
echo -e "\n[6] Required Files:"
for file in app.py config.py seed.py README.md Pipfile .gitignore; do
    if [ -f "$file" ]; then
        echo "  [OK] $file"
    else
        echo "  [MISSING] $file"
    fi
done

# 7. Check Git
echo -e "\n[7] Git Workflow:"
echo "  Current branch: $(git branch --show-current)"
echo "  Branches:"
git branch -a | head -8

echo -e "\n=========================================="
echo "  VALIDATION COMPLETE"
echo "=========================================="
