from sqlalchemy.orm import Session

from database.models import User
from database.models import Chat
from database.models import Message
from database.models import Memory


# ==================================================
# USER CRUD
# ==================================================

def create_user(db: Session, username, email, password):

    user = User(
        username=username,
        email=email,
        password=password
    )

    db.add(user)
    db.commit()
    db.refresh(user)

    return user


def get_user_by_username(db: Session, username):

    return (
        db.query(User)
        .filter(User.username == username)
        .first()
    )


def get_user_by_email(db: Session, email):

    return (
        db.query(User)
        .filter(User.email == email)
        .first()
    )


# ==================================================
# CHAT CRUD
# ==================================================

def create_chat(db: Session, user_id, title="New Chat"):

    chat = Chat(
        title=title,
        user_id=user_id
    )

    db.add(chat)
    db.commit()
    db.refresh(chat)

    return chat


def get_user_chats(db: Session, user_id):

    return (
        db.query(Chat)
        .filter(Chat.user_id == user_id)
        .order_by(Chat.created_at.desc())
        .all()
    )


def get_chat(db: Session, chat_id):

    return (
        db.query(Chat)
        .filter(Chat.id == chat_id)
        .first()
    )


def rename_chat(db: Session, chat_id, new_title):

    chat = (
        db.query(Chat)
        .filter(Chat.id == chat_id)
        .first()
    )

    if chat:

        chat.title = new_title

        db.commit()
        db.refresh(chat)

    return chat


def delete_chat(db: Session, chat_id):

    chat = (
        db.query(Chat)
        .filter(Chat.id == chat_id)
        .first()
    )

    if chat:

        db.delete(chat)
        db.commit()


# ==================================================
# MESSAGE CRUD
# ==================================================

def save_message(db: Session, chat_id, role, content):

    message = Message(
        chat_id=chat_id,
        role=role,
        content=content
    )

    db.add(message)
    db.commit()
    db.refresh(message)

    return message


def get_chat_messages(db: Session, chat_id):

    return (
        db.query(Message)
        .filter(Message.chat_id == chat_id)
        .order_by(Message.created_at)
        .all()
    )


# ==================================================
# MEMORY CRUD
# ==================================================

def save_memory(db: Session, user_id, key, value):

    memory = (
        db.query(Memory)
        .filter(
            Memory.user_id == user_id,
            Memory.key == key
        )
        .first()
    )

    if memory:

        memory.value = value

    else:

        memory = Memory(
            user_id=user_id,
            key=key,
            value=value
        )

        db.add(memory)

    db.commit()
    db.refresh(memory)

    return memory


def get_memory(db: Session, user_id):

    return (
        db.query(Memory)
        .filter(Memory.user_id == user_id)
        .all()
    )


def get_memory_by_key(db: Session, user_id, key):

    return (
        db.query(Memory)
        .filter(
            Memory.user_id == user_id,
            Memory.key == key
        )
        .first()
    )


def delete_memory(db: Session, memory_id):

    memory = (
        db.query(Memory)
        .filter(Memory.id == memory_id)
        .first()
    )

    if memory:

        db.delete(memory)
        db.commit()

# ==================================================
# SEARCH CHATS
# ==================================================

def search_chats(db: Session, user_id, keyword):

    return (
        db.query(Chat)
        .filter(
            Chat.user_id == user_id,
            Chat.title.ilike(f"%{keyword}%")
        )
        .order_by(Chat.created_at.desc())
        .all()
    )