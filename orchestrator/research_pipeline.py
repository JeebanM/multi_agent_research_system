from agents.planner_agent import plan_research
from agents.search_agent import search_topic
from agents.research_agent import research_links
from agents.summarizer_agent import summarize_chunks
from agents.verification_agent import verify_information
from agents.writer_agent import write_report

import time

# 🔥 Global cache
cache = {}


def safe_writer_call(query, content, sources):
    for _ in range(3):
        try:
            return write_report(query, content, sources)
        except Exception as e:
            if "quota" in str(e).lower() or "429" in str(e):
                print("⚠️ Gemini quota hit, retrying in 30s...")
                time.sleep(30)
            else:
                raise e
    return "❌ Failed after multiple retries due to quota limits."


def extract_text(item):
    if isinstance(item, dict):
        return item.get("text", "")
    return str(item)


def extract_sources(chunks):
    """
    🔥 Extract unique sources from chunk list
    """
    return list({
        c.get("source")
        for c in chunks
        if isinstance(c, dict) and c.get("source")
    })


def run_pipeline(query: str):
    try:
        print("\n🔹 Starting Research Pipeline...\n")

        # 🔥 CACHE
        if query in cache:
            print("⚡ Using cached result\n")
            return cache[query]

        # 1️⃣ Planning
        print("🧠 Planning research...")
        plan = plan_research(query)
        improved_query = plan.get("improved_query", query)

        print(f"Original Query: {query}")
        print(f"Improved Query: {improved_query}\n")

        # 2️⃣ Search
        print("🔍 Searching for information...")
        search_results = search_topic(improved_query)

        web_results = (
            search_results.get("web", [])
            if isinstance(search_results, dict)
            else search_results
        )

        if not web_results:
            print("⚠️ No results found. Retrying...")
            search_results = search_topic(query + " latest research")

            web_results = (
                search_results.get("web", [])
                if isinstance(search_results, dict)
                else search_results
            )

        if not web_results:
            raise Exception("Search failed: No results found")

        web_results = web_results[:5]
        print(f"Found {len(web_results)} results\n")

        # 3️⃣ Research (FIXED)
        print("📚 Extracting and chunking content...")
        chunks = research_links(web_results)

        if not isinstance(chunks, list):
            print("⚠️ Invalid research output, forcing fallback")
            chunks = []

        # Retry with fewer links
        if not chunks:
            print("⚠️ Retrying with fewer links...")
            chunks = research_links(web_results[:2])

        # Final fallback
        if not chunks:
            print("⚠️ Using fallback content")
            chunks = [{
                "text": f"General information about {query}",
                "source": "fallback",
                "confidence": 0.5
            }]

        # 🔥 Extract sources properly
        sources = extract_sources(chunks)

        print(f"Generated {len(chunks)} chunks")
        print(f"Collected {len(sources)} sources\n")

        # 4️⃣ Summarization
        print("🧾 Summarizing content...")

        limited_chunks = chunks[:3]

        processed_chunks = [
            {
                "text": extract_text(c)[:1500],
                "source": c.get("source", "") if isinstance(c, dict) else "",
                "confidence": c.get("confidence", 1.0) if isinstance(c, dict) else 1.0
            }
            for c in limited_chunks
        ]

        summaries = summarize_chunks(processed_chunks)

        if not summaries:
            print("⚠️ Summarization failed, using raw chunks")
            summaries = processed_chunks

        print(f"Generated {len(summaries)} summaries\n")

        # 5️⃣ Verification
        print("✅ Verifying information...")
        try:
            verified_docs = verify_information(summaries)
        except Exception:
            print("⚠️ Verification skipped")
            verified_docs = summaries

        if not verified_docs:
            verified_docs = summaries

        print(f"Verified {len(verified_docs)} documents\n")

        # 6️⃣ Final Content Prep
        final_docs = verified_docs[:3]

        final_texts = [
            extract_text(doc)[:1200]
            for doc in final_docs
            if extract_text(doc).strip()
        ]

        if not final_texts:
            final_texts = [query]

        combined_content = "\n\n".join(final_texts)

        # 7️⃣ Writing
        print("✍️ Generating final report...")
        report = safe_writer_call(improved_query, combined_content, sources)

        if not report:
            raise Exception("Report generation failed")

        # 🔥 Cache result
        cache[query] = report

        print("\n✅ Pipeline completed successfully!\n")
        return report

    except Exception as e:
        print(f"\n❌ Error in pipeline: {str(e)}")

        return f"""
⚠️ Research could not be fully completed.

Reason:
{str(e)}

Suggestions:
- Try broader queries
- Reduce complexity
- Wait if quota exceeded
- Avoid very long inputs

Example:
"AI in healthcare recent research"
"""


if __name__ == "__main__":
    query = input("Enter your research query: ")
    result = run_pipeline(query)

    if result:
        print("\n📄 Final Report:\n")
        print(result)