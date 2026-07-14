from database.models import User
from database.models import Chat
from database.models import Message

def get_user_by_username(
    db,
    username
):

    return db.query(User).filter(
        User.username == username
    ).first()


def get_user_by_email(
    db,
    email
):

    return db.query(User).filter(
        User.email == email
    ).first()


def create_user(
    db,
    username,
    email,
    password
):

    user = User(
        username=username,
        email=email,
        password=password
    )

    db.add(user)

    db.commit()

    db.refresh(user)

    return user