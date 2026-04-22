import os
import json
from google import genai
from dotenv import load_dotenv

load_dotenv()
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

def analyze(article):
    # prompt to feed to llm for exact output
    prompt = f"""
                You are a tech news intelligence analyst.

                Analyze the following article and return ONLY valid JSON.
                Do not include explanations, markdown, or extra text.
                Return EXACTLY the JSON structure specified.

                Article:
                Title: {article.get("title", "")}
                Description: {article.get("description", "")}
                Sources: {", ".join(article.get("sources", []))}
                URLs: {(article.get("urls", [""])[0])}
                Category: {article.get("category", "")}
                Fetched At: {article.get("fetched_at", "")}
                This topic appears in {article.get("count", 1)} articles from sources: {", ".join(article.get("sources", []))}.

                Return EXACTLY this JSON format:

                {{
                "signal_title": string,
                "category": string,
                "summary": string,
                "impact": string,
                "impact_score": number,
                "relevance": string,
                "relevance_score": number,
                "what_to_do": string,
                "impact_direction": "positive" | "negative",
                "quality_score": number,
                "isRelevant": boolean
                }}

                Rules:
                - summary must be 2-3 concise sentences
                - category must be one short related keyword (AI, Robotics, Startups, Big Tech, etc.)
                - impact must explain what will happen
                - relevance must explain why this matters now
                - what_to_do must be actionable (watch, learn, apply, invest, etc.)
                - impact_score must be between 1 and 10
                - relevance_score must be between 1 and 10
                - quality_score must be between 1 and 10
                - impact_direction must be "positive" or "negative"
                - isRelevant must be true or false
                - signal_title must be short, clear, and better than original title (max 8 words)

                Return ONLY JSON.
             """

    try:
        response = client.models.generate_content(
            model="gemini-1.5-flash",
            contents=prompt
        )

        parsed = json.loads(response.text)

        if not parsed.get("isRelevant") or parsed.get("quality_score", 0) < 5:
            return None

        updatedArticle = {
            **article,
            "signal_title": parsed.get("signal_title"),
            "summary": parsed.get("summary"),
            "category": parsed.get("category"),
            "impact": parsed.get("impact"),
            "impact_score": parsed.get("impact_score"),
            "relevance": parsed.get("relevance"),
            "relevance_score": parsed.get("relevance_score"),
            "what_to_do": parsed.get("what_to_do"),
            "impact_direction": parsed.get("impact_direction"),
            "quality_score": parsed.get("quality_score")
        }

        return updatedArticle

    except Exception as e:
        print("Analysis error:", e)
        return None


def analyzeArticles(articles):
    news = []
    for article in articles:
        result = analyze(article)
        if result:
            news.append(result)
    return news
