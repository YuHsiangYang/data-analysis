from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import pyperclip
from selenium.webdriver.common.by import By
import browser


def askGPT(prompt, chat_id=None):
    """This uses selenium to interact with ChatGPT and get the response to the prompt using google chrome remote debugging port at 9222

    Args:
        prompt (str): the prompt to ask
        instructions (str, optional): custom instructions that is to be followed by ChatGPT specific for the prompt. Defaults to None.

    Returns:
        string: ChatGPT response to the prompt
    """
    
    # Intialized the browser
    chrome_browser = browser.initialize_browser()
    chat_url = "https://chatGPT.com/"
    if chat_id:
        chat_url = f"https://chatGPT.com/c/{chat_id}"
    chrome_browser.get(chat_url)
    
    #Combine the instuctions and the prompt
    
    try:
        text_prompt = WebDriverWait(chrome_browser, 10).until(EC.visibility_of_element_located(("xpath", "//*[@id='prompt-textarea']")))
        
        lines = prompt.split("\n")
        
        for line in lines:
            text_prompt.send_keys(line)
            text_prompt.send_keys(Keys.SHIFT + Keys.ENTER)
        text_prompt.submit()#Submit to ChatGPT
        
        
        #Round up to the next even number, thi is to wait for the response, the number of article elements present in the page should always be even.
        article_count = len(chrome_browser.find_elements(By.TAG_NAME, "article"))
        next_even = article_count if article_count % 2 == 0 else article_count + 1
    
        
        
        # Wait for the response
        WebDriverWait(chrome_browser, 120).until(EC.visibility_of_element_located(("xpath", f"/html/body/div[1]/div[2]/main/div[1]/div[1]/div/div/div/div/article[{next_even}]/div/div/div[2]/div/div[2]/div/div")))
        
        
        # Get the response by pressing Ctrl + Shift + C
        body = WebDriverWait(chrome_browser, 10).until(EC.presence_of_element_located(("xpath", "/html/body")))
        body.send_keys(Keys.CONTROL + Keys.SHIFT + "C")
        
        response = pyperclip.paste()
        chat_id = chrome_browser.current_url.split("/c/")[1]
        
        return {
            "response": response,
            "chat_id": chat_id
        }
    except (Exception) as e:
        return e.message
    finally:
        # return "An error occured"
        pass


def customInstructions(prompt:str, arguments:dict, chat_id_input=None):
    """This function is used to provide custom instructions to ChatGPT for the prompt

    Args:
        prompt (str): the prompt to ask
        input_fields (list): list of input fields in the prompt
        input_values (list): list of input values for the input fields

    Returns:
        string: ChatGPT response to the prompt
    """
    #Get all the keys in the arguments
    inputfields = list(arguments.keys())
    for key in inputfields:
        prompt = prompt.replace(key, arguments[key])
    

    return askGPT(prompt, chat_id=chat_id_input)



# Example usage
if __name__ == "__main__":
    prompt = "Generate a JSON code for a list of 5 items"
    
    response = askGPT(prompt)
    print(response)