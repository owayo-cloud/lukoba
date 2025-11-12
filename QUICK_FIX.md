# Quick Fix for SQLite3 Issue

## The Problem
Python 3.11.14 from pyenv doesn't have SQLite3 support compiled in.

## Quick Solution

### Step 1: Install SQLite3 Development Libraries
```bash
sudo apt-get update
sudo apt-get install libsqlite3-dev
```

### Step 2: Reinstall Python with pyenv
```bash
pyenv uninstall 3.11.14
pyenv install 3.11.14
```

### Step 3: Recreate Virtual Environment
```bash
cd /home/uchiha/Documents/projects/lukoba
rm -rf .venv
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### Step 4: Verify SQLite3 Works
```bash
python -c "import sqlite3; print('SQLite3 OK')"
```

### Step 5: Run Migrations
```bash
python manage.py makemigrations
python manage.py migrate
```

## Alternative: Use System Python

If you prefer to use the system Python (which has SQLite3):

1. Install python3-venv:
   ```bash
   sudo apt install python3.13-venv
   ```

2. Remove pyenv local version:
   ```bash
   rm .python-version
   ```

3. Use system Python:
   ```bash
   rm -rf .venv
   python3 -m venv .venv
   source .venv/bin/activate
   pip install -r requirements.txt
   ```

## After Fixing

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
