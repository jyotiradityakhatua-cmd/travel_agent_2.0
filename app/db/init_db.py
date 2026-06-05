from app.db.database import Base, engine
from app.db.models.chat_message import ChatMessage
from app.db.chat_state import ChatState 

def init_db():
    Base.metadata.create_all(bind=engine)