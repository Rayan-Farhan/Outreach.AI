import http.client
import json
import requests
import os
from dotenv import load_dotenv
load_dotenv()

# Search places using Serper Maps API
def search_places_with_serper(query, city_name):
    conn = http.client.HTTPSConnection("google.serper.dev")

    payload = json.dumps({
        "q": f"{query} in {city_name}",
    })

    headers = {
        'X-API-KEY': os.getenv("SERPER_API_KEY"),
        'Content-Type': 'application/json'
    }

    conn.request("POST", "/places", payload, headers)
    res = conn.getresponse()

    if res.status != 200:
        raise Exception(f"Serper API failed with status {res.status}")

    data = res.read()
    return json.loads(data.decode("utf-8"))

# Master function: user gives business type + city
def get_leads_from_serper(business_type, city):
    raw_results = search_places_with_serper(business_type, city)

    leads = []
    for place in raw_results.get("places", []):
        leads.append({
            "name": place.get("title"),
            "address": place.get("address"),
            "phone": place.get("phoneNumber"),
            "website": place.get("website"),
            "latitude": place.get("latitude"),
            "longitude": place.get("longitude")
        })

    return leads

leads = get_leads_from_serper("Software House", "Karachi")
print(leads)