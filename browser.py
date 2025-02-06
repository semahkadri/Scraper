from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import os
import json
from config import DRIVER_PATH

_http_log_ids = set()

def setup_driver(headless=False):
    """Sets up the Selenium WebDriver with HTTP traffic capture enabled.

    Args:
        headless (bool, optional): Run the browser in headless mode. Defaults to False.

    Returns:
        selenium.webdriver.Chrome: Configured Chrome WebDriver.
    """
    if os.path.exists("./chromedriver.exe"):
        driver_path = "./chromedriver.exe"
    elif os.path.exists("./chromedriver"):
        driver_path = "./chromedriver"
    else:
        driver_path = DRIVER_PATH  

    service = Service(executable_path=driver_path)
    options = Options()
    if headless:
        options.add_argument("--headless")

    options.set_capability("goog:loggingPrefs", {"performance": "ALL"})
    
    return webdriver.Chrome(service=service, options=options)

def close_driver(driver):
    """Closes the Selenium WebDriver.

    Args:
        driver (webdriver.Chrome): The Selenium WebDriver.
    """
    if driver:
        driver.quit()

def append_http_traffic(driver, output_file="http_traffic.json"):
    """Appends new HTTP traffic logs from the driver to the given file.
    
    This function compares the current logs with the logs already written (tracked
    by a global set) so that only new entries are appended. This allows you to see
    the file growing in real time.

    Args:
        driver (webdriver.Chrome): The Selenium WebDriver.
        output_file (str, optional): The filename to save logs. Defaults to "http_traffic.json".
    """
    global _http_log_ids
    try:
        logs = driver.get_log("performance")
    except Exception as e:
        print(f"Error getting performance logs: {e}")
        return

    new_logs = []
    for entry in logs:
        log_id = entry.get("timestamp")
        if log_id not in _http_log_ids:
            new_logs.append(entry)
            _http_log_ids.add(log_id)
    if new_logs:
        with open(output_file, "a", encoding="utf-8") as f:
            for entry in new_logs:
                f.write(json.dumps(entry) + "\n")
        print(f"Appended {len(new_logs)} new HTTP log entries to {output_file}")
