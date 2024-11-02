# Objective
# Example URL: https://tw.nextapple.com/search/跑步/35

# 35 is the page number
# Change to the next page by changing the number
# Change until the page shows no results, this means all of the results have been recorded

# JS selector for selecting the articles


# At the end remove all duplicates per search and turn that into a JSON file
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
import selenium.common.exceptions
from selenium.webdriver.support import expected_conditions as EC
import json
import utilities
from selenium.webdriver import ChromeOptions


def crawl_keyword(keyword_input: str, progress_file="") -> json:
    browser_options = ChromeOptions()
    browser_options.add_argument("--headless=new")
    chrome_browser = webdriver.Chrome(options=browser_options)
    # Add the page number at the end
    base_url = f"https://tw.nextapple.com/search/{keyword_input}"
    news_provider = "蘋果日報"

    HasContent = True
    page_index_count = 0
    news_array = []

    # Check for previous progress
    file_name = f"temp/temp_{news_provider}_{keyword_input}.json"
    if os.path.exists(file_name):
        with open(file_name, "r", encoding="UTF-8") as progress_file:
            progress_json = json.load(progress_file)
            news_array = progress_json["news_array"]
            page_index_count = progress_json["current_page"]

    while HasContent is True:
        chrome_browser.get(f"{base_url}/{page_index_count}")
        try:
            # Check if this page has content
            chrome_browser.find_element(
                By.XPATH, '//*[@id="main-content"]/div/p')
            break
        except selenium.common.NoSuchElementException:
            pass

        try:
            WebDriverWait(chrome_browser, 10).until(
                EC.presence_of_all_elements_located(
                    (By.XPATH, '//*[@id="main-content"]/div'))
            )
        except selenium.common.TimeoutException:
            print("Timed out waiting for page to load")
            HasContent = False
            break

        news_elements = chrome_browser.find_elements(
            By.XPATH, '//*[@id="main-content"]/div/article')

        for index in range(len(news_elements)):
            try:
                link = news_elements[index].find_element(
                    By.CLASS_NAME, "post-title").get_attribute("href")
                title = news_elements[index].find_element(
                    By.CLASS_NAME, "post-title").get_attribute("innerText")
                publication_date = news_elements[index].find_element(
                    By.CLASS_NAME, "post-meta").find_element(By.TAG_NAME, "time").get_attribute("innerText")
                summary = news_elements[index].find_element(
                    By.TAG_NAME, "p").get_attribute("innerHTML")

                news_info = {
                    "title": title,
                    "href": link,
                    "publication_date": publication_date,
                    "summary": summary
                }

                news_array.append(news_info)
                print(news_info)
            except selenium.common.NoSuchElementException:
                # print("Link not found")
                pass

        # Remove duplicates
        news_array = [dict(t) for t in {tuple(d.items()) for d in news_array}]

        utilities.dump_temp_results(
            news_array, keyword_input, page_index_count, "蘋果日報")

        page_index_count += 1

    return news_array
