from database.database import SessionLocal
from database.models import Memory


class MemoryDB:

    @staticmethod
    def save(user_id, key, value):

        db = SessionLocal()

        memory = Memory(
            user_id=user_id,
            key=key,
            value=value
        )

        db.add(memory)

        db.commit()

        db.close()

    @staticmethod
    def get_all(user_id):

        db = SessionLocal()

        memories = db.query(Memory).filter(
            Memory.user_id == user_id
        ).all()

        db.close()

        return memories