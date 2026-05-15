import json
from groq import Groq
from django.conf import settings

_client = None


def _get_client():
    global _client
    if _client is None:
        _client = Groq(api_key=settings.GROQ_API_KEY)
    return _client


def generate_insights(post) -> dict:
    """Call Groq to produce insight_title and insight_description for a BlogPost."""
    prompt = f"""You are an editorial assistant. Given the blog post below, produce a JSON object with exactly two keys:
- "insight_title": a concise, punchy title (max 15 words) that captures the core insight of the post.
- "insight_description": a 2-3 sentence summary of the key takeaway a reader should walk away with.

Respond with valid JSON only — no markdown fences, no extra text.

Title: {post.title}
Excerpt: {post.excerpt or '(none)'}
Content:
{post.content[:3000]}
"""
    response = _get_client().chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.5,
        max_tokens=300,
    )
    raw = response.choices[0].message.content.strip()
    data = json.loads(raw)
    return {
        "insight_title": str(data["insight_title"])[:200],
        "insight_description": str(data["insight_description"]),
    }
