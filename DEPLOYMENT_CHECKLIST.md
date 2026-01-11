# ✅ PythonAnywhere Deployment Checklist

Use this checklist to ensure you complete all steps for deployment.

## Pre-Deployment
- [ ] Created `requirements.txt` file
- [ ] Updated `settings.py` for production (environment variables)
- [ ] Committed code to Git (if using GitHub)
- [ ] Tested application locally

## PythonAnywhere Setup
- [ ] Created PythonAnywhere account
- [ ] Uploaded project (via Git or file upload)
- [ ] Created virtual environment
- [ ] Installed dependencies (`pip install -r requirements.txt`)

## Database Setup
- [ ] Ran migrations (`python manage.py migrate`)
- [ ] Created superuser (`python manage.py createsuperuser`)
- [ ] Verified database file exists (`db.sqlite3`)

## Web App Configuration
- [ ] Created web app on PythonAnywhere
- [ ] Configured WSGI file (see `pythonanywhere_wsgi.py`)
- [ ] Set environment variables:
  - [ ] `SECRET_KEY` (generated new one)
  - [ ] `DEBUG=False`
  - [ ] `ALLOWED_HOSTS=yourusername.pythonanywhere.com`
- [ ] Configured static files:
  - [ ] Ran `collectstatic`
  - [ ] Set static files URL and directory in Web app settings
- [ ] Configured media files (if needed)

## Final Steps
- [ ] Reloaded web app
- [ ] Tested homepage
- [ ] Tested user registration/login
- [ ] Tested admin panel
- [ ] Checked error logs (no errors)

## Post-Deployment
- [ ] Bookmarked error log URL
- [ ] Set up database backup routine
- [ ] Documented deployment process for future updates

---

## Quick Commands Reference

```bash
# Navigate to project
cd ~/hiremap

# Activate virtual environment
source venv/bin/activate

# Run migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Collect static files
python manage.py collectstatic --noinput

# Check configuration
python manage.py check
```

---

**Your site URL**: https://yourusername.pythonanywhere.com



