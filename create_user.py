import argparse
from werkzeug.security import generate_password_hash
from db_setup import SessionLocal, init_db
from models import User

init_db()

def main():
    parser = argparse.ArgumentParser(description="Create a new user")
    parser.add_argument('username', type=str, help="Username of the new user")
    parser.add_argument('email', type=str, help="Email of the new user")
    parser.add_argument('password', type=str, help="Password for the new user")
    parser.add_argument('--admin', action='store_true', help="Set this flag to create an admin user")

    args = parser.parse_args()

    create_user(args.username, args.email, args.password, args.admin)

def validate_username_email(username, email, db):
    # Check if username already exists
    existing_user = db.query(User).filter(User.username == username).first()
    if existing_user:
        raise ValueError(f"Username '{username}' is already taken.")

    # Check if email already exists
    existing_email = db.query(User).filter(User.email == email).first()
    if existing_email:
        raise ValueError(f"Email '{email}' is already registered.")

    # Validate email format
    if not validate_email_format(email):
        raise ValueError(f"Email '{email}' is not in a valid format.")

def validate_email_format(email):
    # Basic email validation (or use a library for more robust validation)
    if "@" in email and "." in email.split('@')[-1]:
        return True
    return False

def validate_password_strength(password):
    if len(password) < 8:
        raise ValueError("Password must be at least 8 characters long.")
    if not any(char.isupper() for char in password):
        raise ValueError("Password must contain at least one uppercase letter.")
    if not any(char.isdigit() for char in password):
        raise ValueError("Password must contain at least one digit.")

def create_user(username, email, password, is_admin=False):
    db = SessionLocal()

    # Validate username and email
    validate_username_email(username, email, db)

    # Validate password strength
    validate_password_strength(password)

    # Create and save the new user
    hashed_password = generate_password_hash(password)
    new_user = User(username=username, email=email, password=hashed_password, is_admin=is_admin)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    db.close()
    print(f"User {username} created with admin status: {is_admin}")

if __name__ == "__main__":
    try:
        main()
    except ValueError as e:
        print(f"Error: {e}")
