from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
from time import sleep
import requests
import os

def get_filtered_page(base_url):
    """
    Set up the Selenium WebDriver and get the filtered page.

    Args:
        base_url (str): The base URL of the website.

    Returns:
        soup (BeautifulSoup): The parsed page source using BeautifulSoup.
        filtered_folders (list): The news folders with titles in news_folder_titles.
    """
    print('Going to ForexFactory.com...')
    chrome_options = Options()
    # chrome_options.add_argument("--headless")  # This argument configures Chrome to run in headless mode.
    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=chrome_options)
    driver.get(base_url)
    driver.maximize_window()

    sleep(5)

    # Get the page source
    soup = BeautifulSoup(driver.page_source, 'lxml')

    # Close the browser
    print('Soup Gotten and served!')
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
    print('Scraping...')
    data_dict = {}
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
                event = news_cell.text.strip() if news_cell else "No Event"

                # Append the event to the dictionary
                if currency in data_dict:
                    data_dict[currency].append(event)  # Append to existing list
                else:
                    data_dict[currency] = [event]  # Create a new list if key doesn't exist
    
    # If no news found, add a default message
    if not data_dict:
        data_dict['No News'] = ['No News Found']

    print('Scraped!' + str(data_dict))    
    return data_dict

def send_notification(data_dict):
    """
    Send a notification to the user.

    Args:
        data_dict (dict): A dictionary containing the news events.

    Returns:
        None
    """
    print('Sending notification...')
    url = "https://whin2.p.rapidapi.com/send"

    headers = {
        "content-type": "application/json",
        "X-RapidAPI-Key": os.getenv('X-RapidAPI-Key_WHATSAPP'),
        "X-RapidAPI-Host": os.getenv('X-RapidAPI-Host_WHATSAPP'),
    }

    payload = {
        "text": []
    }

    for currency, events in data_dict.items():
        payload["text"].append({
            "currency": currency,
            "events": events  # This will list all events for that currency
        })

    payload = {
    "text": "\n".join([f"{currency}: {', '.join(events)}" for currency, events in data_dict.items()])
    }

        
    try:
        response = requests.post(url, json=payload, headers=headers)
        print(f"Payload: {payload} \n Status Code: {response.status_code} \n >> Message sent")
    except Exception as e:
        print(f"Failed to send notification for {currency}. Error: {e}")
        return



if __name__ == "__main__":
    base_url = "https://www.forexfactory.com/calendar?day=today"
    soup = get_filtered_page(base_url)
    data_dict = scrape_page(soup)
    send_notification(data_dict)
