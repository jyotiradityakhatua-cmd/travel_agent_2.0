
# import uuid

# from fastapi import APIRouter

# from app.schemas.chat_schema import ChatRequest
# from app.agents.travel_agents import process_chat


# router = APIRouter()




# def generate_chat_id():

#     return str(uuid.uuid4())



# @router.post("/")
# async def chat(req: ChatRequest):

#     chat_id = req.chat_id

#     if not chat_id:

#         chat_id = generate_chat_id()



#     response = await process_chat(
#         user_id=req.user_id,
#         chat_id=chat_id,
#         message=req.message
#     )



#     return {
#         "chat_id": chat_id,
#         "response": response
#     }

# from fastapi import APIRouter, Depends
# from sqlalchemy.orm import Session

# from app.db.database import get_db
# from app.agents.travel_agents import process_chat

# router = APIRouter()


# @router.post("/chat")
# async def chat(
#     message: str,
#     chat_id: str | None = None,
#     db: Session = Depends(get_db)
   
# ):

#     response = await process_chat(
#         user_id="demo_user",   
#         chat_id=chat_id,
#         message=message
#     )

#     return response

# @router.get("/test")
# def test(db: Session = Depends(get_db)):

#     return {
#         "status": "ok"
#     }


# from fastapi import APIRouter, Depends
# from sqlalchemy.orm import Session
# from pydantic import BaseModel
# from typing import Optional

# from app.db.session import get_db
# from app.agents.travel_agents import process_chat

# router = APIRouter()




# class ChatRequest(BaseModel):
#     message: str
#     chat_id: Optional[str] = None




# @router.post("/chat")
# async def chat(
# from fastapi import APIRouter
# from app.memory.chat_store import add, get
# from app.services.agent import travel_agent

# router = APIRouter()


# @router.post("/")
# def chat(message: str, chat_id: str = "default"):

#     add(chat_id, "user", message)

#     response = travel_agent(chat_id, message)

#     add(chat_id, "assistant", response)

#     return {
#         "chat_id": chat_id,
#         "response": response,
#         "history": get(chat_id)
#     }


# import uuid
# from fastapi import APIRouter
# from app.memory.chat_store import add, get
# from app.services.agent import travel_agent

# router = APIRouter()


# @router.post("/")
# def chat(message: str, chat_id: str | None = None):


#     if not chat_id:
#         chat_id = str(uuid.uuid4())

#     add(chat_id, "user", message)

#     response = travel_agent(chat_id, message)

#     add(chat_id, "assistant", response)

#     return {
#         "chat_id": chat_id,
#         "response": response,
#         "history": get(chat_id)
#     }



# from app.memory.chat_store import add, get
# from app.services.agent import travel_agent





# @router.post("/")
# def chat(message: str, chat_id: str | None = None):


#     if not chat_id:
#         chat_id = str(uuid.uuid4())


#     add(chat_id, "user", message)


#     history = get(chat_id)

#     response = travel_agent(chat_id, message, history)


#     add(chat_id, "assistant", response)

#     return {
#         "chat_id": chat_id,
#         "response": response,
#         "history": get(chat_id)
#     }
import uuid
from fastapi import APIRouter
from fastapi import Depends
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.db.chat_repo import save_message
from app.memory.chat_store import get as get_memory, add as add_memory
from app.services.agent import travel_agent
from  app.db.chat_repo import get_history_db

router = APIRouter()
@router.post("/")
def chat(message: str, chat_id: str | None = None, db: Session = Depends(get_db)):

    if not chat_id:
        chat_id = str(uuid.uuid4())


    add_memory(chat_id, "user", message)


    save_message(db, chat_id, "user", message)

    history = get_memory(chat_id)

    response = travel_agent(chat_id, message, history)


    add_memory(chat_id, "assistant", response)


    save_message(db, chat_id, "assistant", response)

    return {
        "chat_id": chat_id,
        "response": response
    }

@router.post("/")
def chat(message: str, chat_id: str | None = None, db: Session = Depends(get_db)):

    if not chat_id:
        chat_id = str(uuid.uuid4())

   
    save_message(db, chat_id, "user", message)

    history = get_history_db(db, chat_id)


    response = travel_agent(chat_id, message, history)


    save_message(db, chat_id, "assistant", response)

    return {
        "chat_id": chat_id,
        "response": response,
        "history": history
    }