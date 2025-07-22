# agents/website_scraper_agent.py

import requests
from bs4 import BeautifulSoup
import re
from urllib.parse import urljoin
from typing import Optional, Dict

EMAIL_REGEX = r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}"

SOCIAL_DOMAINS = [
    "facebook.com", "instagram.com", "twitter.com",
    "linkedin.com", "youtube.com", "tiktok.com"
]

def scrape_website_for_data(url: str) -> Optional[Dict]:
    if not url:
        return None

    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")

        text = soup.get_text(separator=" ", strip=True)
        links = [a['href'] for a in soup.find_all('a', href=True)]

        emails = list(set(re.findall(EMAIL_REGEX, response.text)))
        social_links = list(set(
            link for link in links if any(domain in link for domain in SOCIAL_DOMAINS)
        ))

        about_text = ""
        for section in soup.find_all(["section", "div"]):
            if section.get("id", "").lower() in ["about", "about-us"]:
                about_text = section.get_text(strip=True)
                break
            if "about" in section.get("class", []):
                about_text = section.get_text(strip=True)
                break

        return {
            "raw_text": text[:5000],  # Truncate for safety
            "emails": emails,
            "social_links": social_links,
            "about_section": about_text
        }

    except Exception as e:
        print(f"[!] Error scraping {url}: {e}")
        return None
