from time import sleep
from selenium import webdriver
from bs4 import BeautifulSoup as soup
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, WebDriverException

chrome_options = Options()
chrome_options.add_argument("--headless=new")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")
# chrome_options.add_argument("--disable-blink-features=AutomationControlled")
# chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
# chrome_options.add_experimental_option("useAutomationExtension", False)

# instantiate browser driver
driver = webdriver.Chrome(options=chrome_options)
# driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")


class RestaurantScraper:
    driver = webdriver.Chrome(options=chrome_options)
    wait = WebDriverWait(driver, 10)

    def __init__(self) -> None:
        self.restaurant_index = 0

    def load_url_page(self, url: str) -> None:
        if not url:
            raise ValueError("Input a url to scrape data")

        print("Fetching url...")
        self.driver.get(url)
        sleep(2)
        print("URL fetched \n")

    def scrape_restaurants(self):
        restaurants = self.wait.until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, "a.vwVdIc")))
        sleep(2)
        print(f"{len(restaurants)} restaurants found")

        if self.restaurant_index < len(restaurants):
            curr_restaurant = restaurants[self.restaurant_index]
            self.restaurant_index += 1
            return curr_restaurant


class Extractor(RestaurantScraper):
    def __init__(self):
        super().__init__()

    def click_restaurant(self):
        restaurant = self.scrape_restaurants()
        if restaurant:
            restaurant.click()
            self.wait.until(
                EC.visibility_of_all_elements_located((By.CSS_SELECTOR, "div.kp-header")))
            sleep(3)
            
            # parse restaurant page to bs4
            page = soup(self.driver.page_source, "html.parser")
            return page

    def extract_restaurant_name(self):
        name = self.driver.find_element(By.XPATH, "//h2/span[not(@*)]").text
        print(f"Name: {name}")
        return name
    
    def extract_restaurant_address(self):
        address = self.driver.find_element(By.CSS_SELECTOR, "span.LrzXr").text
        print(f"Address: {address}")
        return address
    
    def extract_restaurant_nationality(self):
        nationality = self.driver.find_element(By.CSS_SELECTOR, "div.zloOqf span.YhemCb:nth-child(2)").text
        print(f"Nationality: {nationality}")
        return nationality

    def extract_restaurant_telephone_number(self):
        telephone_number = self.driver.find_element(By.XPATH, "//a/span[starts-with(text(), '+')]").text
        print(f"Telephone Number: {telephone_number}")
        return telephone_number

    def extract_restaurant_website(self):
        website_url = self.driver.find_element(By.CSS_SELECTOR, "a.mI8Pwc").get_attribute("href")
        print(f"Website: {website_url}")
        return website_url

    def extract_restaurant_instagram_link(self):
        insta_link_element = self.driver.find_element(By.XPATH, "//g-link/a[starts-with(@href, 'https://www.instagram.com/')]")
        insta_link = insta_link_element.get_attribute("href")
        print(f"Instagram Link: {insta_link}")
        return insta_link

    def extract_restaurant_facebook_link(self):
        facebook_link_element = self.driver.find_element(By.XPATH, "//g-link/a[starts-with(@href, 'https://www.facebook.com/')]")
        facebook_link = facebook_link_element.get_attribute("href")
        print(f"Facebook Link: {facebook_link}")
        return facebook_link

    def extract_restaurant_service_options(self):
        service_options = self.driver.find_element(By.XPATH, "//div[@style='margin:8px 16px']").text
        service_options = service_options.split(":")[1].strip()
        print(f"service options: {service_options}")
        return service_options
    
    def close_restaurant_page(self):
        self.driver.back()
        self.wait.until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, "a.vwVdIc")))
        sleep(2)


extractor = Extractor()
mainz = "https://www.google.com/search?client=firefox-b-d&sca_esv=596374102&tbs=lf:1,lf_ui:9&tbm=lcl&sxsrf=ACQVn0-2G5sPef-vv6QYCfU0u1cJpeTLYw:1704641224806&q=mainz+finthen+restaurant&rflfq=1&num=10&sa=X&ved=2ahUKEwil77G1y8uDAxUvaUEAHT3CDdgQjGp6BAgSEAE&biw=1525&bih=760&dpr=0.9#rlfi=hd:;si:;mv:[[49.997862299999994,8.1819598],[49.9712104,8.1506037]];tbs:lrf:!1m4!1u3!2m2!3m1!1e1!1m4!1u5!2m2!5m1!1sgcid_3pizza_1restaurant!1m4!1u5!2m2!5m1!1sgcid_3german_1restaurant!1m4!1u2!2m2!2m1!1e1!2m1!1e2!2m1!1e5!2m1!1e3!3sIAEqAkRF,lf:1,lf_ui:9"
extractor.load_url_page(mainz)
while extractor.click_restaurant():
    data = {
        "S/N": extractor.restaurant_index,
        "Name": extractor.extract_restaurant_name(),
        "Address": extractor.extract_restaurant_address(),
        "Nationality": extractor.extract_restaurant_nationality(),
        "Telephone Number": extractor.extract_restaurant_telephone_number(),
        "Website": extractor.extract_restaurant_website(),
        "Instagram Link": extractor.extract_restaurant_instagram_link(),
        "Facebook Link": extractor.extract_restaurant_facebook_link(),
        "Service Options": extractor.extract_restaurant_service_options()
    }

    print()
    print(data)
    extractor.close_restaurant_page
