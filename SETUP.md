# Lukoba Django Setup Guide

## SQLite3 Issue Fix

If you encounter `ModuleNotFoundError: No module named '_sqlite3'`, this means your Python installation doesn't have SQLite3 support compiled in.

### Solution 1: Install SQLite3 Development Libraries and Recompile Python

1. Install SQLite3 development libraries:
   ```bash
   sudo apt-get update
   sudo apt-get install libsqlite3-dev
   ```

2. Reinstall Python with pyenv:
   ```bash
   pyenv uninstall 3.11.14
   pyenv install 3.11.14
   ```

3. Recreate virtual environment:
   ```bash
   cd /home/uchiha/Documents/projects/lukoba
   rm -rf .venv
   pyenv local 3.11.14
   python -m venv .venv
   source .venv/bin/activate
   pip install -r requirements.txt
   ```

### Solution 2: Use System Python (Alternative)

If you prefer to use the system Python (which has SQLite3):

1. Install python3-venv:
   ```bash
   sudo apt install python3.13-venv
   ```

2. Use system Python:
   ```bash
   cd /home/uchiha/Documents/projects/lukoba
   rm -rf .venv
   python3 -m venv .venv
   source .venv/bin/activate
   pip install -r requirements.txt
   ```

### Solution 3: Use PostgreSQL (Alternative)

If you have PostgreSQL installed:

1. Install psycopg2:
   ```bash
   pip install psycopg2-binary
   ```

2. Update `lukoba_django/settings.py`:
   ```python
   DATABASES = {
       'default': {
           'ENGINE': 'django.db.backends.postgresql',
           'NAME': 'lukoba',
           'USER': 'your_user',
           'PASSWORD': 'your_password',
           'HOST': 'localhost',
           'PORT': '5432',
       }
   }
   ```

## After Fixing SQLite3

Once SQLite3 is working:

1. Create .env file:
   ```bash
   cp env.example .env
   # Edit .env with your API keys
   ```

2. Run migrations:
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

3. Create superuser:
   ```bash
   python manage.py createsuperuser
   ```

4. Run server:
   ```bash
   python manage.py runserver
   ```
