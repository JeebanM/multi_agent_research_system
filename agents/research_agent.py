from tools.scraper import scrape_article
from urllib.parse import urlparse
import requests
from bs4 import BeautifulSoup


def chunk_text(text, chunk_size=500):
    text = text.strip()
    return [
        text[i:i + chunk_size]
        for i in range(0, len(text), chunk_size)
        if text[i:i + chunk_size].strip()
    ]


def get_domain_score(url):
    domain = urlparse(url).netloc.lower()

    trusted = ["arxiv.org", "ieee.org", "nature.com", "sciencedirect.com"]
    medium = ["medium.com", "towardsdatascience.com"]

    if any(t in domain for t in trusted):
        return 3
    elif any(m in domain for m in medium):
        return 2
    else:
        return 1


def is_valid_url(url):
    if not url or not isinstance(url, str):
        return False
    if url.endswith(".pdf"):
        return False
    if not url.startswith("http"):
        return False
    return True


def extract_arxiv_abstract(url):
    try:
        response = requests.get(url, timeout=10)
        soup = BeautifulSoup(response.text, "html.parser")

        abstract = soup.find("blockquote", class_="abstract")

        if abstract:
            return abstract.get_text().replace("Abstract:", "").strip()

    except Exception as e:
        print(f"[ARXIV ERROR] {url}: {e}")

    return None


def research_links(results, max_links=5, max_chars=1500, chunk_size=500):

    chunk_source_pairs = []
    seen_domains = set()

    # Normalize input
    if isinstance(results, dict):
        links = [item.get("link") for item in results.get("web", []) if item.get("link")]
    else:
        links = results if isinstance(results, list) else []

    ranked_links = []

    # Step 1: Filter + deduplicate
    for link in links:
        try:
            if not is_valid_url(link):
                continue

            domain = urlparse(link).netloc

            if domain in seen_domains:
                continue

            seen_domains.add(domain)

            score = get_domain_score(link)
            ranked_links.append((link, score))

        except Exception:
            continue

    # Step 2: Sort
    ranked_links.sort(key=lambda x: x[1], reverse=True)

    top_links = ranked_links[:max_links]

    print(f"🔗 Selected {len(top_links)} high-quality sources")

    # Step 3: Extract content
    for link, score in top_links:
        try:
            print(f"🌐 Processing: {link}")

            content = None

            # 🔥 arXiv handling
            if "arxiv.org" in link:
                print("📄 Extracting arXiv abstract...")
                content = extract_arxiv_abstract(link)

            # fallback scraping
            if not content:
                content = scrape_article(link)

            # 🔥 FIXED WEAK CONTENT HANDLING
            if not content or len(content.strip()) < 50:
                print("⚠️ Weak content, using fallback text")
                content = content if content else f"Information related to {link}"

            # clean + limit
            content = " ".join(content.split())
            content = content[:max_chars]

            chunks = chunk_text(content, chunk_size)

            for chunk in chunks:
                if chunk:
                    length_factor = len(chunk) / chunk_size
                    confidence = round(score * length_factor, 2)

                    chunk_source_pairs.append({
                        "text": chunk,
                        "source": link,
                        "confidence": confidence
                    })

        except Exception as e:
            print(f"[ERROR] {link}: {e}")

    # Final fallback
    if not chunk_source_pairs:
        print("[WARNING] No content extracted, using fallback")

        return [{
            "text": "General information could not be retrieved, using fallback knowledge.",
            "source": "system",
            "confidence": 0.5
        }]

    return chunk_source_pairs