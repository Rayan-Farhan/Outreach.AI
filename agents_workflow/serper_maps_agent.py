import http.client
import json
import os
import streamlit as st
from dotenv import load_dotenv

load_dotenv()

# Search places using Serper Maps API
def search_places_with_serper(query, city_name, page=1):
    conn = http.client.HTTPSConnection("google.serper.dev")

    payload = json.dumps({
        "q": f"{query} in {city_name}",
        "page": page
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

# Get leads from Serper based on desired count
def get_leads_from_serper(business_type, city, lead_count):
    pages_to_fetch = lead_count // 10
    all_leads = []

    for page in range(1, pages_to_fetch + 1):
        raw_results = search_places_with_serper(business_type, city, page)

        for place in raw_results.get("places", []):
            all_leads.append({
                "name": place.get("title"),
                "address": place.get("address"),
                "phone": place.get("phoneNumber"),
                "website": place.get("website"),
                "latitude": place.get("latitude"),
                "longitude": place.get("longitude")
            })

    return all_leads[:lead_count]