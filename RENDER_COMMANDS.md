# Render Deployment - Quick Commands Reference

## Build Command (Copy & Paste)
```
pip install -r requirements.txt && python manage.py migrate && python manage.py collectstatic --noinput
```

## Start Command (Copy & Paste)
```
gunicorn project_name.wsgi:application --bind 0.0.0.0:$PORT
```

## Environment Variables to Set

| Variable | Value | Example |
|----------|-------|---------|
| `DEBUG` | `False` | `False` |
| `SECRET_KEY` | Generate strong key | `django-insecure-abc123...` |
| `ALLOWED_HOSTS` | Your domain | `hireconnect-backend.onrender.com,localhost` |
| `DATABASE_URL` | PostgreSQL URL | `postgresql://user:pass@host:5432/db` |
| `CORS_ALLOWED_ORIGINS` | Frontend URL | `https://hireconnect-frontend.onrender.com` |

## Generate SECRET_KEY Locally
```bash
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

## Local Testing Steps
```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Create .env file
cp .env.example .env

# 3. Run migrations
python manage.py migrate

# 4. Collect static files
python manage.py collectstatic --noinput

# 5. Test with Gunicorn
gunicorn project_name.wsgi:application --bind 0.0.0.0:8000
```

## Push to GitHub
```bash
git add .
git commit -m "Prepare for Render deployment"
git push origin main
```

## Render Deployment Steps
1. Go to https://render.com
2. Click "New +" → "Web Service"
3. Connect your GitHub repository
4. Fill in:
   - Name: `hireconnect-backend`
   - Environment: Python 3
   - Build Command: (see above)
   - Start Command: (see above)
5. Add Environment Variables (see table above)
6. Click "Create Web Service"
7. Wait for deployment to complete
8. Your app will be at: `https://hireconnect-backend.onrender.com`

## After Deployment
- Test API endpoints
- Check logs for errors
- Update frontend CORS settings if needed
- Monitor application performance
