from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
from time import sleep
import requests

def get_page_links(base_url):
    # Set up the Selenium WebDriver
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # This argument configures Chrome to run in headless mode.
    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=chrome_options)
    driver.get(base_url)
        # Click on the filter element
    filter_element = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "li.calendar__filters.right.imagefade.noborder a.highlight.filters"))
    )
    filter_element.click()

if __name__== "__main__":
    base_url="https://www.forexfactory.com/"
    get_page_links(base_url)