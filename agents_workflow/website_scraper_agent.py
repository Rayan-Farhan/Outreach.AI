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

def extract_about_section(url):
    try:
        headers = {"User-Agent": "Mozilla/5.0"}
        response = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(response.text, "html.parser")

        # Step 1: Find a link to the About page
        about_link = None
        for a in soup.find_all("a", href=True):
            href = a['href'].lower()
            if "about" in href:
                about_link = urljoin(url, href)
                break

        # Step 2: Follow that link to get About content
        if about_link:
            response = requests.get(about_link, headers=headers, timeout=10)
            about_soup = BeautifulSoup(response.text, "html.parser")

            # Step 3: Try to find the main content area
            main_content = ""
            for tag in about_soup.find_all(['section', 'div', 'article'], recursive=True):
                text = tag.get_text(strip=True, separator=' ')
                if len(text.split()) > 100:  # Only include large blocks of text
                    main_content += text + "\n\n"

            return main_content.strip()

        return "About page not found."
    
    except Exception as e:
        return f"Error extracting about section: {e}"

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

        about_text = extract_about_section(url)

        return {
            "raw_text": text[:5000],  # Truncate for safety
            "emails": emails,
            "social_links": social_links,
            "about_section": about_text[1000:5000]
        }

    except Exception as e:
        print(f"[!] Error scraping {url}: {e}")
        return None

#websiteData = scrape_website_for_data("https://contour-software.com/")
#print(websiteData)