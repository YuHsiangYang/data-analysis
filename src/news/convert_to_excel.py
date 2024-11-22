import pandas as pd
from src.news import news_models


def classify_news_to_excel(news_articles: list[news_models.NewsArticle], file_path: str):
    news_articles_dict = {
        'Title': [article.title for article in news_articles],
        'Publication Date': [article.date for article in news_articles],
        'Summary': [article.summary for article in news_articles],
        'URL': [article.href for article in news_articles],
        "Relevance": [article.additional_info["is_relevant"] for article in news_articles],
    }

    news_articles_df = pd.DataFrame(news_articles_dict)
    news_articles_df.to_excel(file_path, index=False)
    print(f'News articles are saved to {file_path}')