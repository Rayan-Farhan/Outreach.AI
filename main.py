# main.py

import os
from dotenv import load_dotenv
from agents_workflow.serper_maps_agent import get_local_businesses
from agents_workflow.website_scraper_agent import scrape_website_for_data
from agents_workflow.company_info_extractor import extract_company_info
from agents_workflow.export_agent import export_leads_to_csv
from langchain_groq import ChatGroq

load_dotenv()

def main():
    chat_model = ChatGroq(model="llama3-8b-8192", temperature=0.0)

    print("🔍 AI Lead Generation Workflow")

    query = input("Enter business type and location (e.g., 'Cafes in Austin, Texas'): ").strip()
    
    # take two inputs!!!!
    
    print("\n📍 Fetching businesses from Serper Maps...")
    businesses = get_local_businesses(query)

    print(f"Found {len(businesses)} businesses. Enriching data...\n")

    enriched_leads = []

    for idx, biz in enumerate(businesses, 1):
        print(f"🔗 [{idx}] Processing: {biz.get('name')}")

        website = biz.get("website")
        if not website:
            print("   ⚠️ No website. Skipping enrichment.\n")
            continue

        scraped_text, structured_scrape = scrape_website_for_data(website)
        if not scraped_text:
            print("   ⚠️ Failed to scrape.\n")
            continue

        llm_info = extract_company_info(scraped_text, chat_model)

        final_lead = {**biz, **structured_scrape, **llm_info}
        enriched_leads.append(final_lead)
        print("   ✅ Lead enriched.\n")

    if enriched_leads:
        csv_path = export_leads_to_csv(enriched_leads)
        print(f"✅ Exported {len(enriched_leads)} leads to CSV: {csv_path}")
    else:
        print("❌ No enriched leads to export.")

if __name__ == "__main__":
    main()