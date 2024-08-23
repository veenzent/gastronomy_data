## Streamlit Gastronomy Data Scraper

This scraper leverages Streamlit to create a user-friendly web app for scraping gastronomy data (restaurant details) from Google Maps search results. It utilizes Selenium and BeautifulSoup for the core scraping functionality.

**Features:**

* **Streamlit Interface:** Provides an easy-to-use interface for entering the target Google Maps search URL.
* **Clear Instructions:** Guides users through the steps to obtain the required URL from Google Maps.
* **Data Scraping:** Scrapes restaurant details like name, address, nationality, phone number, website, social media links, and service options.
* **Error Handling:** Handles potential network issues and displays informative messages.
* **Progress Tracking:** Displays real-time progress as data is scraped.
* **Result Display:** Presents the scraped data in a clear tabular format within the web app.
* A downloadable csv format of scraped data upon scraping completion

**Requirements:**

* Python 3.x
* Streamlit
* Pandas
* selenium
* beautifulsoup4
* webdriver_manager

**Others:**
* checkout master branch's README file to read about the scraper.py script where the core scraping functionality is.

**Installation:**

```bash
pip install streamlit pandas selenium beautifulsoup4 webdriver_manager
```

**Running the App:**

1. Open a terminal, navigate to your script directory, and run:
    ```bash
    streamlit run streamlit_client.py
    ```

**Usage:**

1. Open the web app in your browser (usually http://localhost:8501).
2. Follow the on-screen instructions to obtain the target URL from Google Maps.
3. Paste the URL into the text input field and click "Scrape".
4. The app will display real-time progress as it scrapes data.
5. Once completed, the scraped data will be presented with a csv format download icon in a table format within the web app.

**Disclaimer:**

* Google may throttle or block scraping attempts. Use this script responsibly and adhere to Google's Terms of Service.
* This script is for educational purposes only. Modifying it for commercial use might require additional licenses or agreements.

**Additional Notes:**

* The script utilizes a limit of 10 scraped restaurants to avoid overwhelming Google and triggering CAPTCHAs. 
* Feel free to adjust this limit if needed, but be mindful of Google's scraping guidelines.

This Streamlit app provides a convenient way to scrape gastronomy data from Google Maps, simplifying the process and offering a user-friendly experience.