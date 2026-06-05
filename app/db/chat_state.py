from sqlalchemy import Column, String
from app.db.database import Base


class ChatState(Base):
    __tablename__ = "chat_state"

    chat_id = Column(String, primary_key=True, index=True)
    source = Column(String, nullable=True)
    destination = Column(String, nullable=True)
    departure_date = Column(String, nullable=True)
    return_date = Column(String, nullable=True)