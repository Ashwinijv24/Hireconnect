#!/bin/bash

# HireConnect Backend Startup Script

echo "================================"
echo "HireConnect Backend Startup"
echo "================================"

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python -m venv venv
fi

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Install dependencies
echo "Installing dependencies..."
pip install -r requirements.txt

# Run migrations
echo "Running migrations..."
python manage.py migrate

# Create superuser if needed
echo "Checking for superuser..."
python manage.py shell << END
from django.contrib.auth import get_user_model
User = get_user_model()
if not User.objects.filter(username='admin').exists():
    print("Creating superuser...")
    User.objects.create_superuser('admin', 'admin@example.com', 'admin123')
    print("Superuser created: admin / admin123")
else:
    print("Superuser already exists")
END

# Start server
echo ""
echo "================================"
echo "Starting Django development server..."
echo "Backend will be available at: http://localhost:8000"
echo "Admin panel at: http://localhost:8000/admin"
echo "================================"
echo ""

python manage.py runserver
