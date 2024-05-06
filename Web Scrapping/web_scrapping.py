import requests
from bs4 import BeautifulSoup
import re

# List of URLs to scrape
urls = [
    "https://www.infosys.com/about.html",
    "https://www.infosys.com/about/history.html",
    "https://www.infosys.com/about/subsidiaries.html",
    "https://www.infosys.com/about/management-profiles.html",
    "https://www.infosys.com/about/alliances.html",
    "https://www.infosys.com/about/awards.html",
    "https://www.infosys.com/about/overview.html",
    "https://www.infosys.com/newsroom/press-releases/2024/top-3-it-services-brand-globally2024.html",
    "https://www.infosys.com/newsroom/features/2023/recognized-global-top-employer.html",
    "https://www.infosys.com/industries.html",
    "https://www.infosys.com/services.html",
    "https://www.infosys.com/products-and-platforms.html",
    "https://www.infosys.com/about/springboard.html",
    "https://www.infosys.com/newsroom/journalist-resources/contact.html",
    "https://www.infosys.org/infosys-foundation/initiatives.html",
    "https://www.infosys.com/leadership-institute.html",
    "https://www.infosys.com/services/generative-ai/overview.html"
]

def scrape_and_save_text(urls):
    all_text = ""
    for url in urls:
        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Extracting all text from the page and combining into a single paragraph
        text_blocks = soup.find_all(['p', 'h1', 'h2', 'h3', 'li'])  # You can adjust the tags as necessary
        clean_text = ' '.join(block.get_text(strip=True) for block in text_blocks)
        clean_text = re.sub(r'\s+', ' ', clean_text)  # Replace multiple whitespace with single space
        clean_text = re.sub(r'\n+', ' ', clean_text)  # Replace multiple newlines with single space
        all_text += clean_text + "\n\n"
    
    # Removing additional whitespace and newlines from the entire document before saving
    formatted_text = re.sub(r'\s\s+', ' ', all_text)  # Collapse multiple spaces
    formatted_text = re.sub(r'\n\n+', '\n', formatted_text)  # Collapse multiple newlines

    # Saving the formatted text to a text file
    with open("infosys_data.txt", "w", encoding='utf-8') as file:
        file.write(formatted_text)

# Execute the function
scrape_and_save_text(urls)
