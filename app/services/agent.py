# from app.tools.search_flight import search_flight
# from app.tools.search_hotel import search_hotel
# from app.tools.build_itnerary import build_itinerary


# # def travel_agent(chat_id, message):

# #     if "goa" in message.lower() and "delhi" in message.lower():

# #         if "days" not in message:
# #             return "Please provide return date and number of days"

# #         flights = search_flight("Delhi", "Goa", "6 Sep")
# #         hotels = search_hotel("Goa", 4)

# #         return build_itinerary({
# #             "source": "Delhi",
# #             "destination": "Goa",
# #             "departure": "6 Sep",
# #             "return": "10 Sep",
# #             "days": 4,
# #             "flights": flights,
# #             "hotels": hotels
# #         })

# #     return "Tell me your travel plan (source, destination, dates)"


# def travel_agent(chat_id, message, history=None):

#     history = history or []

#     full_context = " ".join([h["content"] for h in history]) + " " + message
#     full_context = full_context.lower()


#     if "delhi" in full_context and "goa" in full_context:

#         if "10th" in full_context and "4" in full_context:

#             flights = search_flight("Delhi", "Goa", "10 Sep")
#             hotels = search_hotel("Goa", 4)

#             return build_itinerary({
#                 "source": "Delhi",
#                 "destination": "Goa",
#                 "departure": "10 Sep",
#                 "return": "14 Sep",
#                 "days": 4,
#                 "flights": flights,
#                 "hotels": hotels
#             })

#         return "Got it  When is your travel date and duration?"

#     return "Tell me source and destination"

# import json
# from app.llm.ollama_client import ask_ollama
# from app.llm.prompt import SYSTEM_PROMPT
# from app.tools.search_flight import search_flight
# from app.tools.search_hotel import search_hotel
# from app.tools.build_itnerary import build_itinerary


# def travel_agent(chat_id, message, history):

#     messages = [
#         {"role": "system", "content": SYSTEM_PROMPT}
#     ]


#     for h in history:
#         messages.append({
#             "role": h["role"],
#             "content": h["content"]
#         })


#     messages.append({"role": "user", "content": message})


#     llm_output = ask_ollama(messages)

#     data = json.loads(llm_output)


#     if data.get("missing_fields"):
#         return f"Please provide: {', '.join(data['missing_fields'])}"


#     flights = search_flight(
#         data["source"],
#         data["destination"],
#         data["departure_date"]
#     )

#     hotels = search_hotel(
#         data["destination"],
#         data["days"]
#     )

#     itinerary = build_itinerary({
#         **data,
#         "flights": flights,
#         "hotels": hotels
#     })

#     return itinerary














from datetime import datetime, timedelta

from app.services.llm_service import extract_state_with_llm

from app.tools.search_flight import search_flight
from app.tools.search_hotel import search_hotel
from app.tools.build_itnerary import build_itnerary

from app.db.chat_state import (
    get_state,
    save_state,
)
# from app.db.chat_repo import save_message, get_chat_history

def travel_agent(chat_id, message, db):


    state = get_state(db, chat_id)

    print("STATE FROM DATABASE:", state)

    if state is None:
        state = {
            "source": None,
            "destination": None,
            "departure_date": None,
            "return_date": None,
            "days": None,
        }

    print("CHAT ID:", chat_id)
    print("LOADED FROM DB:", state)


    updated = extract_state_with_llm(
        state,
        message
    )

    print("UPDATED STATE:", updated)


    state.update(
        {
            k: v
            for k, v in updated.items()
            if v not in [None, "", []]
        }
    )

  
    try:

   
        if (
            state.get("departure_date")
            and state.get("return_date")
        ):

            dep = datetime.strptime(
                state["departure_date"],
                "%d %b"
            )

            ret = datetime.strptime(
                state["return_date"],
                "%d %b"
            )

            state["days"] = (ret - dep).days


        elif (
            state.get("departure_date")
            and state.get("days")
            and not state.get("return_date")
        ):

            dep = datetime.strptime(
                state["departure_date"],
                "%d %b"
            )

            ret = dep + timedelta(
                days=int(state["days"])
            )

            state["return_date"] = ret.strftime(
                "%d %b"
            )

    except Exception as e:
        print("Date calculation error:", e)

    print("FINAL STATE:", state)


    save_state(
        db,
        chat_id,
        state
    )


    required = [
        "source",
        "destination",
        "departure_date",
    ]

    missing = [
        field
        for field in required
        if not state.get(field)
    ]

    if missing:
        return f"Please provide: {', '.join(missing)}"


    if (
        not state.get("days")
        and not state.get("return_date")
    ):
        return "Please provide either days or return_date"


    flights = search_flight(
        state["source"],
        state["destination"],
        state["departure_date"],
        state["return_date"]
    )

    print("FLIGHTS:", flights)


    hotels = search_hotel(
        state["destination"],
        state["departure_date"],
        state["return_date"]
    )

    print("HOTELS:", hotels)


    itinerary = build_itnerary(
        state,
        flights,
        hotels
    )

    return itinerary










