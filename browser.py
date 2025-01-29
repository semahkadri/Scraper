"""Sets up and manages the Selenium WebDriver."""

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import os
from config import DRIVER_PATH

def setup_driver(headless=False):
    """Sets up the Selenium WebDriver.

    Args:
       headless (bool, optional): whether the browser should be headless or not. Defaults to True.

    Returns:
        selenium.webdriver.chrome.webdriver.WebDriver: The Selenium WebDriver.
    """
    if os.path.exists("./chromedriver.exe"):
        driver_path = "./chromedriver.exe"
    elif os.path.exists("./chromedriver"):
       driver_path = "./chromedriver"    
    else:
        driver_path = r"C:\Users\semah\Desktop\aribnb\Scraper\chromedriver.exe"  

    service = Service(executable_path=driver_path)
    options = Options()
    if headless:
        options.add_argument("--headless")
    return webdriver.Chrome(service=service, options=options)


def close_driver(driver):
    """Closes the Selenium WebDriver.

    Args:
      driver: selenium.webdriver.chrome.webdriver.WebDriver: The Selenium WebDriver.
    """
    if driver:
        driver.quit()