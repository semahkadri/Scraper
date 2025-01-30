"""Logic for extracting data from the Airbnb page."""
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import json
from config import TIMEOUT_SECONDS


def extract_data_bootstrap(driver):
    """Extract the data-bootstrap attribute"""
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
    """Extracts the categories from the Airbnb page."""
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
    """Extract data from listing cards, now including PDP URLs."""
    try:
        WebDriverWait(driver, TIMEOUT_SECONDS).until(
            EC.presence_of_all_elements_located((By.XPATH, '//div[@data-testid="card-container"]'))
        )
        listing_elements = driver.find_elements(By.XPATH, '//div[@data-testid="card-container"]')
        listings_data = []

        for listing_element in listing_elements:
            title_element = listing_element.find_element(By.XPATH,'.//div[@data-testid="listing-card-title"]').text
            host_element = listing_element.find_element(By.XPATH,'.//div[@data-testid="listing-card-subtitle"]/span[1]').text
            date_element = listing_element.find_element(By.XPATH,'.//div[@data-testid="listing-card-subtitle"]/span[2]').text
            price_element = listing_element.find_element(By.XPATH,'.//span[@class="_11jcbg2"]').text
            image_element = listing_element.find_element(By.XPATH, './/picture/img')
            image_url = image_element.get_attribute('src')
            card_link_element = listing_element.find_element(By.XPATH, './/a[@aria-labelledby]')
            listing_url = card_link_element.get_attribute('href')

            listings_data.append({
                "title": title_element,
                "host": host_element,
                "dates": date_element,
                "price": price_element,
                "image_url": image_url,
                "listing_url": listing_url
            })
        return listings_data

    except Exception as e:
        print(f"Error extracting listings card data: {e}")
        return []


def extract_listing_description(driver):
    """Extracts the 'À propos de ce logement' description, using provided class name."""
    description_text = "Description not found"
    try:
        try:
            popup_close_button = WebDriverWait(driver, 5).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, 'button[aria-label="Fermer"]'))
            )
            popup_close_button.click()
            print("Translation pop-up dismissed.")
        except TimeoutException:
            print("Translation pop-up not found, proceeding without dismissing.")

        WebDriverWait(driver, TIMEOUT_SECONDS).until(
            EC.presence_of_element_located((By.CLASS_NAME, 'd1isfkwk')) 
        )
        description_element = driver.find_element(By.CLASS_NAME, 'd1isfkwk') 
        description_text = description_element.text

    except TimeoutException:
        print("Timeout: Description not found on listing detail page.")
    except NoSuchElementException:
        print("NoSuchElementException: Description element not found.")
    except Exception as e:
        print(f"Error extracting description from listing page: {e}")

    return description_text


def find_next_page_button(driver):
     """Find next page button if exist."""
     try:
        next_page_button = WebDriverWait(driver, TIMEOUT_SECONDS).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, 'button[aria-label="Page suivante des catégories"]'))
        )
        return next_page_button
     except TimeoutException:
         print("Timeout: Next page button not found within the given time.")
         return None
     except Exception as e:
         print(f"Error finding next page button: {e}")
         return None