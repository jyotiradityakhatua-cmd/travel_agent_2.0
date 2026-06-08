from app.db.database import Base, engine
from .chat_message import ChatMessage
from .chat_state import ChatState
import app.db.models

def init_db():
    Base.metadata.create_all(bind=engine)