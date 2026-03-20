import os
import time
import hashlib
from google import genai

client = genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))

# ✅ Smart cache
cache = {}


def generate_cache_key(query, context):
    """Create unique cache key"""
    raw = (query + context[:1000]).encode("utf-8")
    return hashlib.md5(raw).hexdigest()


def safe_extract_text(response):
    """
    Safely extract text from Gemini response
    """
    try:
        if hasattr(response, "text") and response.text:
            return response.text.strip()

        # fallback (rare cases)
        return str(response)
    except Exception:
        return "⚠️ Unable to parse response."


def normalize_items(summary_items):
    """
    Ensure consistent structure
    """
    normalized = []

    for item in summary_items:
        if isinstance(item, dict):
            normalized.append({
                "text": str(item.get("text", "")),
                "source": item.get("source", "Unknown"),
                "confidence": float(item.get("confidence", 1.0))
            })
        else:
            normalized.append({
                "text": str(item),
                "source": "Unknown",
                "confidence": 1.0
            })

    return normalized


def write_report(query, summary_items, sources=None):
    try:
        # 🔥 SAFETY INPUT
        if not summary_items:
            summary_items = [{"text": query, "source": "User Input", "confidence": 1.0}]

        if sources is None:
            sources = []

        summary_items = normalize_items(summary_items)

        # 🔥 BUILD CONTEXT
        context_parts = []
        extracted_sources = []

        for i, item in enumerate(summary_items[:3]):
            text = item["text"][:1000]
            source = item["source"]
            confidence = item["confidence"]

            if text.strip():
                context_parts.append(
                    f"{text} [{i+1}] (confidence: {round(confidence,2)})"
                )
                extracted_sources.append(source)

        if not context_parts:
            context_parts = [query]

        context = "\n\n".join(context_parts)[:3500]

        # 🔥 MERGE SOURCES
        all_sources = sources + extracted_sources
        unique_sources = list(dict.fromkeys([s for s in all_sources if s]))[:5]

        citation_text = (
            "\n".join([f"[{i+1}] {src}" for i, src in enumerate(unique_sources)])
            if unique_sources else "No sources available"
        )

        # 🔥 CACHE
        cache_key = generate_cache_key(query, context)

        if cache_key in cache:
            print("⚡ Using cached response")
            return cache[cache_key]

        # 🔥 OPTIMIZED PROMPT
        prompt = f"""
You are a professional AI Research Assistant.

Topic: {query}

Use ONLY the provided content. Do NOT say you lack data.
Always generate a useful report.

Content:
{context}

Write:

1. Title
2. Introduction (2 lines)
3. Key Findings (3-5 bullet points with [1], [2])
4. Technologies
5. Trends
6. Conclusion

Keep it concise (max 300 words).
"""

        # 🔥 RETRY WITH BACKOFF
        wait_time = 2

        for attempt in range(3):
            try:
                response = client.models.generate_content(
                    model="gemini-2.5-flash",
                    contents=prompt
                )

                result = safe_extract_text(response)

                if not result or len(result.strip()) < 20:
                    raise Exception("Empty response")

                result += "\n\n📚 Sources:\n" + citation_text

                cache[cache_key] = result
                return result

            except Exception as e:
                print(f"[Retry {attempt+1}] Gemini error: {e}")

                error_msg = str(e).lower()

                if "429" in error_msg or "quota" in error_msg:
                    wait_time = 30
                elif "503" in error_msg:
                    wait_time = 5
                else:
                    wait_time = 2

                print(f"⏳ Waiting {wait_time}s...")
                time.sleep(wait_time)

        # 🔥 FALLBACK MODEL
        try:
            print("⚠️ Switching to fallback model...")

            response = client.models.generate_content(
                model="gemini-2.0-flash",
                contents=prompt
            )

            result = safe_extract_text(response)

            result += "\n\n📚 Sources:\n" + citation_text

            cache[cache_key] = result
            return result

        except Exception as e:
            print(f"[Fallback failed]: {e}")

        # 🔥 FINAL FALLBACK (NO LLM)
        return f"""
⚠️ AI service unavailable.

📌 Topic: {query}

🔍 Key Points:
{context[:800]}

📚 Sources:
{citation_text}
"""

    except Exception as e:
        print(f"❌ Writer Agent Error: {e}")

        return f"""
⚠️ Report generation failed.

Reason:
{str(e)}

Try a simpler query.
"""