import json
from src.news import newsFunctions_ChatGPTAPI
import logging
from src.news import newsFunctions_WebBased
import unittest
import sys
import os

from src.news import news_models
from src.llm import chatgptcredentials

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))


class TestNews_API(unittest.TestCase):
    def setUp(self):
        self.news_directory = (
            r"C:\Users\yuhsi\repos\web crawler (private version)\資料\資料交集_新"
        )
        logging.basicConfig(level=logging.INFO)
        self.theme = news_models.Theme(
            "空汙對馬拉松的影響",
            "本主題著重探討馬拉松與空氣污染之間的關係，特別是分析空汙如何影響馬拉松賽事、參賽者及其表現。僅收錄直接涉及這些內容的文章或資料，與主題無關者請勿納入。",
        )
        self.logger = logging.getLogger(__name__)
        self.news_articles = newsFunctions_WebBased.retrieve_news_articles_from_folder(
            self.news_directory
        )
        
    def test_api_function(self):
        client = chatgptcredentials.openai_client
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "user", "content": "hi there"},
            ],
            max_tokens=20,
        )
        self.logger.info(f"API Response: {response}")

    def test_retrieve_news_articles_from_folder(self):
        news_articles = newsFunctions_WebBased.retrieve_news_articles_from_folder(
            self.news_directory
        )
        self.logger.info(f"Number of news articles: {len(news_articles)}")

    def test_check_article_is_processed(self):
        self.logger.debug(f"Number of news articles: {len(self.news_articles)}")
        news_article = self.news_articles[0]
        is_processed = newsFunctions_ChatGPTAPI.check_article_is_processed(news_article)
        self.logger.debug(f"Is processed: {is_processed}")

    def test_IdentifyRelevanceBatch(self):
        self.logger.debug(f"Number of news articles: {len(self.news_articles)}")

        news_articles = newsFunctions_ChatGPTAPI.IdentifyRelevanceBatch(
            self.news_articles,
            self.theme,
            progress_callback=newsFunctions_ChatGPTAPI.log_progress,
        )

        # Dump the final results to a file
        with open("output/filtered_articles.json", "w", encoding="UTF-8") as temp_file:
            json.dump(
                [article.to_dict() for article in news_articles],
                temp_file,
                ensure_ascii=False,
                indent=4,
            )

    def test_relevance(self):
        news_articles = newsFunctions_WebBased.retrieve_news_articles_from_folder(
            self.news_directory
        )
        self.logger.debug(f"Number of news articles: {len(news_articles)}")
        relevance = newsFunctions_ChatGPTAPI.IdenfityRelevance(news_articles[0], self.theme)
        self.logger.info(f"Model response: {relevance}")
