from src.llm import ChatGPT_BrowserBased
import src.news.news_models as news_models
import json
import re
import os
from typing import Callable, List
import logging


def retrieve_news_articles_from_folder(directory) -> list[news_models.NewsArticle]:
    news_articles = []
    for root, dirs, files in os.walk(directory):
        for file_name in files:
            if file_name.endswith(".json"):
                file_path = os.path.join(root, file_name)
                news_articles.extend(retrieve_news_articles_from_file(file_path))
                

    return news_articles

def retrieve_news_articles_from_file(file_path) -> list[news_models.NewsArticle]:
    articles = []
    with open(file_path, "r", encoding="UTF-8") as file:
        try:
            news_articles_in_a_file = json.loads(file.read())
        except json.JSONDecodeError:
            logger = logging.getLogger(__name__)
            logger.error(f"Invalid JSON in file: {file_path}")

        for news_article in news_articles_in_a_file:
            try:
                news_article["keywords"] = file.name.split(".")[0].split("_")[2].split(" ")
                news_article["news_provider"] = file.name.split(".")[0].split("_")[1]
            except IndexError:
                pass
            news_article["filename"] = file.name.split(".")[0]
            articles.append(news_models.NewsArticle.from_dict(news_article))
            
    return articles

def IdenfityRelevance(news_article: news_models.NewsArticle, theme: news_models.Theme) -> bool:
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
    logger = logging.getLogger(__name__)
    # Import the intructions for identifying relevance
    with open(r"news\filter_news_one_by_one.md", "r", encoding="UTF-8") as file:
        filter_news_results_Instruction = file.read()

        # Remove link from the news article
        article_without_link = {
            "title": news_article.title,
            "summary": news_article.summary
        }

        # Convert results to string
        results_str = json.dumps(article_without_link, ensure_ascii=False)

        response = ChatGPT_BrowserBased.GetChatGPTResponse(ChatGPT_BrowserBased.formatPromptWithArguments(filter_news_results_Instruction, {
            "__news_article_summary__": results_str,
            "__theme__": theme.title,
            "__theme_description__": theme.description
        })).response

        # Check if the response is in JSON format
        json_pattern = re.compile(r'```json(.*?)```', re.DOTALL)
        match = json_pattern.search(response)
        
        if match:
            #Find the JSON code in the response
            response = match.group(1)
        else:
            raise Exception(
                "No JSON code found in the response, ChatGPT may not follow the instructions properly" + response)
        
        logger.info(f"Response: {response}")
        
        
        try:
            response_json = json.loads(str.lower(response))
            is_related = response_json["is_related"]
        except json.JSONDecodeError:
            logger.error(f"Failed to decode JSON: {response}")
    
    return is_related


# Define the type for the progress callback function
ProgressCallback = Callable[[int, int, news_models.NewsArticle], None]


def IdentifyRelevanceBatch(news_articles: List[news_models.NewsArticle], theme: news_models.Theme, progress_callback: ProgressCallback = None) -> List[news_models.NewsArticle]:
    logger = logging.getLogger(__name__)
    processed_articles = []
    total_articles = len(news_articles)
    
    for index, news_article in enumerate(news_articles):
        logger.warning(f"Processing article: {news_article.to_dict()}")
        #Check if the article is processed
        with open("output/progress.json", "r", encoding="UTF-8") as temp_file:
            processed_articles_dict = json.load(temp_file)
            processed_articles = [news_models.NewsArticle.from_dict(article_dict) for article_dict in processed_articles_dict]
            if news_article in processed_articles:
                continue
        
        
        relevance = IdenfityRelevance(news_models.NewsArticle.from_dict(news_article.to_dict()), theme)
        news_article.additional_info = {
            "is_relevant": relevance
        }
        processed_articles.append(news_article)
        
        # Call the progress callback with the current progress
        if progress_callback:
            progress_callback(total_articles, processed_articles)
        
        # Log the progress
        logger.info(f"Processed article {index + 1}/{total_articles}: {news_article.title}")
    
    return processed_articles

# Log progress
def log_progress(total: int, processed_articles: List[news_models.NewsArticle]):
    articles_dict = [article.to_dict() for article in processed_articles]
    with open("output/progress.json", "w", encoding="UTF-8") as temp_file:
        json.dump(articles_dict, temp_file, ensure_ascii=False, indent=4)