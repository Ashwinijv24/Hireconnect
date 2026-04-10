# Render Deployment Guide for Hireconnect

## Prerequisites
- GitHub account with your repo pushed
- Render account (https://render.com)
- PostgreSQL database (Render provides this)

## Step-by-Step Deployment

### 1. Prepare Your Repository
```bash
# Make sure all changes are committed
git add .
git commit -m "Prepare for Render deployment"
git push origin main
```

### 2. Create a Render Account
- Go to https://render.com
- Sign up with GitHub
- Authorize Render to access your repositories

### 3. Create a PostgreSQL Database
1. Go to Dashboard → New +
2. Select "PostgreSQL"
3. Name: `hireconnect-db`
4. Region: Choose closest to you
5. Click "Create Database"
6. Copy the Internal Database URL (you'll need this)

### 4. Deploy the Web Service
1. Go to Dashboard → New +
2. Select "Web Service"
3. Connect your GitHub repository
4. Fill in the details:
   - **Name**: `hireconnect-backend`
   - **Environment**: Python 3
   - **Build Command**: 
     ```
     pip install -r requirements.txt && python manage.py migrate && python manage.py collectstatic --noinput
     ```
   - **Start Command**: 
     ```
     gunicorn project_name.wsgi:application --bind 0.0.0.0:$PORT
     ```
   - **Plan**: Free (or paid if needed)

### 5. Set Environment Variables
In the Web Service settings, add these environment variables:

```
DEBUG=False
SECRET_KEY=<generate-a-strong-secret-key>
ALLOWED_HOSTS=<your-app-name>.onrender.com,localhost
DATABASE_URL=<paste-the-internal-database-url-from-step-3>
CORS_ALLOWED_ORIGINS=https://<your-frontend-url>.onrender.com,http://localhost:3000
```

To generate a SECRET_KEY, run:
```bash
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

### 6. Deploy
1. Click "Create Web Service"
2. Render will automatically start building and deploying
3. Monitor the logs in the "Logs" tab
4. Once deployed, your app will be available at: `https://<your-app-name>.onrender.com`

## Build and Start Commands Explained

### Build Command
```bash
pip install -r requirements.txt && python manage.py migrate && python manage.py collectstatic --noinput
```
- Installs all Python dependencies
- Runs database migrations
- Collects static files (CSS, JS, images)

### Start Command
```bash
gunicorn project_name.wsgi:application --bind 0.0.0.0:$PORT
```
- Starts the Gunicorn WSGI server
- Binds to all network interfaces (0.0.0.0)
- Uses the PORT environment variable provided by Render

## Local Testing Before Deployment

### 1. Install dependencies
```bash
pip install -r requirements.txt
```

### 2. Create .env file
```bash
cp .env.example .env
# Edit .env with your local settings
```

### 3. Run migrations
```bash
python manage.py migrate
```

### 4. Collect static files
```bash
python manage.py collectstatic --noinput
```

### 5. Test with Gunicorn locally
```bash
gunicorn project_name.wsgi:application --bind 0.0.0.0:8000
```

## Troubleshooting

### Build Fails
- Check the build logs in Render dashboard
- Ensure all dependencies are in requirements.txt
- Verify Python version compatibility

### Database Connection Error
- Verify DATABASE_URL is correct
- Check if database is running
- Ensure migrations have run

### Static Files Not Loading
- Run `python manage.py collectstatic --noinput`
- Check STATIC_ROOT and STATIC_URL settings
- Verify WhiteNoise middleware is installed

### CORS Errors
- Add your frontend URL to CORS_ALLOWED_ORIGINS
- Format: `https://your-frontend-domain.com`

## Useful Commands

### View Logs
```bash
# In Render dashboard, go to Logs tab
```

### SSH into Container
```bash
# Available in Render dashboard for paid plans
```

### Redeploy
```bash
# Push changes to GitHub
git push origin main
# Render will automatically redeploy
```

## Security Checklist
- [ ] DEBUG is set to False
- [ ] SECRET_KEY is strong and unique
- [ ] ALLOWED_HOSTS includes your domain
- [ ] Database credentials are in environment variables
- [ ] CORS_ALLOWED_ORIGINS is restricted to your frontend
- [ ] .env file is in .gitignore
- [ ] No sensitive data in code

## Next Steps
1. Deploy frontend to Render or Vercel
2. Update CORS_ALLOWED_ORIGINS with frontend URL
3. Set up custom domain (optional)
4. Configure email service for notifications
5. Set up monitoring and error tracking
