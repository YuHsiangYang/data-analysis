from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import json
import time
import math
import re
import utilities
import os
from selenium import webdriver
from tqdm import tqdm
import datetime


def crawl_keyword_date_range(keyword_input: str, start=datetime.date(2013, 1, 1), end=datetime.date(2023, 12, 31), interval=5) -> json:
    results = []
    for i in range(start.year, end.year, interval):
        start_date = datetime.date(i, 1, 1)
        end_date = datetime.date(i + interval, 1, 1)
        crawl_keyword(keyword_input, datetime.date.strftime(start_date, "%Y-%m-%d"), datetime.date.strftime(end_date, "%Y-%m-%d"))

def crawl_keyword(keyword_input: str, start_date="2013-01-01", end_date="2023-12-31") -> json:
    news_provider = "聯合新聞網"
    complete_news_collection = []
    page_index_current = 0
    
    
    #Check if temp file exists
    file_name = f"temp/temp_{news_provider}_{keyword_input}.json"
    if os.path.exists(file_name):
        with open(file_name, 'r', encoding="UTF-8") as f:
            progress = json.load(f)
            page_index_current = progress["current_page"]
            complete_news_collection = progress["news_array"]
    
    
    
    chrome_browser = webdriver.Chrome(options=webdriver.ChromeOptions().add_argument("--headless"))
    main_page_url = "https://udndata.com/ndapp/Index?cp=udn" # The main base URL for searching the keyword
    
    chrome_browser.get(main_page_url)
    WebDriverWait(chrome_browser, 10).until(
        EC.presence_of_all_elements_located((By.XPATH, '//*[@id="mainbar"]'))
        )#Wait for the page to load
    
    
    #Input the keyword in the field.
    keyword_input_element = chrome_browser.find_element(By.XPATH, '//*[@id="SearchString"]')
    keyword_input_element.send_keys(keyword_input)
    
    #Click on the radio button to search by date range
    search_date_range_RadioButton = chrome_browser.find_element(By.XPATH, '//*[@id="udnform"]/div[1]/div[2]/div[2]/div[1]/input')
    search_date_range_RadioButton.click()
    
    #Input the start date
    date_start_datePicker = chrome_browser.find_element(By.XPATH, '//*[@id="datepicker-start"]')
    date_start_datePicker.send_keys(start_date) #Date start to search
    
    #Input the end date
    date_end_datePicker = chrome_browser.find_element(By.XPATH, '//*[@id="datepicker-end"]')
    date_end_datePicker.send_keys(end_date) #Date end to search
    
    #After submitting the form, the page will reload to the search result page
    submit_form_btn = chrome_browser.find_element(By.XPATH, '//*[@id="udnform"]/button')
    submit_form_btn.click()
    
    #Get the number of results
    number_of_results = int(chrome_browser.find_element(By.XPATH, '//*[@id="mainbar"]/section/div[1]/span[2]').get_attribute("innerText"))
    print(number_of_results)
    results_per_page = 20
    #Get compute for total pages
    total_pages = math.ceil(number_of_results / results_per_page)
    with tqdm(total=total_pages, initial=page_index_current) as pbar:
        #Run the loop for the total pages
        while page_index_current <= total_pages:
            #Begin with the first page by getting the current url
            current_url = chrome_browser.current_url
            #Replace the page element in the url
            new_url = replace_page_number(current_url, page_index_current)
            
            chrome_browser.get(new_url)
        
            #Get the news elements
            news_elements_list = chrome_browser.find_elements(By.XPATH, '//*[@id="mainbar"]/section/div[6]/ul/li')
            
            for news_element in news_elements_list:
                title = news_element.find_element(By.TAG_NAME, "a").get_attribute("innerHTML")
                #Remove the digit from the title
                title = re.sub(r'^\d+\.', '', title)
                href = news_element.find_element(By.TAG_NAME, "a").get_attribute("href")
                summary = news_element.find_element(By.TAG_NAME, "p").get_attribute("innerText")
                publication_date_str = news_element.find_element(By.TAG_NAME, "span").get_attribute("innerText")
                #Find the publication date in publication_date_str
                date_match = re.search(r'\d{4}-\d{2}-\d{2}', publication_date_str)
                if date_match:
                    publication_date = date_match.group()
                else:
                    publication_date = ""
                
                news_info = {
                    "title": title,
                    "href": href,
                    "summary": summary,
                    "publication_date": publication_date
                }
                complete_news_collection.append(news_info)
            
            #Remove duplicates
            complete_news_collection = [dict(t) for t in {tuple(d.items()) for d in complete_news_collection}]
            
            #Dump the results to a temporary file
            utilities.dump_temp_results(complete_news_collection, keyword_input, page_index_current, news_provider)
            time.sleep(1)
            page_index_current += 1
            #Update the progress
            pbar.update(1)
        utilities.dump_temp_results(complete_news_collection, keyword_input, 0, news_provider)
    return complete_news_collection
        

def replace_page_number(url, page_number):
    return re.sub(r'page=\d+', f'page={page_number}', url)