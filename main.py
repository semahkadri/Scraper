"""Main script to scrape Airbnb data with listing descriptions."""

from browser import setup_driver, close_driver
from extractor import extract_categories, extract_listing_cards_data, extract_data_bootstrap, find_next_page_button, extract_listing_description
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
    print("\nExtracted categories:")
    print(categories)

    page_num = 1
    while True:
        print(f"\nScraping page: {page_num}")
        listings_data = extract_listing_cards_data(driver)
        if not listings_data:
            print("No listings found on this page, ending scraping.")
            break

        for listing in listings_data:
            listing_url = listing['listing_url']
            listing_data_with_description = {}
            try:
                driver.execute_script("window.open('', '_blank');")  
                driver.switch_to.window(driver.window_handles[1])  
                driver.get(listing_url)  
                description = extract_listing_description(driver)  
                listing_data_with_description = listing.copy()
                listing_data_with_description['description'] = description  

            except TimeoutException:
                listing_data_with_description = listing.copy()
                listing_data_with_description['description'] = "Description not loaded (Timeout)"
                print(f"Timeout loading description for: {listing_url}")
            except Exception as e:
                listing_data_with_description = listing.copy()
                listing_data_with_description['description'] =  f"Description not loaded (Error: {e})"
                print(f"Error loading description for: {listing_url} - {e}")
            finally:
                all_listings_data.append(listing_data_with_description)
                driver.close()  
                driver.switch_to.window(driver.window_handles[0])  


        next_button = find_next_page_button(driver)
        if not next_button:
            print("No Next Button Found - End of Pagination")
            break

        try:
            WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'button[aria-label="Page suivante des catégories"]')))
            next_button.click()

            WebDriverWait(driver, 20).until(
                EC.staleness_of(driver.find_element(By.XPATH, '//div[@data-testid="card-container"][1]'))
            )
            WebDriverWait(driver, 20).until(
                EC.presence_of_element_located((By.XPATH, '//div[@data-testid="card-container"][1]'))
            )


            print(f"Navigated to page {page_num + 1} successfully.")
            page_num += 1

        except StaleElementReferenceException:
            print("StaleElementReferenceException, trying to find next button again...")
            next_button = find_next_page_button(driver)
            if next_button:
                WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'button[aria-label="Page suivante des catégories"]')))
                next_button.click()
                WebDriverWait(driver, 20).until(
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

    print("\nAll Listing Cards Data (Including Descriptions):")
    for i, listing in enumerate(all_listings_data):
        print(f" Listing {i+1}:")
        for key, value in listing.items():
            print(f"  {key}: {value}")

    close_driver(driver)


if __name__ == "__main__":
    main()