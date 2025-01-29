# main.py
"""Main script to scrape data from Airbnb."""

from browser import setup_driver, close_driver
from extractor import extract_categories, extract_listing_cards_data,extract_data_bootstrap
from config import CATEGORY_URL, TIME_SLEEP_SECONDS
import time


def main():
    """Main function to orchestrate the scraping process."""
    driver = setup_driver(headless=False)
    driver.get(CATEGORY_URL)
    data_bootstrap = extract_data_bootstrap(driver)
    print(data_bootstrap)

    categories = extract_categories(driver)
    print("\nExtracted categories:")
    print(categories)


    listing_cards_data = extract_listing_cards_data(driver)
    print("\nListing Cards Data:")
    for i, listing in enumerate(listing_cards_data):
     print(f"Listing {i+1}:")
     for key, value in listing.items():
       print(f"  {key}: {value}")



    time.sleep(TIME_SLEEP_SECONDS)

    close_driver(driver)


if __name__ == "__main__":
   main()