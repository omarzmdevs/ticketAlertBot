import os
import requests
from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
import undetected_chromedriver as uc
import time
import random

load_dotenv()


def send_telegram_message(bot_token, chat_id, message):
    """
    Sends a message to a Telegram bot.
    
    Args:
        bot_token: You can get one starting a chat with BotFather on Telegram.
        chat_id:  Which can be retrieved using bots like GetIdsBot.
        message: Message to send.
    """
    
    url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    payload = {
        "chat_id": chat_id,
        "text": message
    }

    try:
        response = requests.post(url, json=payload)
        if response.status_code == 200:
            print("Sent successfully.")
        else:
            print(f"Error sending the message: {response.status_code}, {response.text}, to {chat_id}")
    except Exception as e:
        print(f"Connection error: {e}")


def init_driver(user_agents, proxies=None, prefs=None):
    """
    Initializes the WebDriver with given user agents, proxies, and preferences.
    
    Args:
        user_agents (list): A list of user-agent strings.
        proxies (list): A list of proxies (optional but highly recommended).
        prefs (dict): Preferences for the browser (optional).

    Returns:
        WebDriver: Configured WebDriver instance.
    """
    selected_user_agent = random.choice(user_agents)
    
    chrome_options = uc.ChromeOptions()
    chrome_options.add_argument("--headless") 
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--window-size=1920,1080")
    chrome_options.add_argument(f"user-agent={selected_user_agent}")
    chrome_options.add_argument("--log-level=1")

    
    if proxies:
        proxy = random.choice(proxies)
        chrome_options.add_argument(f"--proxy-server={proxy}")

    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    chrome_options.add_experimental_option("useAutomationExtension", False)

    if prefs:
        chrome_options.add_experimental_option("prefs", prefs)

    chrome_driver_path = os.getenv("CHROME_DRIVER_PATH", "chromedriver")
    service = Service(chrome_driver_path)
    driver = webdriver.Chrome(service=service, options=chrome_options)

    driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
    
    return driver

##if you are aiming to scale this code, consider moving this class apart and importing here for a better modularization
class TicketScraper:
    def __init__(self):
        self.last_current_price = None

    def scrape_tickets(self, driver, url, price_threshold, bot_token, chat_id):
        """
        Scrapes ticket prices and sends a Telegram notification to a bot if conditions are met.
        Also detects bot-check screens and sends an alert if encountered.

        Args:
            driver: Selenium WebDriver instance.
            url: URL of the page to scrape.
            price_threshold: Price threshold for sending notifications.
            bot_token: Telegram bot token.
            chat_id: Telegram chat ID.
        
        Returns:
            bool: True if the program should continue, False otherwise.
        """
        try:
            sleep_time = random.uniform(5, 15)   # Random delay between 5 and 15 seconds
            driver.get(url)

            # Wait until the DOM is fully loaded
            driver.implicitly_wait(10 + sleep_time)
            
            try:
                click_button = driver.find_element(By.XPATH, '//button[contains(text(), "Click")]') # Adapt to your context
                if click_button:
                    send_telegram_message(
                        bot_token=bot_token,
                        chat_id=chat_id,
                        message="Program stopped: Bot detection screen detected."
                    )
                    print("Bot detection screen detected. Exiting...")
                    time.sleep(30)
                    return False
            except Exception:
                pass  


            # Extract price information or any other data from the page
            tickets = driver.find_elements(By.CLASS_NAME, 'css-14yessp.ebnsu0d0')

            if tickets:
                # Take the first ticket, that is the lowest 
                first_ticket = tickets[0]
                price_text = first_ticket.text.strip()  # Remove spaces at the beginning and end

                if price_text:
                    # Clean the text to extract numeric price. Adapt to context
                    price_cleaned = price_text.replace('€', '').replace('/ ticket', '').replace(',', '.').strip()

                    try:
                        current_price = float(price_cleaned)  # Price string to float
                        print(f"Price found: €{current_price}")

                        # Notify if the current price meets conditions
                        if current_price <= price_threshold and (
                            self.last_current_price is None or current_price < self.last_current_price
                        ):
                            send_telegram_message(
                                bot_token=bot_token,
                                chat_id=chat_id,
                                message=f"New lowest price: {current_price}€"
                            )
                            self.last_current_price = current_price  # Update current_price attribute of the class
                        else:
                            print("No price below the threshold or lower than the last price was found.")
                    except ValueError:
                        print(f"Error converting the price: {price_cleaned}")
            else:
                print("No tickets available.")

            """ # Send a heartbeat notification indicating the program is still running. Just for checks if necessary.
            send_telegram_message(
                bot_token=bot_token,
                chat_id=chat_id,
                message="Program is running and checking for prices."
            ) """

            return True

        except Exception as e:
            send_telegram_message(
                bot_token=bot_token,
                chat_id=chat_id,
                message=f"Program stopped due to an error: {e}"
            )
            print(f"Error trying to retrieve data: {e}")
            return False

### MAIN ###
if __name__ == "__main__":
    # Load configuration from .env
    BOT_TOKEN = os.getenv("BOT_TOKEN")  
    CHAT_ID = os.getenv("CHAT_ID")  

    USER_AGENTS = [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.5672.63 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36",
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.96 Safari/537.36",
        "Mozilla/5.0 (iPhone; CPU iPhone OS 14_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0 Mobile/15E148 Safari/604.1",
        "Mozilla/5.0 (iPad; CPU OS 13_4 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.1.1 Mobile/15E148 Safari/604.1",
    ]

    PREFS = {
        "profile.managed_default_content_settings.images": 2,  # Block images for faster loading
        "credentials_enable_service": False,                  # Disable credential prompts
        "profile.password_manager_enabled": False,            # Disable password manager
    }

    PROXIES = []  # Add proxy list if needed (RECOMMENDED)

    URL = "https://www.ticketswap.com/event/riverland-warm-up/689b58a0-3572-4e0d-97dd-9f1de09d6f56"
    PRICE_THRESHOLD = 70

    driver = init_driver(user_agents=USER_AGENTS, proxies=PROXIES, prefs=PREFS)
    scraper = TicketScraper()  # Instantiate the scraper
    
    

    try:
        while True:
            if not scraper.scrape_tickets(driver, URL, PRICE_THRESHOLD, BOT_TOKEN, CHAT_ID):
                break
            time.sleep(random.uniform(60, 120))  # Wait between 1 and 2 minutes before reloading
    finally:
        driver.quit()
