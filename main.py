from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
from time import sleep
import requests

def get_filtered_page(base_url):
    """
    Set up the Selenium WebDriver and get the filtered page.

    Args:
        base_url (str): The base URL of the website.

    Returns:
        soup (BeautifulSoup): The parsed page source using BeautifulSoup.
        filtered_folders (list): The news folders with titles in news_folder_titles.
    """
    chrome_options = Options()
    # chrome_options.add_argument("--headless")  # This argument configures Chrome to run in headless mode.
    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=chrome_options)
    driver.get(base_url)
    driver.maximize_window()

    sleep(5)

    # Get the page source
    soup = BeautifulSoup(driver.page_source, 'lxml')

    # Close the browser
    driver.quit()

    return soup  # Return both soup and filtered folders

def scrape_page(soup):
    """
    Scrape the page source and return the relevant information.

    Args:
        soup (BeautifulSoup): The parsed page source using BeautifulSoup.

    Returns:
        list: A list of dictionaries where each dictionary contains the information
            of a news event.

    """
    # Define the target currencies and impact titles
    target_currencies = ['GBP', 'USD']
    impact_titles = ['High Impact Expected', 'Medium Impact Expected', 'Non-Economic']
    
    all_impact_cells =  soup.find_all('td', class_='calendar__cell calendar__impact')

    impact_cells = [impact_cell for impact_cell in all_impact_cells if impact_cell.find('span')['title'] in impact_titles]

    for impact_cell in impact_cells:
        currency_cell = impact_cell.find_previous_sibling('td', class_='calendar__cell calendar__currency')

        if currency_cell:
            currency = currency_cell.find('span').text.strip()  # Get the currency text
            if currency in target_currencies:
                news_cell = currency_cell.find_next_sibling('td', class_='calendar__cell calendar__event event')
                print(currency)
                print(news_cell)
            # break


if __name__ == "__main__":
    base_url = "https://www.forexfactory.com/calendar?day=today"
    soup = get_filtered_page(base_url)
