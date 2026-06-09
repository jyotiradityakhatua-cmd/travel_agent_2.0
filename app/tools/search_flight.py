# def search_flight(source: str, destination: str, date: str):
 

    # return [
    #     {
    #         "airline": "IndiGo",
    #         "price": 6500,
    #         "source": source,
    #         "destination": destination,
    #         "date": date
    #     },
    #     {
    #         "airline": "Vistara",
    #         "price": 8200,
    #         "source": source,
    #         "destination": destination,
    #         "date": date
    #     }
    # ]


# def search_flight(source, destination, date, return_date):

#     return f"""
# ###  Available Flights

# | Airline | Source | Destination | Date | Price |
# |----------|----------|-------------|------|--------|
# | IndiGo | {source} | {destination} | {date} | ₹6,500 |
# | Vistara | {source} | {destination} | {date} | ₹8,200 |
# """

# from serpapi import GoogleSearch
# import os
# from dotenv import load_dotenv
# load_dotenv()

# def search_flights(source, destination, outbound_date,return_date):
#     params = {
#         "engine": "google_flights",
#         "departure_id": source,
#         "arrival_id": destination,
#         "outbound_date": outbound_date,
#         "return_date":return_date,
#         "type": 1,
#         "api_key": os.getenv("SERPAPI_KEY")
#     }

#     search = GoogleSearch(params)
#     results = search.get_dict()

#     flights = []

#     for flight in results.get("best_flights", []):
#         flights.append({
#             "airline": flight.get("airline"),
#             "price": flight.get("price"),
#             "duration": flight.get("duration"),
#         })

#     return flights

# from serpapi import GoogleSearch

# # from app.utils.logger import logger
# import os
# from dotenv import load_dotenv
# load_dotenv()


# SERP_API_KEY: os.getenv("serp_api_key")


# # logger.info("Fetching flights from SerpAPI")

# def search_flight(source, destination, date):

#     params = {
#         "engine": "google_flights",
#         "departure_id": source,
#         "arrival_id": destination,
#         "outbound_date": date,
#         "api_key": os.getenv("SERP_API_KEY")
#     }

#     search = GoogleSearch(params)
#     results = search.get_dict()

#     print("RAW FLIGHT RESPONSE:", results)

#     flights = []

#     for f in results.get("best_flights", []) or results.get("other_flights", []):
#         flights.append({
#             "airline": f.get("airline", "Unknown"),
#             "price": f.get("price", 0)
#         })

#     return flights


# load_dotenv()
# params = {
#     "engine": "google_flights",
#     "departure_id": "DEL",
#     "arrival_id": "GOI",
#     "outbound_date": "2026-09-14",
#     "api_key": os.getenv("serp_api_key"),
#     "return_date":"2026-10-12"
# }

# search = GoogleSearch(params)
# results = search.get_dict()

# print(results)



# from serpapi import GoogleSearch
# import os
# from dotenv import load_dotenv

# load_dotenv()

# SERP_API_KEY = os.getenv("SERP_API_KEY")


# chat_memory = {}

# def update_chat_memory(chat_id, source=None, destination=None):
#     if chat_id not in chat_memory:
#         chat_memory[chat_id] = {"source": None, "destination": None}

#     if source:
#         chat_memory[chat_id]["source"] = source

#     if destination:
#         chat_memory[chat_id]["destination"] = destination


# def search_flight(chat_id, source=None, destination=None, date=None):


#     update_chat_memory(chat_id, source, destination)


#     source = source or chat_memory.get(chat_id, {}).get("source")
#     destination = destination or chat_memory.get(chat_id, {}).get("destination")

#     if not source or not destination:
#         return {"error": "Source and destination not set for this chat_id"}

#     params = {
#         "engine": "google_flights",
#         "departure_id": source,
#         "arrival_id": destination,
#         "outbound_date": date,
#         "api_key": SERP_API_KEY
#     }

#     search = GoogleSearch(params)
#     results = search.get_dict()

#     print("RAW FLIGHT RESPONSE:", results)

#     flights = []

#     flights_data = results.get("best_flights") or results.get("other_flights") or []

#     for group in flights_data:
#         for f in group.get("flights", []):
#             flights.append({
#                 "airline": f.get("airline", "Unknown"),
#                 "price": group.get("price", 0)
#             })

#     return {
#         "chat_id": chat_id,
#         "source": source,
#         "destination": destination,
#         "flights": flights
#     }



# load_dotenv()

# SERP_API_KEY = os.getenv("serp_api_key")


# def search_flight(source, destination, date):

#     params = {
#         "engine": "google_flights",
#         "departure_id": source,
#         "arrival_id": destination,
#         "outbound_date": date,
#         "api_key": SERP_API_KEY,

#     }


#     # if return_date:
#     #     params["return_date"] = return_date

#     search = GoogleSearch(params)
#     results = search.get_dict()

#     print("RAW RESPONSE:", results)
#     return results


import requests

def search_flight(source, destination, date, return_date):
    prompt = f"""
You are a precise flight search engine.

 CRITICAL RULE:
You MUST return flights ONLY for the exact dates provided.
Do NOT include any other dates.

---

## SEARCH CRITERIA
- From: {source}
- To: {destination}
- Departure Date (MANDATORY FILTER): {date}
- Return Date (MANDATORY FILTER): {return_date}

---

## OUTPUT RULES
- Output ONLY Markdown
- No explanations
- No extra dates
- No guessing different days
- All flights MUST match the given departure date exactly
- If return_date is provided, include return flight options separately

---

## REQUIRED FORMAT

###  Departure Flights ({date})

| Airline | From | To | Departure Date | Price (INR) | Duration |
|----------|------|----|----------------|-------------|-----------|

###  Return Flights ({return_date})

| Airline | From | To | Departure Date | Price (INR) | Duration |
|----------|------|----|----------------|-------------|-----------|

---

Include realistic airlines such as:
- IndiGo
- Air India
- Vistara
- Akasa Air
- SpiceJet
"""

    response = requests.post(
        "http://localhost:11434/api/generate",
        json={
            "model": "llama3",
            "prompt": prompt,
            "stream": False
        }
    )

    return response.json()["response"]