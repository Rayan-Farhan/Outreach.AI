from fastapi import FastAPI, Query
from fastapi.responses import FileResponse
from pydantic import BaseModel
from typing import List, Dict
from agents_workflow.serper_maps_agent import get_leads_from_serper
from agents_workflow.website_scraper_agent import scrape_website_for_data
from agents_workflow.company_info_extractor import extract_company_info
from agents_workflow.export_agent import export_leads_to_csv
from langchain_groq import ChatGroq
import uvicorn
import os

app = FastAPI()

chat_model = ChatGroq(model="llama3-8b-8192", temperature=0.0)

class LeadRequest(BaseModel):
    business_type: str
    location: str
    lead_count: int

@app.post("/generate-leads")
def generate_leads(request: LeadRequest):
    leads = get_leads_from_serper(request.business_type, request.location, request.lead_count)
    enriched_leads = []

    for biz in leads:
        website = biz.get("website")
        if not website:
            continue

        scraped_text = scrape_website_for_data(website)
        if not scraped_text:
            continue

        llm_info = extract_company_info(scraped_text, chat_model)
        final_lead = {**biz, **llm_info}
        enriched_leads.append(final_lead)

    if enriched_leads:
        csv_path = export_leads_to_csv(enriched_leads)
        return {"csv_path": csv_path, "lead_count": len(enriched_leads)}
    else:
        return {"csv_path": None, "lead_count": 0}

@app.get("/download")
def download_csv(path: str = Query(...)):
    if os.path.exists(path):
        return FileResponse(path, media_type='text/csv', filename=os.path.basename(path))
    return {"error": "File not found"}

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)