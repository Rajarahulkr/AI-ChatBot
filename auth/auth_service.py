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

        user = crud.get_user_by_email(
            db,
            email
        )

        if user:

            db.close()

            return False, "Email already exists."

        hashed = hash_password(password)

        crud.create_user(
            db,
            username,
            email,
            hashed
        )

        db.close()

        return True, "Registration successful."

    @staticmethod
    def login(
        email,
        password
    ):

        db = SessionLocal()

        user = crud.get_user_by_email(
            db,
            email
        )

        if not user:

            db.close()

            return False, None

        if verify_password(
            password,
            user.password
        ):

            db.close()

            return True, user

        db.close()

        return False, None