"""Main script to scrape Airbnb data with pagination."""

from browser import setup_driver, close_driver
from extractor import extract_categories, extract_listing_cards_data, extract_data_bootstrap, find_next_page_button
from config import CATEGORY_URL, TIME_SLEEP_SECONDS
import time
from selenium.common.exceptions import StaleElementReferenceException, ElementClickInterceptedException, TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By


def main():
    """Main function to orchestrate the scraping process with pagination."""
    driver = setup_driver(headless=False)
    driver.get(CATEGORY_URL)
    all_listings_data = []

    data_bootstrap = extract_data_bootstrap(driver)
    print(data_bootstrap)

    categories = extract_categories(driver)
    print("\nExtracted categories:", categories)

    page_num = 1
    while True:
        print(f"\nScraping page: {page_num}")
        listings_data = extract_listing_cards_data(driver)
        if not listings_data:
            print("No listings found on this page, ending scraping.")
            break
        all_listings_data.extend(listings_data)

        next_button = find_next_page_button(driver)

        if not next_button:
            print("No Next Button Found - End of Pagination")
            break

        try:
            WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.CSS_SELECTOR, 'button[aria-label="Page suivante des catégories"]')))
            WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'button[aria-label="Page suivante des catégories"]')))

            driver.execute_script("arguments[0].scrollIntoView(true);", next_button)
            time.sleep(2) 
            next_button.click()


            WebDriverWait(driver, 30).until(EC.title_contains("Paris - Logements"))


            print(f"Navigated to page {page_num + 1} successfully.")
            page_num += 1

        except StaleElementReferenceException:
            print("StaleElementReferenceException, trying to find next button again...")
            next_button = find_next_page_button(driver)
            if next_button:
                WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'button[aria-label="Page suivante des catégories"]')))
                next_button.click()
                WebDriverWait(driver, 30).until(
                    EC.presence_of_element_located((By.XPATH, '//div[@data-testid="card-container"][1]'))
                )
                page_num += 1
            else:
                print("No Next Button Found after exception, end pagination.")
                break

        except ElementClickInterceptedException as e:
                print(f"ElementClickInterceptedException catched {e} breaking the loop")
                break
        except TimeoutException as e:
            print(f"Timeout during page navigation, ending pagination. {e}")
            break
        except Exception as e:
            print(f"An unexpected error occurred during pagination: {e}")
            break

    print("\nAll Listing Cards Data:")
    for i, listing in enumerate(all_listings_data):
        print(f" Listing {i+1}:")
        for key, value in listing.items():
            print(f"  {key}: {value}")

    close_driver(driver)


if __name__ == "__main__":
    main()