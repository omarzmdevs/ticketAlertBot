# TicketAlertBot
An adaptable web scraping tool for tracking ticket prices and sending targeted alerts via Telegram. Built to bypass detection with user-agent rotation and proxy support.

This repository contains a Python script designed to scrape ticket prices from a specific webpage and send Telegram notifications when certain conditions are met. While not intended as a fully polished tool for end-users, it serves as an example or skeleton for developers who wish to customize it to their own needs.

The idea originated when I wanted to purchase a ticket and noticed that the webpage offered notifications for new tickets but lacked filtering options for notifications based on my preferences. This inspired me to create my own solution while learning along the way.

## Features

### Ticket Price Monitoring
- Scrapes ticket prices from a webpage to find the lowest price available.
- Sends a notification when a price below a specified threshold is found.

### Telegram Integration
- Notifies users via Telegram bot when conditions are met or when the program encounters issues, such as bot detection screens.

### Randomization and Anti-Detection
- Supports a list of user agents and proxy servers to reduce the likelihood of being flagged as a bot.

### Error Handling and Notifications
- Provides error messages and status updates via Telegram for better monitoring of the program’s behavior.

## Getting Started

### Prerequisites
To use this project, you will need the following:
- Python 3.9+
- Libraries (install using `pip install`):
  - selenium
  - requests
  - python-dotenv
  - undetected-chromedriver

#### Environment Variables (store in a `.env` file):
- **BOT_TOKEN**: Telegram bot token obtained from BotFather.
- **CHAT_ID**: Chat ID for the Telegram bot (use a tool like GetIdsBot to find this).
- **CHROME_DRIVER_PATH** (optional): Path to your ChromeDriver executable.

#### ChromeDriver
- Download ChromeDriver from the official website and ensure it matches your installed Chrome version.
  
### Installation
1. Pip install requirements
2. Configure the .env file with your environment variables(BOT_TOKEN, CHAT_ID, CHROME_DRIVER_PATH).
3. Modify the script based on your context:
  - Target URL: Replace the URL in the URL variable with the page you want to scrape.
  - XPath or Class Names: Update the XPath or class names in the scraper to match the structure of your target webpage.
  - Threshold: Set a PRICE_THRESHOLD value suitable for your needs.

## Key Components

### Libraries and Tools
- **Selenium with Undetected ChromeDriver**  
  Used for web scraping while avoiding bot detection mechanisms. The `undetected_chromedriver` module is helpful for bypassing anti-bot systems.

- **Requests**  
  Used for sending Telegram messages via the Telegram Bot API.

- **dotenv**  
  Handles sensitive information like bot tokens and chat IDs using environment variables.

### Considerations

#### Randomization and Proxies
- **User Agents**: A list of user-agent strings is provided to simulate different devices and browsers, reducing the chance of detection.  
- **Proxies**: While optional, using a list of proxy servers is strongly recommended to distribute requests and avoid IP bans. Add proxies to the `PROXIES` variable.

### Customization
This script is not a final product but an adaptable framework. Developers are expected to:
- Update XPath/class selectors based on the webpage structure.  
- Adjust delays, user-agent lists, and proxy lists to suit their use case.

### Limitations
This project is designed for educational purposes and personal use, should not be used for commercial purposes or in violation of any website’s terms of service. The user assumes all responsibility for its usage.

