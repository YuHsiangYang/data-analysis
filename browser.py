from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager


def initialize_browser():
    """This initializes the browser with the remote debugging port at 9222.

    Returns:
        WebDriver: the chrome driver initialized with the remote debugging port at 9222
    """
    # initialize the driver with the debugger address
    driver_options = Options()
    driver_options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")

    chrome_driver = webdriver.Chrome(service=Service(
        ChromeDriverManager().install()), options=driver_options)
    return chrome_driver
