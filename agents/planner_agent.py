def plan_research(query: str):

    # Step 1: Improve query if needed
    if "2026" in query or "future" in query.lower():
        improved_query = query.replace("2026", "recent").replace("future", "latest")
    else:
        improved_query = query

    # Step 2: Add search optimization
    improved_query += " research papers OR latest developments OR study"

    # Step 3: Create dynamic plan
    plan = {
        "original_query": query,
        "improved_query": improved_query,
        "steps": [
            "search web",
            "search research papers (arXiv)",
            "search news sources",
            "scrape webpages",
            "extract key insights",
            "verify information",
            "generate structured report"
        ]
    }

    return plan