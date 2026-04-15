@echo off
REM HireConnect Backend Startup Script for Windows

echo ================================
echo HireConnect Backend Startup
echo ================================

REM Check if virtual environment exists
if not exist "venv" (
    echo Creating virtual environment...
    python -m venv venv
)

REM Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate.bat

REM Install dependencies
echo Installing dependencies...
pip install -r requirements.txt

REM Run migrations
echo Running migrations...
python manage.py migrate

REM Create superuser if needed
echo Checking for superuser...
python manage.py shell << EOF
from django.contrib.auth import get_user_model
User = get_user_model()
if not User.objects.filter(username='admin').exists():
    print("Creating superuser...")
    User.objects.create_superuser('admin', 'admin@example.com', 'admin123')
    print("Superuser created: admin / admin123")
else:
    print("Superuser already exists")
EOF

REM Start server
echo.
echo ================================
echo Starting Django development server...
echo Backend will be available at: http://localhost:8000
echo Admin panel at: http://localhost:8000/admin
echo ================================
echo.

python manage.py runserver
