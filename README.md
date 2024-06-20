# Lukoba

Lukoba is a movie booking website built with Python's HTTP server, Jinja2 templating, and SQLAlchemy for database management. The website supports user registration, login, movie browsing, and booking functionalities. It also includes an admin CLI for user management.

## Table of Contents

-   [Project Overview](#project-overview)
-   [Features](#features)
-   [Setup](#setup)
-   [Usage](#usage)
-   [Admin User Creation](#admin-user-creation)

## Project Overview

This project is a simple movie booking web application where users can register, log in, browse movies, and make bookings. The backend is built using Python's built-in HTTP server, Jinja2 for templating, and SQLAlchemy for database interactions.

## Features

-   User Registration and Login
-   Browsing Movies
-   Booking Movies
-   Admin User Management through CLI
-   Session Management with Cookies

## Setup

### Prerequisites

-   Python 3.x
-   Virtualenv

### Installation

1. Clone the repository:

    ```sh
    git clone https://github.com/owayo-cloud/lukoba.git
    cd lukoba
    ```

2. Create a virtual environment:

    ```sh
    python -m venv .venv
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

5. Initialize the database:
    ```sh
    python
    >>> from db_setup import init_db
    >>> init_db()
    >>> exit()
    ```

## Usage

1. Run the server:

    ```sh
    python server.py
    ```

2. Open your browser and navigate to:
    ```
    http://localhost:8000
    ```

## Admin User Creation

To create a user with admin access from the terminal, use the following steps:

1. Open a shell.

2. Execute the following commands:

    ```sh
    python create_user.py <username> <email> <password> --admin
    ```

    Replace `<username>`, `<email>`, and `<password>` with the desired values for the new user.

    For example:

    ```sh
    python create_user.py admin admin@example.com password123 --admin
    ```

    This will create a new user with the provided username, email, and password, and assign admin privileges.
