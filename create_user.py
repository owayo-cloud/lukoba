import argparse
from werkzeug.security import generate_password_hash
from db_setup import SessionLocal, init_db
from models import User
from db_setup import init_db

init_db()

def main():
    parser = argparse.ArgumentParser(description="Create a new user")
    parser.add_argument('username', type=str, help="Username of the new user")
    parser.add_argument('email', type=str, help="Email of the new user")
    parser.add_argument('password', type=str, help="Password for the new user")
    parser.add_argument('--admin', action='store_true',
                        help="Set this flag to create an admin user")

    args = parser.parse_args()

    create_user(args.username, args.email, args.password, args.admin)


def create_user(username, email, password, is_admin=False):
    db = SessionLocal()
    hashed_password = generate_password_hash(password)
    new_user = User(username=username, email=email,
                    password=hashed_password, is_admin=is_admin)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    db.close()
    print(f"User {username} created with admin status: {is_admin}")
    
if __name__ == "__main__":
    main()
