# Airbnb Scraper

This project is a Python-based web scraper designed to extract data from the Airbnb.fr website. It uses Selenium for browser automation, allowing for the extraction of listing details and other information.

## Project Structure

The project is organized into the following files:

*   `config.py`: Contains configuration variables such as the path to the ChromeDriver, base URL, category URLs, and timeouts.
*   `browser.py`: Handles the setup and management of the Selenium WebDriver. This includes launching a browser instance and quitting the driver when complete.
*   `extractor.py`: Contains functions to extract specific data from the Airbnb webpage, like the `data-bootstrap` element, the categories, listing cards, etc.
*   `main.py`: Serves as the entry point for the scraper. It orchestrates the process, calling functions from other modules.
* `requirements.txt`: Contains a list of dependencies for the project.

## Requirements

*   Python 3.6+
*   Selenium (and other dependencies): Install using `pip`:
    ```bash
    pip install -r requirements.txt
    ```
*   ChromeDriver: Download the appropriate version for your Chrome browser and place it in the same directory as your python script.

## Usage

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/semahkadri/Scraper
    cd Scraper/airbnb_scraper
    ```
2.  **Install dependencies:**
     ```bash
     pip install -r requirements.txt
    ```
3.  **Set up ChromeDriver:** Ensure you have `chromedriver` (or the appropriate driver for your specific browser) in the `airbnb_scraper` directory or specify the path to your chromedriver using absolute path inside `config.py`
4.  **Run the scraper:**
    ```bash
    python main.py
    ```
    This will:
    * Open the specified Airbnb category page in a browser.
    * Extract the data from data-bootstrap balise.
    * Extract the categories available in the page.
    * Extract data from all listing cards on the page (title, host, dates, price).
     *Close the browser.
     * Prints the output in your terminal.
5. **Adjust Configurations (Optional)**

*   If needed, modify the variables in `config.py` to change the driver path, timeout, base URLs, etc.

## Key Features

*   **Modular Design:**  Code is organized into separate modules for better readability and maintainability.
*   **Docstrings:** Modules, functions, and methods are documented with docstrings.
*  **Clear output:** Extracted data is presented clearly in the terminal.
* **Explicit Waits:** Explicit waits are now used to handle dynamic content.
*   **Headless or visible mode:** can run the code in headless (fast) mode, or visible mode (for debugging).
*  **Flexibility:** Able to extract data for all listing cards.

## Important Considerations

*   **Website Changes:**  Airbnb may change its website structure, which could break the scraper. Be prepared to inspect the page and update selectors in `extractor.py` as needed.
*   **Terms of Service:** Use the code respectfully and ethically, adhering to Airbnb's terms of service. Do not overload their servers.
*   **Scalability:** This code focuses on a single page. For multi-page scraping you will have to improve the code.

## Contributing

Contributions and improvements are welcome. Feel free to submit a pull request!

**License**

This project is open source. (Add the license info you'd like to use, such as MIT License, Apache 2.0, etc.).