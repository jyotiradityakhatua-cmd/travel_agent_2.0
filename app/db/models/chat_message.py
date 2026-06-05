# from sqlalchemy import Column, String, Text, DateTime
# from sqlalchemy.sql import func
# from app.db.database import Base


# class ChatMessage(Base):
#     __tablename__ = "chat_messages"

#     id = Column(String, primary_key=True, index=True)
#     chat_id = Column(String, index=True)

#     role = Column(String)  
#     content = Column(Text)

#     created_at = Column(DateTime(timezone=True), server_default=func.now())


from sqlalchemy import Column, String, Integer, Text, DateTime
from datetime import datetime
from app.db.database import Base

class ChatMessage(Base):
    __tablename__ = "chat_messages"

    id = Column(Integer, primary_key=True, index=True)
    chat_id = Column(String, index=True)
    role = Column(String) 
    content = Column(Text)
    timestamp = Column(DateTime, default=datetime.utcnow)