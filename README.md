# Lukoba - Django Movie Booking System

Lukoba is a movie booking website built with Django, featuring user registration, login, movie browsing, and booking functionalities. It includes an admin dashboard for management and M-Pesa payment integration.

## Table of Contents

- [Project Overview](#project-overview)
- [Features](#features)
- [Setup](#setup)
- [Usage](#usage)
- [Environment Variables](#environment-variables)
- [Admin User Creation](#admin-user-creation)
- [Management Commands](#management-commands)

## Project Overview

This project is a Django-based movie booking web application where users can register, log in, browse movies, and make bookings. The backend uses Django ORM for database interactions, and integrates with OMDB API for movie data and M-Pesa for payments.

## Features

- User Registration and Login
- Browsing Movies (with OMDB API integration)
- Seat Selection and Booking
- M-Pesa Payment Integration
- Admin Dashboard with Analytics
- User Management
- Booking Management
- PDF Report Generation
- Session Management

## Setup

### Prerequisites

- Python 3.8 or higher
- pip
- Virtualenv (recommended)

### Installation

1. Clone the repository:

    ```sh
    git clone https://github.com/owayo-cloud/lukoba.git
    cd lukoba
    ```

2. Create a virtual environment:

    **Important:** Make sure your Python installation has SQLite3 support. If you encounter `ModuleNotFoundError: No module named '_sqlite3'`, see the [Troubleshooting](#troubleshooting) section below.

    ```sh
    python -m venv .venv
    ```

    **Note:** If using pyenv, ensure SQLite3 development libraries are installed:
    ```sh
    sudo apt-get install libsqlite3-dev
    pyenv install 3.11.14  # Reinstall if needed
    ```

3. Activate the virtual environment:

    - On Windows:
        ```sh
        .\.venv\Scripts\activate
        ```

    - On macOS and Linux:
        ```sh
        source .venv/bin/activate
        ```

4. Install the required packages:

    ```sh
    pip install -r requirements.txt
    ```

5. Set up environment variables:

    ```sh
    cp env.example .env
    ```

    Edit `.env` file and add your configuration:
    - `SECRET_KEY`: Django secret key (generate a random string)
    - `OMDB_API_KEY`: Your OMDB API key (get it from http://www.omdbapi.com/)
    - `MPESA_CONSUMER_KEY`: Your M-Pesa consumer key
    - `MPESA_CONSUMER_SECRET`: Your M-Pesa consumer secret
    - `MPESA_BUSINESS_SHORT_CODE`: Your M-Pesa business short code
    - `MPESA_LIPA_NA_MPESA_ONLINE_PASSKEY`: Your Lipa na M-Pesa online passkey
    - `MPESA_CALLBACK_URL`: Your M-Pesa callback URL

6. Run database migrations:

    ```sh
    python manage.py makemigrations
    python manage.py migrate
    ```

7. Create a superuser (admin):

    ```sh
    python manage.py createsuperuser
    ```

## Usage

1. Run the development server:

    ```sh
    python manage.py runserver
    ```

2. Open your browser and navigate to:
    ```
    http://localhost:8000
    ```

3. Access the admin panel:
    ```
    http://localhost:8000/admin
    ```

## Environment Variables

Create a `.env` file in the project root with the following variables:

```env
SECRET_KEY=your-secret-key-here
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# M-Pesa Configuration
MPESA_CONSUMER_KEY=your-mpesa-consumer-key
MPESA_CONSUMER_SECRET=your-mpesa-consumer-secret
MPESA_BUSINESS_SHORT_CODE=174379
MPESA_LIPA_NA_MPESA_ONLINE_PASSKEY=your-passkey
MPESA_CALLBACK_URL=https://your-domain.com/mpesa_callback/

# OMDB API Configuration
OMDB_API_KEY=your-omdb-api-key
```

## Admin User Creation

To create a user with admin access from the terminal, use the Django management command:

```sh
python manage.py create_user <username> <email> <password> --admin
```

Replace `<username>`, `<email>`, and `<password>` with the desired values for the new user.

For example:

```sh
python manage.py create_user admin admin@example.com Password123 --admin
```

This will create a new user with the provided username, email, and password, and assign admin privileges.

**Note:** Password must be at least 8 characters long and contain at least one uppercase letter and one digit.

## Management Commands

### Populate Database

Populate the database with sample data:

```sh
python manage.py populate_db --users 10 --movies "Inception" "The Dark Knight" --showtimes 20 --bookings 15
```

Options:
- `--users`: Number of users to create (default: 10)
- `--movies`: List of movie titles to add (required)
- `--showtimes`: Number of showtimes to create (default: 20)
- `--bookings`: Number of bookings to create (default: 15)

### Generate Report

Generate a PDF report from the database:

```sh
python manage.py generate_report --output report.pdf
```

## Project Structure

```
lukoba/
├── booking/                    # Main app
│   ├── management/
│   │   └── commands/          # Management commands
│   ├── migrations/            # Database migrations
│   ├── models.py             # Database models
│   ├── views.py              # Views
│   ├── urls.py               # URL routing
│   └── utils.py              # Utility functions
├── lukoba_django/            # Django project settings
│   ├── settings.py           # Django settings
│   ├── urls.py               # Main URL configuration
│   └── wsgi.py               # WSGI configuration
├── templates/                # HTML templates
├── static/                   # Static files (CSS, JS, images)
├── manage.py                 # Django management script
├── requirements.txt          # Python dependencies
└── .env                      # Environment variables (create from env.example)
```

## API Integration

### OMDB API

The application uses the OMDB API to fetch movie data. Get your API key from: http://www.omdbapi.com/

### M-Pesa API

The application integrates with M-Pesa for payment processing. You need to:
1. Register for M-Pesa Developer Portal
2. Get your consumer key and secret
3. Set up your business short code
4. Configure the callback URL

## Troubleshooting

### SQLite3 Module Not Found

If you encounter `ModuleNotFoundError: No module named '_sqlite3'`:

**Solution 1: Install SQLite3 Development Libraries (Recommended)**

```bash
# Install SQLite3 development libraries
sudo apt-get update
sudo apt-get install libsqlite3-dev

# If using pyenv, reinstall Python
pyenv uninstall 3.11.14
pyenv install 3.11.14

# Recreate virtual environment
rm -rf .venv
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

**Solution 2: Use System Python**

```bash
# Install python3-venv
sudo apt install python3.13-venv

# Use system Python
rm -rf .venv
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

**Solution 3: Use PostgreSQL**

If you have PostgreSQL installed:

```bash
# Install PostgreSQL adapter
pip install psycopg2-binary

# Update settings.py to use PostgreSQL
# See SETUP.md for details
```

For more details, see [SETUP.md](SETUP.md).

## License

This project is licensed under the MIT License.

## Contributors

- Original developers
- Django conversion contributors