import logging
import json
from src.llm import chatgptcredentials
import pydantic
from typing import Callable, List
import os
import time
from src.llm import ChatGPT_BrowserBased
from src.news import news_models


class RelevanceSchema(pydantic.BaseModel):
    is_related: bool
    reason: str


def IdenfityRelevance(
    news_article: news_models.NewsArticle, theme: news_models.Theme
) -> bool:
    """Uses the LLM to identify whether a news article is relevant to a theme

    Args:
        news_article (json): a json object containing the news article
        theme (str): the theme to check relevance
        theme_description (str): the description of the theme

    Raises:
        Exception: When chatgpt does not follow the instructions properly

    Returns:
        bool: True if the news article is relevant to the theme, False otherwise
    """
    # Import the intructions for identifying relevance
    with open(r"news\filter_news_one_by_one.md", "r", encoding="UTF-8") as file:
        filter_news_results_Instruction = file.read()

        # Remove link from the news article
        article_without_link = {
            "title": news_article.title,
            "summary": news_article.summary,
        }
        # Convert results to string
        article_str = json.dumps(article_without_link, ensure_ascii=False)

        formatted_instruction = ChatGPT_BrowserBased.formatPromptWithArguments(
            filter_news_results_Instruction,
            {
                "__news_article_summary__": article_str,
                "__theme__": theme.title,
                "__theme_description__": theme.description,
            },
        )

        # Get the response from chatGPT
        response = chatgptcredentials.openai_client.beta.chat.completions.parse(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": formatted_instruction}],
            response_format=RelevanceSchema,
        )

        is_related = response.choices[0].message.parsed.is_related
        reason = response.choices[0].message.parsed.reason

    return is_related, reason


# Define the type for the progress callback function
ProgressCallback = Callable[[int, int, news_models.NewsArticle], None]


def check_article_is_processed(news_article: news_models.NewsArticle) -> bool:
    progress_file = "output/progress.json"
    if os.path.exists(progress_file):
        with open(progress_file, "r", encoding="UTF-8") as temp_file:
            processed_articles_dict = json.load(temp_file)
            processed_articles = [
                news_models.NewsArticle.from_dict(article_dict)
                for article_dict in processed_articles_dict
            ]
            for processed_article in processed_articles:
                if processed_article.title == news_article.title:
                    return True
    return False


def IdentifyRelevanceBatch(
    news_articles: List[news_models.NewsArticle],
    theme: news_models.Theme,
    progress_callback: ProgressCallback = None,
) -> List[news_models.NewsArticle]:
    logger = logging.getLogger(__name__)
    processed_articles = []
    total_articles = len(news_articles)

    for index, news_article in enumerate(news_articles):
        if check_article_is_processed(news_article):
            logger.info(f"Article {news_article.title} has been processed")
            continue

        logger.warning(f"Processing article: {news_article.to_dict()}")
        is_related, reason = IdenfityRelevance(
            news_models.NewsArticle.from_dict(news_article.to_dict()), theme
        )
        news_article.additional_info = {"is_relevant": is_related, "reason": reason}
        processed_articles.append(news_article)

        # Call the progress callback with the current progress
        if progress_callback:
            progress_callback(total_articles, processed_articles)

        # Log the progress
        logger.info(
            f"Processed article {index + 1}/{total_articles}: {news_article.title}"
        )

        time.sleep(0.2)

    return processed_articles


# Log progress
def log_progress(total: int, processed_articles: List[news_models.NewsArticle]):
    articles_dict = [article.to_dict() for article in processed_articles]
    with open("output/progress.json", "w", encoding="UTF-8") as temp_file:
        json.dump(articles_dict, temp_file, ensure_ascii=False, indent=4)
