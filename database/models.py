from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import Text
from sqlalchemy import DateTime
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship

from datetime import datetime

from database.database import Base


# ==================================================
# USER
# ==================================================

class User(Base):

    __tablename__ = "users"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    username = Column(
        String,
        unique=True,
        nullable=False
    )

    email = Column(
        String,
        unique=True,
        nullable=False
    )

    password = Column(
        String,
        nullable=False
    )

    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )

    chats = relationship(
        "Chat",
        back_populates="user",
        cascade="all, delete-orphan"
    )

    memories = relationship(
        "Memory",
        back_populates="user",
        cascade="all, delete-orphan"
    )


# ==================================================
# CHAT
# ==================================================

class Chat(Base):

    __tablename__ = "chats"

    id = Column(
        Integer,
        primary_key=True
    )

    title = Column(
        String,
        default="New Chat"
    )

    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )

    user_id = Column(
        Integer,
        ForeignKey("users.id")
    )

    user = relationship(
        "User",
        back_populates="chats"
    )

    messages = relationship(
        "Message",
        back_populates="chat",
        cascade="all, delete-orphan"
    )


# ==================================================
# MESSAGE
# ==================================================

class Message(Base):

    __tablename__ = "messages"

    id = Column(
        Integer,
        primary_key=True
    )

    role = Column(
        String
    )

    content = Column(
        Text
    )

    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )

    chat_id = Column(
        Integer,
        ForeignKey("chats.id")
    )

    chat = relationship(
        "Chat",
        back_populates="messages"
    )


# ==================================================
# MEMORY
# ==================================================

class Memory(Base):

    __tablename__ = "memories"

    id = Column(
        Integer,
        primary_key=True
    )

    user_id = Column(
        Integer,
        ForeignKey("users.id")
    )

    key = Column(
        String,
        nullable=False
    )

    value = Column(
        Text,
        nullable=False
    )

    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )

    user = relationship(
        "User",
        back_populates="memories"
    )