"""Main script to scrape data from Airbnb."""

from browser import setup_driver, close_driver
from extractor import extract_categories, extract_listing_cards_data,extract_data_bootstrap, find_next_page_button
from config import CATEGORY_URL, TIME_SLEEP_SECONDS
import time
import time
from selenium.common.exceptions import StaleElementReferenceException


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
      all_listings_data.extend(listings_data)
      try:
        next_button = find_next_page_button(driver)
        if next_button:
            driver.execute_script("arguments[0].click();", next_button)

            WebDriverWait(driver, 10).until(
                  EC.presence_of_element_located((By.CLASS_NAME, 'c1abgzgs'))
            )
            page_num +=1
        else:
           print("No Next Button Found")
           break
      except StaleElementReferenceException:
         print("StaleElementReferenceException catched, trying to find next button again.")
         try:
          next_button = find_next_page_button(driver)
          if next_button:
            driver.execute_script("arguments[0].click();", next_button)

            # Wait for the new page to load
            WebDriverWait(driver, 10).until(
               EC.presence_of_element_located((By.CLASS_NAME, 'c1abgzgs'))
            )
            page_num += 1
          else:
            print("No Next Button Found")
            break
         except:
             print("Still cannot find the next button, breaking")
             break
      except Exception as e:
          print(f"Error during pagination: {e}")
          break
    print("\nAll Listing Cards Data:")
    for i, listing in enumerate(all_listings_data):
        print(f" Listing {i+1}:")
        for key, value in listing.items():
            print(f"  {key}: {value}")


    time.sleep(TIME_SLEEP_SECONDS)

    close_driver(driver)


if __name__ == "__main__":
    main()