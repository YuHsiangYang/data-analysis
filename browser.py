from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys

def initialize_browser():
    #initialize the driver with the debugger address
    driver_options = Options()
    driver_options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")

    chrome_driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=driver_options)
    return chrome_driver