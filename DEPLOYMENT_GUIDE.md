# 🚀 Complete PythonAnywhere Deployment Guide for HireMap

This guide will walk you through deploying your HireMap Django application to PythonAnywhere, including setting up the database.

---

## 📋 Prerequisites

1. **PythonAnywhere Account**: Sign up at [pythonanywhere.com](https://www.pythonanywhere.com)
   - Free tier is available, but consider a paid plan for production
2. **GitHub Account** (recommended) or ability to upload files
3. **Your HireMap project** ready for deployment

---

## 📦 Step 1: Prepare Your Project Locally

### 1.1 Create a requirements.txt file
✅ Already created in your project root with:
```
Django==5.2.5
requests>=2.31.0
```

### 1.2 Update settings.py for production
✅ Already updated to use environment variables

### 1.3 Commit your code to Git (if using GitHub)
```bash
git add .
git commit -m "Prepare for deployment"
git push origin main
```

**OR** if not using Git, you'll upload files directly in Step 3.

---

## 🌐 Step 2: Set Up PythonAnywhere Account

1. Go to [pythonanywhere.com](https://www.pythonanywhere.com) and sign up/login
2. Once logged in, you'll see the dashboard

---

## 📤 Step 3: Upload Your Project

### Option A: Using GitHub (Recommended)

1. **Push your code to GitHub** (if not already done):
   - Create a repository on GitHub
   - Push your code:
   ```bash
   git remote add origin https://github.com/yourusername/hiremap.git
   git push -u origin main
   ```

2. **On PythonAnywhere Dashboard**:
   - Click on **"Files"** tab
   - Navigate to `/home/yourusername/`
   - Click **"Open Bash console here"**
   - Clone your repository:
   ```bash
   git clone https://github.com/yourusername/hiremap.git
   ```
   - This creates `/home/yourusername/hiremap/`

### Option B: Upload Files Directly

1. **On PythonAnywhere Dashboard**:
   - Click on **"Files"** tab
   - Navigate to `/home/yourusername/`
   - Click **"Upload a file"**
   - Upload your entire project folder (you may need to zip it first)

2. **Or use the Bash console**:
   - Open Bash console
   - Use `wget` or `curl` to download your project if hosted elsewhere

---

## 🐍 Step 4: Set Up Python Virtual Environment

1. **Open a Bash console** from the PythonAnywhere dashboard

2. **Navigate to your project directory**:
   ```bash
   cd ~/hiremap
   # or wherever you uploaded your project
   ```

3. **Create a virtual environment**:
   ```bash
   python3.10 -m venv venv
   # PythonAnywhere supports Python 3.8, 3.9, 3.10, or 3.11
   # Check which version is available: python3 --version
   ```

4. **Activate the virtual environment**:
   ```bash
   source venv/bin/activate
   ```

5. **Upgrade pip**:
   ```bash
   pip install --upgrade pip
   ```

6. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

---

## 🗄️ Step 5: Set Up the Database

### 5.1 Create Database Directory

```bash
# Make sure you're in your project directory
cd ~/hiremap

# Create directory for database (if needed)
mkdir -p ~/hiremap
```

### 5.2 Run Migrations

```bash
# Make sure virtual environment is activated
source venv/bin/activate

# Run migrations to create database tables
python manage.py migrate
```

This will create `db.sqlite3` in your project directory.

### 5.3 Create Superuser (Admin Account)

```bash
python manage.py createsuperuser
```

Follow the prompts to create your admin account.

---

## ⚙️ Step 6: Configure Settings for Production

### 6.1 Set Environment Variables

1. **Go to PythonAnywhere Dashboard**
2. **Click on "Web" tab**
3. **Click on your web app** (or create one - see Step 7)
4. **Scroll down to "Environment variables"**
5. **Add these variables**:

   - `SECRET_KEY`: Generate a new secret key:
     ```bash
     # In Bash console, run:
     python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
     ```
     Copy the output and paste it as the value for `SECRET_KEY`

   - `DEBUG`: Set to `False` (for production)
   - `ALLOWED_HOSTS`: Set to `yourusername.pythonanywhere.com` (replace `yourusername` with your actual username)

### 6.2 Alternative: Edit settings.py directly

You can also edit `settings.py` directly on PythonAnywhere:

```bash
cd ~/hiremap
nano HireMap/settings.py
```

Update:
- `DEBUG = False`
- `ALLOWED_HOSTS = ['yourusername.pythonanywhere.com']`
- `SECRET_KEY = 'your-generated-secret-key'`

---

## 🌍 Step 7: Create Web App

1. **Go to PythonAnywhere Dashboard**
2. **Click on "Web" tab**
3. **Click "Add a new web app"**
4. **Choose domain**: Select `yourusername.pythonanywhere.com`
5. **Select Python version**: Choose the same version you used for virtual environment (e.g., Python 3.10)
6. **Select "Manual configuration"** (not "Django")
7. **Click "Next"**

---

## 🔧 Step 8: Configure WSGI File

1. **In the Web app configuration page**, click on **"WSGI configuration file"** link
2. **Delete all the default code** and replace with:

```python
import os
import sys

# Add your project directory to the Python path
path = '/home/yourusername/hiremap'
if path not in sys.path:
    sys.path.insert(0, path)

# Set the Django settings module
os.environ['DJANGO_SETTINGS_MODULE'] = 'HireMap.settings'

# Activate your virtual environment
activate_this = '/home/yourusername/hiremap/venv/bin/activate_this.py'
with open(activate_this) as f:
    exec(f.read(), {'__file__': activate_this})

# Import Django WSGI application
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
```

**⚠️ IMPORTANT**: Replace `/home/yourusername/hiremap` with your actual path!

3. **Click "Save"**

---

## 📁 Step 9: Configure Static Files

1. **Collect static files**:
   ```bash
   cd ~/hiremap
   source venv/bin/activate
   python manage.py collectstatic --noinput
   ```

2. **In Web app configuration**, scroll to **"Static files"** section:
   - **URL**: `/static/`
   - **Directory**: `/home/yourusername/hiremap/staticfiles`

3. **Add media files** (if you have user uploads):
   - **URL**: `/media/`
   - **Directory**: `/home/yourusername/hiremap/media`

4. **Click "Save"**

---

## 🔗 Step 10: Configure URL Mapping

1. **In Web app configuration**, find **"Code"** section
2. **Source code**: `/home/yourusername/hiremap`
3. **Working directory**: `/home/yourusername/hiremap`

---

## 🗄️ Step 11: Database Configuration (Final Check)

### 11.1 Verify Database Path

Make sure your `settings.py` has the correct database path. On PythonAnywhere, SQLite works fine, but ensure the path is correct:

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}
```

This should work as-is since `BASE_DIR` is already set correctly.

### 11.2 Test Database Connection

```bash
cd ~/hiremap
source venv/bin/activate
python manage.py check --database default
```

### 11.3 Verify Tables Exist

```bash
python manage.py showmigrations
```

All migrations should show `[X]` (applied).

---

## 🚀 Step 12: Reload Web App

1. **Go back to Web app configuration page**
2. **Click the big green "Reload" button** at the top
3. **Wait for the reload to complete** (usually takes 10-30 seconds)

---

## ✅ Step 13: Test Your Deployment

1. **Visit your site**: `https://yourusername.pythonanywhere.com`
2. **Test the homepage**
3. **Test user registration/login**
4. **Test admin panel**: `https://yourusername.pythonanywhere.com/admin/`

---

## 🔐 Step 14: Security Checklist

- [x] `DEBUG = False` in production
- [x] `SECRET_KEY` is set via environment variable
- [x] `ALLOWED_HOSTS` includes your domain
- [x] SSL/HTTPS is enabled (PythonAnywhere provides this automatically)
- [x] Static files are collected and served correctly

---

## 🐛 Troubleshooting

### Issue: "DisallowedHost" Error
**Solution**: Add your domain to `ALLOWED_HOSTS` in settings.py or environment variables

### Issue: Static Files Not Loading
**Solution**: 
1. Run `python manage.py collectstatic`
2. Check static files configuration in Web app settings
3. Verify static files directory path

### Issue: Database Errors
**Solution**:
1. Check database file permissions: `chmod 664 db.sqlite3`
2. Check directory permissions: `chmod 755 ~/hiremap`
3. Verify migrations are applied: `python manage.py migrate`

### Issue: Module Not Found
**Solution**:
1. Verify virtual environment is activated in WSGI file
2. Check that all dependencies are installed: `pip list`
3. Verify Python path in WSGI configuration

### Issue: 500 Internal Server Error
**Solution**:
1. Check error logs in Web app → "Error log" section
2. Check server log for detailed error messages
3. Verify all environment variables are set correctly

---

## 📝 Step 15: Regular Maintenance

### Updating Your Code

1. **If using Git**:
   ```bash
   cd ~/hiremap
   git pull origin main
   source venv/bin/activate
   pip install -r requirements.txt  # if requirements changed
   python manage.py migrate  # if new migrations
   python manage.py collectstatic  # if static files changed
   ```
   Then reload the web app.

2. **If not using Git**: Upload new files and follow the same steps.

### Database Backups

```bash
# Create a backup
cp ~/hiremap/db.sqlite3 ~/hiremap/db_backup_$(date +%Y%m%d).sqlite3
```

### Viewing Logs

- **Error log**: Web app → "Error log"
- **Server log**: Web app → "Server log"

---

## 🎯 Quick Reference Commands

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

# Check Django configuration
python manage.py check

# View migrations status
python manage.py showmigrations
```

---

## 📞 Additional Resources

- [PythonAnywhere Help Docs](https://help.pythonanywhere.com/)
- [Django Deployment Checklist](https://docs.djangoproject.com/en/5.2/howto/deployment/checklist/)
- [PythonAnywhere Django Tutorial](https://help.pythonanywhere.com/pages/DeployExistingDjangoProject/)

---

## ✨ You're Done!

Your HireMap application should now be live at:
**https://yourusername.pythonanywhere.com**

Remember to:
- Keep your `SECRET_KEY` secret
- Regularly backup your database
- Monitor error logs
- Keep dependencies updated

Good luck with your deployment! 🚀

