from sqlalchemy import Column, String
from app.db.database import Base
from sqlalchemy import Column, String, Integer
from datetime import datetime
from sqlalchemy import Column, Integer, String, Text, DateTime


class ChatState(Base):
    __tablename__ = "chat_state"

    chat_id = Column(String, primary_key=True, index=True)
    source = Column(String, nullable=True)
    destination = Column(String, nullable=True)
    departure_date = Column(String, nullable=True)
    return_date = Column(String, nullable=True)
    days = Column(Integer, nullable=True)





def get_state(db, chat_id):

    state = (
        db.query(ChatState)
        .filter(ChatState.chat_id == chat_id)
        .first()
    )

    if not state:
        return None

    return {
        "source": state.source,
        "destination": state.destination,
        "departure_date": state.departure_date,
        "return_date": state.return_date,
        "days": state.days
   
    }


def save_state(db, chat_id, data):

    state = (
        db.query(ChatState)
        .filter(ChatState.chat_id == chat_id)
        .first()
    )

    if not state:
        state = ChatState(chat_id=chat_id)
        db.add(state)

    state.source = data.get("source")
    state.destination = data.get("destination")
    state.departure_date = data.get("departure_date")
    state.return_date = data.get("return_date")
    state.days = data.get("days")

    db.commit()
    db.refresh(state)