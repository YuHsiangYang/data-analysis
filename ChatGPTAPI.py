import json 
import re
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import pyperclip
from selenium.webdriver.common.by import By
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager


class ChatGPTResponse:
    def __init__(self, response:str, chat_id:str):
        self.response = response
        self.chat_id = chat_id

    def __str__(self):
        return f"{self.response}"

    def __repr__(self):
        return f"Response: {self.response}\nChat ID: {self.chat_id}"

#Start a browser and go to the ChatGPT website

def setup_remote_chrome_driver():
    """This initializes the browser with the remote debugging port at 9222.
    This function will automatically be called.

    Returns:
        WebDriver: the chrome driver initialized with the remote debugging port at 9222
    """
    # initialize the driver with the debugger address
    driver_options = Options()
    driver_options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")

    chrome_driver = webdriver.Chrome(service=Service(
        ChromeDriverManager().install()), options=driver_options)
    return chrome_driver


def GetChatGPTResponse(prompt, chat_id=None) -> ChatGPTResponse:
    """This uses selenium to interact with ChatGPT and get the response to the prompt using google chrome remote debugging port at 9222

    Args:
        prompt (str): the prompt to ask
        instructions (str, optional): custom instructions that is to be followed by ChatGPT specific for the prompt. Defaults to None.

    Returns:
        ChatGPTResponse: the response object from ChatGPT and the chat id
    """
    
    # Start the browser and go to the ChatGPT website
    browser = setup_remote_chrome_driver()
    
    chat_url = "https://chatGPT.com/"
    if chat_id:
        chat_url = f"https://chatGPT.com/c/{chat_id}"
    browser.get(chat_url)
    
    
    try:
        text_prompt = WebDriverWait(browser, 10).until(EC.visibility_of_element_located(("xpath", "//*[@id='prompt-textarea']")))
        
        lines = prompt.split("\n")
        
        for line in lines:
            text_prompt.send_keys(line)
            text_prompt.send_keys(Keys.SHIFT + Keys.ENTER)
        text_prompt.submit()#Submit to ChatGPT
        
        
        #Round up to the next even number, thi is to wait for the response, the number of article elements present in the page should always be even.
        article_count = len(browser.find_elements(By.TAG_NAME, "article"))
        next_even = article_count if article_count % 2 == 0 else article_count + 1
    
        # Wait for the response
        WebDriverWait(browser, 120).until(EC.visibility_of_element_located(("xpath", f"/html/body/div[1]/div[2]/main/div[1]/div[1]/div/div/div/div/article[{next_even}]/div/div/div[2]/div/div[2]/div/div")))
        
        
        # Get the response by pressing Ctrl + Shift + C
        body = WebDriverWait(browser, 10).until(EC.presence_of_element_located(("xpath", "/html/body")))
        body.send_keys(Keys.CONTROL + Keys.SHIFT + "C")
        
        response = pyperclip.paste()
        chat_id = browser.current_url.split("/c/")[1]
        
        return ChatGPTResponse(response, chat_id)
    
    except (Exception) as e:
        raise e
    

def formatPromptWithArguments(prompt:str, arguments:dict):
    """This function is used to provide custom instructions to ChatGPT for the prompt

    Args:
        prompt (str): the prompt to ask
        input_fields (list): list of input fields in the prompt
        input_values (list): list of input values for the input fields

    Returns:
        string: formatted prompt with the input values
    """
    #Get all the keys in the arguments
    inputfields = list(arguments.keys())
    for key in inputfields:
        prompt = prompt.replace(key, arguments[key])
    

    return prompt


def formulateQueries(searchPrompt) -> json:
    """Uses the LLM to formulate queries based on the search prompt

    Args:
        searchPrompt (string): the prompt from the user

    Raises:
        Exception: When chatgpt does not follow the instructions properly

    Returns:
        json: a json object containing the queries and the topics and subtopics
    """

    # This reads the flie that contains the instructions for formulating queries
    with open(r"instructions\formulate_queries.md", "r", encoding="UTF-8") as file:
        formulate_queries_Instruction = file.read()

        # Replace _prompt_ with the search prompt
        formulate_queries_Instruction = formulate_queries_Instruction.replace(
            "_prompt_", searchPrompt)

        # Uses google chrome to get the response from ChatGPT
        response_str = GetChatGPTResponse(formulate_queries_Instruction)["response"]

        json_pattern = re.compile(r'```json(.*?)```', re.DOTALL)
        match = json_pattern.search(response_str)

        if match:
            response_str = match.group(1)
        else:
            raise Exception(
                "No JSON code found in the response, ChatGPT may not follow the instructions properly" + "\n" + "prompt:" + searchPrompt)

        # Convert the response_str from string to json object
        response_json = json.loads(response_str)
        return response_json


def identify_relevance(news_article: json, theme: str, theme_description: str) -> list:
    """Uses predefined instructions to identify the relevance of the news article to the theme

    Args:
        news_article (json): _description_
        theme (str): _description_
        theme_description (str): _description_

    Raises:
        Exception: _description_

    Returns:
        list: _description_
    """
    
    # Import the intructions for identifying relevance
    with open(r"instructions\filter_news_one_by_one.md", "r", encoding="UTF-8") as file:
        filter_news_results_Instruction = file.read()

        # Remove link from the news article
        article_without_link = {
            "title": news_article["title"],
            "summary": news_article["summary"]
        }

        # Convert results to string
        results_str = json.dumps(article_without_link, ensure_ascii=False)

        response = GetChatGPTResponse(formatPromptWithArguments(filter_news_results_Instruction,
                                              {
                                                  "__news_article_summary__": results_str,
                                                  "__theme__": theme,
                                                  "__theme_description__": theme_description
                                              }))["response"]

        # Check if the response is a list
        json_pattern = re.compile(r'```json(.*?)```', re.DOTALL)
        match = json_pattern.search(response)

        if match:
            response = match.group(1)
        else:
            raise Exception(
                "No JSON code found in the response, ChatGPT may not follow the instructions properly" + response)

        response_json = json.loads(response)
        is_related = response_json["is_related"]

    return is_related


def filterResults(results: json, search_prompt: str) -> json:
    """Uses LLM to filter the relevant results from the search results

    Args:
        results (json): search results from duckduckgo in the format defined by duckduckgo_direct_results.json

    Returns:
        json: an array with the relevant results
    """
    results_per_batch = 10

    # This reads the flie that contains the instructions for filtering results
    with open(r"instructions\filter_results.md", "r", encoding="UTF-8") as file:
        filter_results_Instruction = file.read()

        # Replace _topic_ with the search_prompt
        filter_results_Instruction = filter_results_Instruction.replace(
            "_topic_", search_prompt)

        # Process the results batch by batch
        for i in range(0, len(results), results_per_batch):
            # Get the batch of results
            results_batch = results[i:i+results_per_batch]

            # Convert the batch of results to string
            results_str = json.dumps(results_batch, ensure_ascii=False)

            # Replace _searchresults_ with results
            filter_results_Instruction = filter_results_Instruction.replace(
                "_searchresults_", results_str)

            # Use ChatGPT to get the response
            response_str = GetChatGPTResponse(filter_results_Instruction)["response"]
            print(response_str)