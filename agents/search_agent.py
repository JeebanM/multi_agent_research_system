from tools.google_search import google_search
from tools.arxiv_search import arxiv_search
from tools.news_search import news_search


def search_topic(query):

    google_results = google_search(query)
    arxiv_results = arxiv_search(query)
    news_results = news_search(query)

    # Flatten everything into a single list
    results = []

    for r in google_results:
        results.append(r)

    for r in arxiv_results:
        results.append(r["link"])   # important

    for r in news_results:
        results.append(r)

    return results