from .fetch_news import fetch_news
from .group_dupes import groupDuplicates
from .analysis_agent import analyzeArticles
from .ranking import rankArticles

def run_news_pipeline():
    news = fetch_news()
    groupedArticles = groupDuplicates(news)
    analyzedArticles = analyzeArticles(groupedArticles)
    rankedArticles = rankArticles(analyzedArticles)
    
    return rankedArticles





