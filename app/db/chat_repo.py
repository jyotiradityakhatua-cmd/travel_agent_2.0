from app.db.models.chat_message import ChatMessage


def save_message(db, chat_id: str, role: str, content: str):
    msg = ChatMessage(
        chat_id=chat_id,
        role=role,
        content=content
    )
    db.add(msg)
    db.commit()
    db.refresh(msg)
    return msg

def get_history_db(db, chat_id: str):
    messages = db.query(ChatMessage)\
        .filter(ChatMessage.chat_id == chat_id)\
        .order_by(ChatMessage.id.asc())\
        .all()

    return [
        {"role": m.role, "content": m.content}
        for m in messages
    ]