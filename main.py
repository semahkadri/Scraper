import os
import json
import requests
import time
import re
from browser import setup_driver, close_driver
from extractor import (
    extract_categories, 
    extract_listing_cards_data, 
    extract_data_bootstrap, 
    find_next_page_button, 
    extract_listing_description,
    extract_listing_photos,
    extract_listing_comments,
    extract_listing_rating,
    extract_listing_location
)
from config import CATEGORY_URL, TIME_SLEEP_SECONDS
from selenium.common.exceptions import StaleElementReferenceException, ElementClickInterceptedException, TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

OUTPUT_DIR = "listings"

def save_listing(listing):
    """Save listing data and all photos in a folder with its title."""
    title = listing["title"].replace("/", "-").replace("\\", "-").strip()
    folder_path = os.path.join(OUTPUT_DIR, title)
    photos_path = os.path.join(folder_path, "photos")

    os.makedirs(folder_path, exist_ok=True)
    os.makedirs(photos_path, exist_ok=True)

    json_path = os.path.join(folder_path, "details.json")
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(listing, f, ensure_ascii=False, indent=4)

    if listing.get("main_image_url"):
        main_image_path = os.path.join(folder_path, "main_image.jpg")
        try:
            response = requests.get(listing["main_image_url"], stream=True)
            response.raise_for_status()
            with open(main_image_path, "wb") as img_file:
                for chunk in response.iter_content(1024):
                    img_file.write(chunk)
        except Exception as e:
            print(f"Failed to download main image for {title}: {e}")

    for i, photo_url in enumerate(listing.get("all_photos", []), 1):
        photo_path = os.path.join(photos_path, f"photo_{i}.jpg")
        try:
            response = requests.get(photo_url, stream=True)
            response.raise_for_status()
            with open(photo_path, "wb") as img_file:
                for chunk in response.iter_content(1024):
                    img_file.write(chunk)
            print(f"Successfully downloaded photo {i} for {title}")
        except Exception as e:
            print(f"Failed to download photo {i} for {title}: {e}")

def main():
    """Main function to orchestrate the scraping process with pagination."""
    driver = setup_driver(headless=False)
    driver.get(CATEGORY_URL)
    all_listings_data = []

    data_bootstrap = extract_data_bootstrap(driver)
    print("Data bootstrap extracted:")
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

        for idx, listing in enumerate(listings_data, 1):
            print(f"\nProcessing listing {idx} on page {page_num}")
            listing_url = listing['listing_url']
            listing_data_with_details = listing.copy()

            try:
                driver.execute_script("window.open('', '_blank');")
                driver.switch_to.window(driver.window_handles[1])
                driver.get(listing_url)

                print(f"Extracting details for: {listing['title']}")
                description = extract_listing_description(driver)
                
                if re.search(r'\blit\b', description.lower()) or re.search(r'\bchambre\b', description.lower()):
                    location = extract_listing_location(driver)
                    all_photos = extract_listing_photos(driver)
                    comments = extract_listing_comments(driver)
                    rating = extract_listing_rating(driver)

                    listing_data_with_details['description'] = description
                    listing_data_with_details['location'] = location
                    listing_data_with_details['all_photos'] = all_photos
                    listing_data_with_details['comments'] = comments
                    listing_data_with_details['rating'] = rating

                    print(f"Matched listing: {listing['title']}\nLocation: {location}\nPhotos: {len(all_photos)}\nComments: {len(comments)}\nRating: {rating}")
                    all_listings_data.append(listing_data_with_details)
                    save_listing(listing_data_with_details)
                else:
                    print(f"Skipped listing: {listing['title']} (Keywords 'lit' or 'chambre' not found in description)")
            except TimeoutException:
                listing_data_with_details['description'] = "Description not loaded (Timeout)"
                print(f"Timeout loading listing details for: {listing_url}")
            except Exception as e:
                listing_data_with_details['description'] = f"Description not loaded (Error: {e})"
                print(f"Error loading listing details for: {listing_url} - {e}")
            finally:
                driver.close()
                driver.switch_to.window(driver.window_handles[0])

        next_button = find_next_page_button(driver)
        if not next_button:
            print("No Next Button Found - End of Pagination")
            break

        try:
            WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, 'button[aria-label="Page suivante des catégories"]'))
            )
            next_button.click()
            WebDriverWait(driver, 20).until(
                EC.staleness_of(driver.find_element(By.XPATH, '//div[@data-testid="card-container"][1]'))
            )
            WebDriverWait(driver, 20).until(
                EC.presence_of_element_located((By.XPATH, '//div[@data-testid="card-container"][1]'))
            )
            print(f"Navigated to page {page_num + 1} successfully.")
            page_num += 1
            time.sleep(TIME_SLEEP_SECONDS)
        except Exception as e:
            print(f"Error during pagination: {e}")
            break

    print("\nScraping completed. All listings data, photos, comments, ratings, and locations have been saved.")
    close_driver(driver)

if __name__ == "__main__":
    main()
