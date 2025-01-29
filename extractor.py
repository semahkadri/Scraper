
"""Logic for extracting data from the Airbnb page."""
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import json
from config import TIMEOUT_SECONDS


def extract_data_bootstrap(driver):
    """Extract the data-bootstrap attribute

    Args:
        driver (selenium.webdriver.chrome.webdriver.WebDriver): The Selenium WebDriver.
    Returns:
        dict : data_bootstrap content in dictionary
    """

    try:
       data_bootstrap_element = driver.find_element(By.ID, 'data-bootstrap')
       if data_bootstrap_element.get_attribute("data-bootstrap") == "true":
          data_bootstrap = {}
       else:
          data_bootstrap_json = data_bootstrap_element.get_attribute('data-bootstrap')
          data_bootstrap = json.loads(data_bootstrap_json)
       return data_bootstrap
    except Exception as e :
       print(f"Could not extract data-bootstrap: {e}")
       return {}


def extract_categories(driver):
    """Extracts the categories from the Airbnb page.

    Args:
        driver (selenium.webdriver.chrome.webdriver.WebDriver): The Selenium WebDriver.

    Returns:
        list: A list of category texts.
    """
    categories = []
    try:
        WebDriverWait(driver, TIMEOUT_SECONDS).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'button[role="radio"][name="categoryScroller"]'))
        )
        categories_elements = driver.find_elements(By.CSS_SELECTOR, 'button[role="radio"][name="categoryScroller"]')
        categories = [category.text for category in categories_elements]
        print(f"Successfully extracted {len(categories)} categories.")  
    except TimeoutException:
        print("Timeout: Categories not found within the given time.") 
    except Exception as e:
        print(f"Error extracting categories: {e}") 

    return categories


def extract_listing_cards_data(driver):
    """Extract data from all listing cards on the Airbnb page.

    Args:
        driver (selenium.webdriver.chrome.webdriver.WebDriver): The Selenium WebDriver.

    Returns:
        list : A list of dictionaries each containing data of one listing card.
    """
    try:
      WebDriverWait(driver, TIMEOUT_SECONDS).until(
        EC.presence_of_all_elements_located((By.XPATH, '//div[@data-testid="card-container"]'))
      )
      listing_elements = driver.find_elements(By.XPATH, '//div[@data-testid="card-container"]')
      listings_data=[]

      for listing_element in listing_elements:
        title_element = listing_element.find_element(By.XPATH,'.//div[@data-testid="listing-card-title"]').text
        host_element = listing_element.find_element(By.XPATH,'.//div[@data-testid="listing-card-subtitle"]/span[1]').text
        date_element = listing_element.find_element(By.XPATH,'.//div[@data-testid="listing-card-subtitle"]/span[2]').text
        price_element = listing_element.find_element(By.XPATH,'.//span[@class="_11jcbg2"]').text

        listings_data.append({
            "title": title_element,
            "host": host_element,
            "dates": date_element,
            "price": price_element
        })
      return listings_data

    except Exception as e:
        print(f"Error extracting listings data: {e}")
        return []

def find_next_page_button(driver):
     """Find next page button if exist."""
     try:
        next_page_button = WebDriverWait(driver, TIMEOUT_SECONDS).until(
            EC.element_to_be_clickable((By.XPATH, '//nav[@aria-label="Pagination"]/a[last()]'))
        )
        return next_page_button
     except TimeoutException:
         print("Timeout: Next page button not found within the given time.")
         return None
     except Exception as e:
         print(f"Error finding next page button: {e}")
         return None