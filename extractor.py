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
    except Exception as e:
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
    """Extract data from listing cards, including the main photo."""
    try:
        WebDriverWait(driver, TIMEOUT_SECONDS).until(
            EC.presence_of_all_elements_located((By.XPATH, '//div[@data-testid="card-container"]'))
        )
        listing_elements = driver.find_elements(By.XPATH, '//div[@data-testid="card-container"]')
        listings_data = []

        for listing_element in listing_elements:
            title_element = listing_element.find_element(By.XPATH, './/div[@data-testid="listing-card-title"]').text
            host_element = listing_element.find_element(By.XPATH, './/div[@data-testid="listing-card-subtitle"]/span[1]').text
            price_element = listing_element.find_element(By.XPATH, './/span[@class="_11jcbg2"]').text
            image_element = listing_element.find_element(By.XPATH, './/picture/img')
            main_image_url = image_element.get_attribute('src')
            card_link_element = listing_element.find_element(By.XPATH, './/a[@aria-labelledby]')
            listing_url = card_link_element.get_attribute('href')

            listings_data.append({
                "title": title_element,
                "host": host_element,
                "price": price_element,
                "main_image_url": main_image_url,
                "listing_url": listing_url,
                "all_photos": [],  
                "location": "Location not found" 

            })
        return listings_data

    except Exception as e:
        print(f"Error extracting listings card data: {e}")
        return []
    
def extract_listing_location(driver):
    """Extracts the location of the listing."""
    location_text = "Location not found"
    try:
        location_selectors = ['.s1qk96pm', '._1t2xqmi']
        for selector in location_selectors:
            try:
                location_element = WebDriverWait(driver, 5).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, selector))
                )
                location_text = location_element.text.strip()
                if location_text:
                    break
            except TimeoutException:
                continue
    except Exception as e:
        print(f"Error extracting location: {e}")

    return location_text

def extract_listing_description(driver):
    """Extracts the 'À propos de ce logement' description."""
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

def extract_listing_photos(driver):
    """Extract all lodging photos from a listing detail page, excluding host images."""
    photos = []
    try:
        try:
            gallery_button = WebDriverWait(driver, TIMEOUT_SECONDS).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, 'button[data-testid="pdp-show-all-photos-button"]'))
            )
            gallery_button.click()
        except TimeoutException:
            print("Could not open photo gallery; falling back to visible photos only.")
        
        WebDriverWait(driver, TIMEOUT_SECONDS).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'img.i1ezuexe'))
        )
        
        photo_elements = driver.find_elements(By.CSS_SELECTOR, 'img.i1ezuexe')
        
        for photo in photo_elements:
            alt_text = photo.get_attribute('alt') or ""
            if "Profil utilisateur" in alt_text:
                continue
            photo_url = photo.get_attribute('src')
            if photo_url and photo_url not in photos:
                photos.append(photo_url)
                
        if photos:
            photos = photos[:-1]
                
        try:
            close_button = driver.find_element(By.CSS_SELECTOR, 'button[aria-label="Close"]')
            close_button.click()
        except Exception:
            pass
            
    except Exception as e:
        print(f"Error extracting photos: {e}")
    
    return photos


def extract_listing_comments(driver):
    """Extract all comments from a listing detail page using the 'r1bctolv' class."""
    comments = []
    try:
        comment_elements = driver.find_elements(By.CLASS_NAME, "r1bctolv")
        comments = [comment.text.strip() for comment in comment_elements if comment.text.strip()]
    except Exception as e:
        print(f"Error extracting comments: {e}")
    return comments

def extract_listing_rating(driver):
    """Extracts the rating from the listing detail page using the updated HTML structure."""
    rating = "Rating not found"
    try:
        rating_container = WebDriverWait(driver, TIMEOUT_SECONDS).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'div[data-testid="pdp-reviews-highlight-banner-host-rating"]'))
        )
        rating_element = rating_container.find_element(By.CSS_SELECTOR, "div[aria-hidden='true']")
        rating = rating_element.text.strip()
    except Exception as e:
        print(f"Error extracting rating: {e}")
    return rating

def find_next_page_button(driver):
    """Find next page button if it exists."""
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
