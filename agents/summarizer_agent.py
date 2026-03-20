import os
import requests
import time

USE_OLLAMA = os.getenv("USE_OLLAMA", "true").lower() == "true"


def ollama_summarize(text, retries=2):
    """
    Calls local Ollama (llama3) for summarization with retry support
    """

    prompt = f"""
Summarize the following text into 3 concise bullet points.

Rules:
- Keep it short and clear
- No extra explanation
- Focus on key insights

Text:
{text}
"""

    for attempt in range(retries + 1):
        try:
            response = requests.post(
                "http://localhost:11434/api/generate",
                json={
                    "model": "mistral",
                    "prompt": prompt,
                    "stream": False
                },
                timeout=30
            )

            if response.status_code != 200:
                print(f"[OLLAMA ERROR] Status {response.status_code}")
                time.sleep(2)
                continue

            data = response.json()
            result = data.get("response", "").strip()

            if result:
                return result

        except Exception as e:
            print(f"[OLLAMA ERROR]: {e}")
            time.sleep(2)

    # 🔥 fallback if all retries fail
    return text[:300]


def normalize_input(item):
    """
    Ensure input is always dict with text, source, confidence
    """
    if isinstance(item, dict):
        return {
            "text": item.get("text", ""),
            "source": item.get("source", "Unknown"),
            "confidence": item.get("confidence", 1.0)
        }
    else:
        return {
            "text": str(item),
            "source": "Unknown",
            "confidence": 1.0
        }


def summarize_chunks(chunk_source_pairs, max_chunks=3, max_chars=300):
    """
    Hybrid summarization with source + confidence preservation
    """

    summaries = []

    if not isinstance(chunk_source_pairs, list):
        print("[WARNING] Invalid input to summarizer")
        return []

    for item in chunk_source_pairs[:max_chunks]:

        try:
            data = normalize_input(item)

            text = " ".join(data["text"].split())[:1500]
            source = data["source"]
            confidence = data["confidence"]

            if not text.strip():
                continue

            # 🔥 Choose summarization method
            if USE_OLLAMA:
                summary_text = ollama_summarize(text)
            else:
                # lightweight fallback
                summary_text = " ".join(text.split()[:80])[:max_chars]

            summaries.append({
                "text": summary_text.strip(),
                "source": source,
                "confidence": confidence
            })

        except Exception as e:
            print(f"[ERROR] Summarization failed: {e}")

    # 🔥 fallback if empty
    if not summaries:
        print("[WARNING] No summaries generated, using fallback")

        fallback = [
            normalize_input(item)
            for item in chunk_source_pairs[:2]
        ]

        return fallback

    return summaries