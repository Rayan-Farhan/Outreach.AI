import streamlit as st
import requests
import pandas as pd
from io import StringIO

st.set_page_config(page_title="⚡OutreachAI", layout="wide")

st.title("⚡OutreachAI, Your Personal Lead Generation Tool.")

left, right = st.columns([1.1, 1])

with left:
    st.markdown("""
OutreachAI is a free, all in one AI powered lead generation tool designed for fast and reliable outreach. Unlike traditional cold emailing platforms like Apollo.io or Instantly.ai that have limited free outreach options and complex setups, OutreachAI:

- Pulls live data from Google Maps based on niche and location
- Scrapes business websites for up to date information
- Collects verified emails and social media links available on Google Maps
- Uses AI to enrich leads with descriptions, unique selling points, and target audience
- Offers one click CSV export

It’s ideal for B2B outreach, freelancers, and agencies providing verified, warm leads with zero hassle. Just enter a business type and location to get started!
    """)

with right:
    business_type = st.text_input("Enter Business Type")
    location = st.text_input("Enter Location")
    lead_count = st.selectbox("Select Maximum Number of Leads", [10, 20, 30])

    if st.button("Generate Leads"):
        with st.spinner("Fetching and enriching leads..."):
            response = requests.post("http://localhost:8000/generate-leads", json={
                "business_type": business_type,
                "location": location,
                "lead_count": lead_count
            })

            if response.status_code == 200:
                data = response.json()
                csv_path = data.get("csv_path")
                lead_count = data.get("lead_count")

                if csv_path and lead_count > 0:
                    st.success(f"{lead_count} relevant leads generated successfully.")

                    csv_response = requests.get("http://localhost:8000/download", params={"path": csv_path})
                    if csv_response.status_code == 200:
                        df = pd.read_csv(StringIO(csv_response.text))
                        st.dataframe(df, use_container_width=True)

                        st.download_button(
                            label="Download CSV",
                            data=csv_response.content,
                            file_name="leads_export.csv",
                            mime="text/csv"
                        )
                    else:
                        st.error("Failed to load the exported CSV.")
                else:
                    st.warning("No enriched leads were found.")
            else:
                st.error("Error generating leads. Please try again.")