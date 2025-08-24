# ⚡ Outreach.AI — An AI-Powered Lead Generation Assistant

## 👉 **[Generate reliable, enriched business leads with the power of AI!](https://github.com/Rayan-Farhan/OutreachAI)**

This **AI-powered lead generator** pulls live data from Google Maps, scrapes business websites for updated info, and uses **AI agents** to enrich leads with meaningful insights, all packed into a simple, one click workflow.

If you are tired of juggling messy spreadsheets, outdated directories, or expensive lead platforms, then let OutreachAI handle the heavy lifting in seconds!

https://github.com/user-attachments/assets/0c22b0de-511d-4e9f-8ca8-2416038a668e

---

## Why OutreachAI?

- **Fresh Data** – Live business listings pulled directly from Google Maps  
- **Verified Info** – Collects emails & social media links from business websites  
- **AI Enrichment** – Clear company description, unique selling points, and target audience  
- **Simple Workflow** – Enter a niche + location to get a ready to use CSV  
- **B2B Friendly** – Perfect for freelancers, agencies, and outreach professionals  

---

## How It Works

The workflow is powered by a sequence of specialized agents:

### 1. Google Maps Lead Finder  
- Uses **Serper.dev API** to fetch business data (name, address, phone, website).  

### 2. Website Scraper  
- Visits the business website to extract:  
  - Raw text  
  - Email addresses  
  - Social media profiles  
  - About page content  

### 3. Company Info Extractor  
- Uses **Groq + LLaMA-3** to distill website data into:  
  - Business description  
  - Unique selling points  
  - Target audience  

### 4. Export Agent  
- Compiles all enriched leads into a clean **CSV export**.  

---

## Project Structure

```
OutreachAI/
├── agents_workflow/
│ ├── company_info_extractor.py # AI enrichment agent
│ ├── export_agent.py # CSV export agent
│ ├── serper_maps_agent.py # Google Maps lead finder
│ ├── website_scraper_agent.py # Scrapes company websites
│ └── init.py
├── main.py # FastAPI backend
├── app.py # Streamlit frontend
├── requirements.txt
├── .env
├── RUN ME.bat
└── README.md # You’re reading it!
```

---

## How to Use

### 1. Clone the Repo

```bash
git clone https://github.com/Rayan-Farhan/Outreach.AI.git
cd OutreachAI
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Add Your API Keys

Enter your api keys in the .env file:

```env
SERPER_API_KEY = your_serper_api_key
GROQ_API_KEY = your_groq_api_key
```

Get your Serper API Key from [here](https://serper.dev)

Get your GROQ API KEY from [here](https://groq.com)

### 4. Run the Tool

Either run everything at once using:

```bash
RUN ME.bat
```

Or manually:

```bash
# Start backend
uvicorn main:app --reload

# In a separate terminal
streamlit run app.py
```

### 5. Try It Out!

Open the Streamlit app in your browser.

Enter a business type + location (e.g., Software House in Karachi) and get enriched leads in seconds!

---

## Output

Once the process completes, you get:

- **Business info**
- **Verified emails & social links**
- **AI enriched insights (description, USPs, target audience)**
- **Downloadable CSV with all leads**

---

## Built With

- **FastAPI** – Backend server
- **Streamlit** – Frontend interface
- **Serper.dev API** – Google Maps business search
- **BeautifulSoup** – Web scraping
- **Groq + LLaMA-3** – AI enrichment of leads
- **Pandas** – CSV export

---

## **Contributing**

Contributions are welcome! Please open an issue or submit a pull request for any changes. 

---

## **Contact**

If you have any questions or suggestions, feel free to reach out!

