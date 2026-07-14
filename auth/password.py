import bcrypt


def hash_password(password: str):

    return bcrypt.hashpw(
        password.encode(),
        bcrypt.gensalt()
    ).decode()


def verify_password(
    password,
    hashed_password
):

    return bcrypt.checkpw(
        password.encode(),
        hashed_password.encode()
    )