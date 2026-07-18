from database.database import SessionLocal
from database import crud

from auth.password import (
    hash_password,
    verify_password
)


class AuthService:

    @staticmethod
    def register(
        username,
        email,
        password
    ):

        db = SessionLocal()

        try:

            # Remove extra spaces
            username = username.strip()
            email = email.strip().lower()

            # Validation
            if not username:
                return False, "Username is required."

            if not email:
                return False, "Email is required."

            if not password:
                return False, "Password is required."

            # Check username
            existing_username = crud.get_user_by_username(
                db,
                username
            )

            if existing_username:
                return False, "Username already exists."

            # Check email
            existing_email = crud.get_user_by_email(
                db,
                email
            )

            if existing_email:
                return False, "Email already exists."

            hashed_password = hash_password(password)

            crud.create_user(
                db,
                username,
                email,
                hashed_password
            )

            return True, "Registration successful."

        except Exception as e:

            db.rollback()

            return False, f"Registration failed: {str(e)}"

        finally:

            db.close()

    @staticmethod
    def login(
        email,
        password
    ):

        db = SessionLocal()

        try:

            email = email.strip().lower()

            user = crud.get_user_by_email(
                db,
                email
            )

            if not user:
                return False, None

            if verify_password(
                password,
                user.password
            ):
                return True, user

            return False, None

        finally:

            db.close()