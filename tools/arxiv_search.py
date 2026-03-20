import feedparser
from urllib.parse import quote


def arxiv_search(query, max_results=5):

    try:
        # ✅ Encode query to avoid URL errors
        encoded_query = quote(query)

        url = (
            f"http://export.arxiv.org/api/query?"
            f"search_query=all:{encoded_query}&start=0&max_results={max_results}"
        )

        feed = feedparser.parse(url)

        papers = []

        for entry in feed.entries:
            papers.append({
                "title": entry.title,
                "link": entry.link,
                "summary": entry.summary
            })

        return papers

    except Exception as e:
        print(f"❌ arXiv search error: {str(e)}")
        return []