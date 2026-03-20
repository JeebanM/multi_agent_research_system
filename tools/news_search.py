import requests

API_KEY = "f354b563fbdc492f88235c9744962458"

def news_search(query):

    url = "https://newsapi.org/v2/everything"

    params = {
        "q": query,
        "apiKey": API_KEY,
        "pageSize": 5
    }

    response = requests.get(url, params=params)
    data = response.json()

    articles = []

    for article in data["articles"]:
        articles.append({
            "title": article["title"],
            "link": article["url"],
            "description": article["description"]
        })

    return articles