import unittest
import logging
import json
import sys
import os
sys.path.insert(0, os.path.abspath(
    os.path.join(os.path.dirname(__file__), '..')))

import config
import LLM

class test_GeneratePerformance(unittest.TestCase):
    def setUp(self):
        self.theme_description = "主要是需要了解馬拉松和空汙的關係，以及空汙對馬拉松的影響，如果文章沒有提到這些或是跟這些無關，就不要放進來"
        self.theme = "馬拉松跟空汙的關係"

        # Configure the logger
        logging.basicConfig(
            level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        self.logger = logging.getLogger()

        # If the LLM identifies correctly, then variables below should be true.
        self.results_related = []
        self.results_unrelated = []
        self.results_mixed = []

        self.mixed_results_answers = []

    def test_generate_mixed_results(self):
        # import both related and unrelated articles
        with open(os.path.join(r"資料\新聞相關性測試", config.NewsProvider.UDN_NEWS.value, "related.json"), "r", encoding="UTF-8") as file:
            related_articles = json.load(file)
            for article in related_articles:
                article['is_related'] = True

        with open(os.path.join(r"資料\新聞相關性測試", config.NewsProvider.UDN_NEWS.value, "unrelated.json"), "r", encoding="UTF-8") as file:
            unrelated_articles = json.load(file)
            for article in unrelated_articles:
                article['is_related'] = False

        # combine the articles
        mixed_articles = related_articles + unrelated_articles

        # shuffle the articles
        import random
        random.shuffle(mixed_articles)

        # store the answers to a variable
        self.mixed_results_answers = mixed_articles

        # store the answers to a file
        with open(os.path.join(r"資料\新聞相關性測試", config.NewsProvider.UDN_NEWS.value, "mixed_answers.json"), "w", encoding="UTF-8") as file:
            json.dump(self.mixed_results_answers, file, ensure_ascii=False)

        mixed_results = []
        # generate the mixed results
        for article in mixed_articles:
            news_article = {
                "title": article["title"],
                "href": article["href"],
                "summary": article["summary"],
                "publication_date": article["publication_date"]
            }

            mixed_results.append(news_article)

        # write the mixed results to a file
        with open(os.path.join(r"資料\新聞相關性測試", config.NewsProvider.UDN_NEWS.value, "mixed.json"), "w", encoding="UTF-8") as file:
            json.dump(mixed_results, file, ensure_ascii=False)

    def test_related_articles(self):
        # Import the results for related articles
        with open(os.path.join(r"資料\新聞相關性測試", config.NewsProvider.UDN_NEWS.value, "related.json"), "r", encoding="UTF-8") as file:
            news_articles = json.load(file)
            for news_article in news_articles:
                is_related = LLM.identify_relevance(
                    news_article, self.theme, self.theme_description)
                self.results_related.append(is_related)
                # break

        self.logger.debug(f"Related results: {self.results_related}")

    def test_unrelated_articles(self):

        # Import the results for related articles
        with open(os.path.join(r"資料\新聞相關性測試", config.NewsProvider.UDN_NEWS.value, "unrelated.json"), "r", encoding="UTF-8") as file:
            news_articles = json.load(file)
            for news_article in news_articles:
                is_related = LLM.identify_relevance(
                    news_article, self.theme, self.theme_description)
                self.results_unrelated.append(is_related)

        self.logger.debug(f"Unrelated results: {self.results_unrelated}")

    def test_mixed_articles(self):
        # Import the results for related articles
        with open(os.path.join(r"資料\新聞相關性測試", config.NewsProvider.UDN_NEWS.value, "unrelated.json"), "r", encoding="UTF-8") as file:
            news_articles = json.load(file)
            for news_article in news_articles:
                is_related = LLM.identify_relevance(
                    news_article, self.theme, self.theme_description)
                self.results_mixed.append(is_related)
                # # check with the answers
                # # Import the answers
                # with open(os.path.join(r"資料\新聞相關性測試", config.NewsProvider.UDN_NEWS.value, "mixed_answers.json"), "r", encoding="UTF-8") as file:
                #     answers = json.load(file)
                #     for answer in answers:
                #         if answer['title'] == news_article['title']:
                #             self.results_mixed.append(
                #                 answer['is_related'] == is_related)
        self.logger.debug(f"Mixed results: {self.results_mixed}")

    def test_generate_performance(self):
        # Generate the performance
        performance = {
            "related": sum(self.results_related),
            "unrelated": sum(self.results_unrelated),
            "mixed": self.results_mixed
        }

        # write the performance to a file
        with open(os.path.join(r"資料\新聞相關性測試", config.NewsProvider.UDN_NEWS.value, "performance.json"), "w", encoding="UTF-8") as file:
            json.dump(performance, file, ensure_ascii=False)


if __name__ == '__main__':
    unittest.main()
