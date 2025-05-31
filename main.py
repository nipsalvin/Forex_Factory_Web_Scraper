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
        dict: A dictionary containing date and events information
    """
    print('Scraping...')

    # Extract the date from the day breaker row
    date_element = soup.find('tr', class_='calendar__row calendar__row--day-breaker')
    date_text = "Date"  # Default fallback
    if date_element:
        date_cell = date_element.find('td', class_='calendar__cell')
        if date_cell:
            date_text = date_cell.get_text()

    # Define the target currencies and impact titles
    target_currencies = ['GBP', 'USD']
    impact_titles = ['High Impact Expected', 'Medium Impact Expected', 'Non-Economic']

    events_list = []

    all_impact_cells = soup.find_all('td', class_='calendar__cell calendar__impact')
    impact_cells = [impact_cell for impact_cell in all_impact_cells if impact_cell.find('span') and impact_cell.find('span').get('title') in impact_titles]

    event_time = None
    for impact_cell in impact_cells:
        currency_cell = impact_cell.find_previous_sibling('td', class_='calendar__cell calendar__currency')

        if currency_cell:
            currency = currency_cell.find('span').text.strip()  # Get the currency text
            # Get the time cell
            time_cell = currency_cell.find_previous_sibling('td', class_='calendar__cell calendar__time')
            # if the time cell is empty, use previous cell
            if time_cell.get_text(strip=True) != '':
                event_time = time_cell.get_text(strip=True) if time_cell else "No Time"

            if currency in target_currencies:
                # Get the event name
                news_cell = currency_cell.find_next_sibling('td', class_='calendar__cell calendar__event event')
                event_name = news_cell.get_text(strip=True) if news_cell else "No Event"

                # Create event info with time, currency, and name
                event_info = {
                    "name": event_name,
                    "time": event_time,
                    "currency": currency
                }

                events_list.append(event_info)

    # Return structured data with date and events
    result = {
        "date": date_text,
        "events": events_list if events_list else [{"name": "No News Found", "time": "N/A", "currency": "N/A"}]
    }

    print('Scraped!' + str(result))
    return result

def send_notification(data_dict):
    """
    Send a notification to the user.

    Args:
        data_dict (dict): A dictionary containing the news events with times.

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

    # Format the message according to the desired output format
    message_lines = []

    # Add the date
    message_lines.append(data_dict.get("date", "Date"))
    message_lines.append("")  # Empty line after Date

    # Process each event
    for event in data_dict.get("events", []):
        # Format: "time: Currency"
        message_lines.append(f"{event['time']}: {event['currency']}")
        # Format: "News_event" (replace spaces with underscores)
        event_name = event['name'].replace(' ', '_')
        message_lines.append(f"News_{event_name}")
        message_lines.append("")  # Empty line after each event

    # Remove the last empty line
    if message_lines and message_lines[-1] == "":
        message_lines.pop()

    # Print the formatted output to console
    formatted_output = "\n".join(message_lines)
    print("Formatted Output:")
    print(formatted_output)

    payload = {
        "text": formatted_output
    }

    try:
        response = requests.post(url, json=payload, headers=headers)
        print(f"Payload: {payload} \n Status Code: {response.status_code} \n >> Message sent")
    except Exception as e:
        print(f"Failed to send notification. Error: {e}")
        return



if __name__ == "__main__":
    base_url = "https://www.forexfactory.com/calendar?day=today"
    print(f"Scraping {base_url}")
    soup = get_filtered_page(base_url)
    data_dict = scrape_page(soup)
    send_notification(data_dict)
