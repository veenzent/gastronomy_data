## G-Maps Gastronomy Data Scraper

This project provides a Python-based solution for scraping restaurant data from Google Maps search results and presenting it through a user-friendly web application.

**Features:**

* **Scrape Restaurant Data:** Extracts details like name, address, nationality, phone number, website, social media links, and service options from Google Maps listings.
* **Web Interface:** Offers a web application built with FastAPI for easy interaction.
* **Data Presentation:** Scraped data is displayed in a tabular format within the web app.
* **Data Download:** Download the extracted information as an Excel spreadsheet.

**Components:**

* **scraper.py file:**
  * Defines classes utilizing Selenium and BeautifulSoup for browser automation and HTML parsing.
  * Provides functionalities for:
      * Loading target Google Maps URL.
      * Navigating through restaurants on the page.
      * Extracting specific restaurant details using XPath and CSS selectors.
      * Handling potential exceptions (missing elements) gracefully.
* **main.py file:**
  * Integrates FastAPI for building the web application.
  * Leverages Jinja2 templates for user interface rendering.
  * Orchestrates scraping functionalities from `scraper.py`.
  * Provides routes for:
      * Home page (`/`).
      * Data scraping with user-provided URL (`/data-via-url`).
      * Downloading scraped data as an Excel file (`/download`).

**Requirements:**

* Python 3.x
* Libraries:
    * Selenium
    * webdriver_manager
    * beautifulsoup4
    * FastAPI
    * Jinja2
    * pandas


**Running the Application:**

1. Install dependencies using a requirements file (`pip install requirements.txt`).
3. Run the application from a terminal: `uvicorn main:app --reload`
4. Access the web app in your browser at http://localhost:8000/

**Disclaimer:**

* Google may throttle or block scraping attempts. Use this script responsibly and adhere to Google's Terms of Service.
* This project is intended for educational purposes only. Modifying it for commercial use might require additional licenses or agreements. 
