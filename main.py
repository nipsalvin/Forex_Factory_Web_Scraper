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
    # Set up the Selenium WebDriver
    # import ipdb; ipdb.set_trace()
    chrome_options = Options()
    # chrome_options.add_argument("--headless")  # This argument configures Chrome to run in headless mode.
    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=chrome_options)
    driver.get(base_url)
    driver.maximize_window()
    # Click on the filter element
    filter_element = WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "li.calendar__filters.right.imagefade.noborder a.highlight.filters"))
    )
    filter_element.click()
    
    # Select none on the filters
    currency_none_btn = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, '//*[@id="content"]/section[2]/div[3]/div/div/div/div/div[2]/div[2]/div/div[2]/div[1]/div[1]/div[2]/p/span/a[2]'))
    )
    currency_none_btn.click()
    impact_none_btn = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, '//*[@id="content"]/section[2]/div[3]/div/div/div/div/div[2]/div[2]/div/div[2]/div[1]/div[1]/div[1]/div[1]/div/p/span/a[2]'))
    )
    impact_none_btn.click()

    # Select the red folder
    red_folder = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, '//*[@id="content"]/section[2]/div[3]/div/div/div/div/div[2]/div[2]/div/div[2]/div[1]/div[1]/div[1]/div[1]/div/div/div[1]/div[2]/label/span'))
    )
    red_folder.click()

    # Select the orange folder
    orange_folder = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, '//*[@id="content"]/section[2]/div[3]/div/div/div/div/div[2]/div[2]/div/div[2]/div[1]/div[1]/div[1]/div[1]/div/div/div[2]/div[2]/label/span'))
    )
    orange_folder.click()

    # Select the grey folder
    grey_folder = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, '//*[@id="content"]/section[2]/div[3]/div/div/div/div/div[2]/div[2]/div/div[2]/div[1]/div[1]/div[1]/div[1]/div/div/div[4]/div[2]/label/span'))
    )
    grey_folder.click()

    # Select USD filter
    usd_filter = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, '//*[@id="content"]/section[2]/div[3]/div/div/div/div/div[2]/div[2]/div/div[2]/div[1]/div[1]/div[2]/div/div[2]/div[5]/div[2]/label'))
    )
    usd_filter.click()

    # Select GBP filter
    gbp_filter = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, '//*[@id="content"]/section[2]/div[3]/div/div/div/div/div[2]/div[2]/div/div[2]/div[1]/div[1]/div[2]/div/div[2]/div[2]/div[2]'))
    )
    gbp_filter.click()

    # Apply filters
    apply_filter_btn = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, '//*[@id="content"]/section[2]/div[3]/div/div/div/div/div[2]/div[2]/div/table/tbody/tr/td[3]/input[1]'))
    )
    import ipdb; ipdb.set_trace()
    # apply_filter_btn.send_keys("\n") #Not working
    # apply_filter_btn.click() #Not working

    # Try different methods to click the button
    try:
        # Method 1: Regular click
        apply_filter_btn.click()
    except:
        try:
            # Method 2: JavaScript click
            driver.execute_script("arguments[0].click();", apply_filter_btn)
        except:
            # Method 3: Action chains
            ActionChains(driver).move_to_element(apply_filter_btn).click().perform()

    # Trigger mousedown, mouseup, and click via JavaScript
    driver.execute_script("""
        var button = arguments[0];
        var mousedownEvent = new MouseEvent('mousedown', {bubbles: true, cancelable: true, view: window});
        var mouseupEvent = new MouseEvent('mouseup', {bubbles: true, cancelable: true, view: window});
        var clickEvent = new MouseEvent('click', {bubbles: true, cancelable: true, view: window});
        
        button.dispatchEvent(mousedownEvent);
        button.dispatchEvent(mouseupEvent);
        button.dispatchEvent(clickEvent);
    """, apply_filter_btn)


    sleep(5)

    news_folder_titles = ['High Impact Expected', 'Medium Impact Expected', 'Non-Economic']

    news_folders  = driver.find_elements(By.CSS_SELECTOR, '.icon[title]')

    if news_folders != []:
        filtered_folders = [folder for folder in news_folders if folder.get_attribute('title') in news_folder_titles]
    
    soup = BeautifulSoup(driver.page_source, 'lxml')

    driver.quit()

    return soup


if __name__== "__main__":
    base_url="https://www.forexfactory.com/calendar?day=today"
    soup = get_filtered_page(base_url)

