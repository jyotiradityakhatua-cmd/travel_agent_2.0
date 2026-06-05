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

import json
from app.llm.ollama_client import ask_ollama
from app.llm.prompt import SYSTEM_PROMPT
from app.tools.search_flight import search_flight
from app.tools.search_hotel import search_hotel
from app.tools.build_itnerary import build_itinerary


def travel_agent(chat_id, message, history):

    messages = [
        {"role": "system", "content": SYSTEM_PROMPT}
    ]


    for h in history:
        messages.append({
            "role": h["role"],
            "content": h["content"]
        })


    messages.append({"role": "user", "content": message})


    llm_output = ask_ollama(messages)

    data = json.loads(llm_output)


    if data.get("missing_fields"):
        return f"Please provide: {', '.join(data['missing_fields'])}"


    flights = search_flight(
        data["source"],
        data["destination"],
        data["departure_date"]
    )

    hotels = search_hotel(
        data["destination"],
        data["days"]
    )

    itinerary = build_itinerary({
        **data,
        "flights": flights,
        "hotels": hotels
    })

    return itinerary