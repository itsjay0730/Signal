import os
from google import genai
from dotenv import load_dotenv

load_dotenv()
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

def analyze(article):
    prompt = f"""
                You are a tech news analyst.

                Analyze this article and return JSON only.

                Title: {article.get("title", "")}
                Description: {article.get("description", "")}
                Source: {article.get("source", "")}

                Return JSON:

                summary: one sentence summary
                impactScore: 1-10
                relevanceScore: 1-10
                qualityScore: 1-10
                category: short category name
                isRelevant: true or false
             """

    try:
        response = client.models.generate_content(
            model="gemini-1.5-flash",
            contents=prompt
        )

        text = response.text

        import json
        parsed = json.loads(text)

        if not parsed.get("isRelevant") or parsed.get("qualityScore", 0) < 5:
            return None

        updatedArticle = {
            **article,
            "summary": parsed.get("summary"),
            "impactScore": parsed.get("impactScore"),
            "relevanceScore": parsed.get("relevanceScore"),
            "qualityScore": parsed.get("qualityScore"),
            "category": parsed.get("category")
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
