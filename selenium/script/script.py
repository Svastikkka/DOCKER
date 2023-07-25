from concurrent.futures import ThreadPoolExecutor
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from pymongo import MongoClient
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import logging
import time


# Set up logging to a file inside the 'logs' directory
logging.basicConfig(filename='logs/scraping.log', level=logging.INFO, format='%(asctime)s - %(levelname)s: %(message)s')


def scrape_page(page):
    chrome_options = Options()
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--headless")
    driver = webdriver.Remote(command_executor='http://selenium-hub:4444/wd/hub', options=chrome_options,)
    driver.get(f"http://quotes.toscrape.com/page/{page}/")
    client = MongoClient('mongodb://mongodb:27017/')
    db = client['mcs_assignment']
    collection = db['quotes']

    for i in range(1, 11):
        quote_xpath = f"/html/body/div[1]/div[2]/div[1]/div[{i}]/span[1]"
        author_xpath = f"/html/body/div[1]/div[2]/div[1]/div[{i}]/span[2]/small"
        quote_element = driver.find_element(By.XPATH, quote_xpath)
        quote_text = quote_element.text
        author_element = driver.find_element(By.XPATH, author_xpath)
        author_name = author_element.text

        # Use logging instead of print
        logging.info(f"Page: {page} - Quote: {quote_text}")
        logging.info(f"Page: {page} - Author: {author_name}")
        print()

        document = {
            'quote_id': (page - 1) * 10 + i,
            'quote': quote_text,
            'author': author_name
        }
        collection.insert_one(document)

    driver.quit()

if __name__ == "__main__":
    num_pages = 10
    num_instances = 2

    # Add a brief delay before starting the ThreadPoolExecutor
    time.sleep(20)

    with ThreadPoolExecutor(max_workers=num_instances) as executor:
        pages_per_instance = num_pages // num_instances
        instances = range(1, num_instances + 1)
        executor.map(scrape_page, [page for instance in instances for page in range((instance - 1) * pages_per_instance + 1, instance * pages_per_instance + 1)])
