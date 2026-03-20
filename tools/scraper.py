import requests
from bs4 import BeautifulSoup


def scrape_article(url):

    try:
        headers = {
            "User-Agent": "Mozilla/5.0"
        }

        response = requests.get(url, headers=headers, timeout=10)

        # ❌ Skip non-HTML content
        if "text/html" not in response.headers.get("Content-Type", ""):
            return None

        soup = BeautifulSoup(response.text, "html.parser")

        paragraphs = soup.find_all("p")

        text = " ".join([p.get_text() for p in paragraphs])

        # ❌ Skip empty content
        if len(text.strip()) < 50:
            return None

        return text

    except Exception as e:
        print(f"❌ Error scraping {url}: {str(e)}")
        return None