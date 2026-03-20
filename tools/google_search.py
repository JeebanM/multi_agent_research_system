import requests

API_KEY = "YOUR_API_KEY"
CX = "033e5c3852f4941d0"

def google_search(query, num_results=5):

    url = "https://www.googleapis.com/customsearch/v1"

    params = {
        "q": query,
        "key": API_KEY,
        "cx": CX,
        "num": num_results
    }

    response = requests.get(url, params=params)
    results = response.json()

    search_results = []

    for item in results.get("items", []):
        search_results.append({
            "title": item["title"],
            "link": item["link"],
            "snippet": item["snippet"]
        })

    return search_results