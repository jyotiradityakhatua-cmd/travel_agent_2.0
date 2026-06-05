def build_itinerary(data: dict):

    flights = data.get("flights", [])
    hotels = data.get("hotels", [])

    return f"""
# Travel Itinerary

## Trip Details
- From: {data.get("source", "N/A")}
- To: {data.get['destination']}
- Departure: {data.get['departure date']}
- Return: {data.et['return']}
- Days: {data.get['days']}

---

##  Flights Options
{data.get(flights)}

---

##  Hotel Options
{data.get(hotels)}

---

##  Suggested Plan
Day 1: Arrival + Relax  
Day 2: Explore Beaches  
Day 3: Adventure Activities  
Day 4: Return  

---

 Have a great trip!
"""