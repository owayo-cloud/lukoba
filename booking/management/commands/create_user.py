from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
import re

User = get_user_model()


class Command(BaseCommand):
    help = 'Create a new user with optional admin privileges'

    def add_arguments(self, parser):
        parser.add_argument('username', type=str, help='Username of the new user')
        parser.add_argument('email', type=str, help='Email of the new user')
        parser.add_argument('password', type=str, help='Password for the new user')
        parser.add_argument('--admin', action='store_true', help='Set this flag to create an admin user')

    def handle(self, *args, **options):
        username = options['username']
        email = options['email']
        password = options['password']
        is_admin = options.get('admin', False)

        # Validate username
        if User.objects.filter(username=username).exists():
            raise ValidationError(f"Username '{username}' is already taken.")

        # Validate email
        if User.objects.filter(email=email).exists():
            raise ValidationError(f"Email '{email}' is already registered.")

        # Validate email format
        if not self.validate_email_format(email):
            raise ValidationError(f"Email '{email}' is not in a valid format.")

        # Validate password strength
        if not self.validate_password_strength(password):
            raise ValidationError("Password must be at least 8 characters long and contain at least one uppercase letter and one digit.")

        # Create user
        try:
            user = User.objects.create_user(
                username=username,
                email=email,
                password=password,
                is_admin=is_admin
            )
            self.stdout.write(
                self.style.SUCCESS(f'Successfully created user "{username}" with admin status: {is_admin}')
            )
        except Exception as e:
            raise ValidationError(f"Failed to create user: {str(e)}")

    def validate_email_format(self, email):
        """Validate email format"""
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(pattern, email) is not None

    def validate_password_strength(self, password):
        """Validate password strength"""
        if len(password) < 8:
            return False
        if not any(char.isupper() for char in password):
            return False
        if not any(char.isdigit() for char in password):
            return False
        return True
