import csv
from time import sleep
from fastapi import FastAPI
from fastapi.responses import FileResponse
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import StaleElementReferenceException, NoSuchElementException



chrome_options = Options()
chrome_options.add_argument("--headless=new")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")
# chrome_options.add_argument("--disable-blink-features=AutomationControlled")
# chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
# chrome_options.add_experimental_option("useAutomationExtension", False)

# instantiate browser driver
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
# driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")


# url = "https://www.google.com/search?client=firefox-b-d&sca_esv=594603375&tbs=lrf:!1m4!1u3!2m2!3m1!1e1!1m4!1u5!2m2!5m1!1sgcid_3german_1restaurant!1m4!1u5!2m2!5m1!1sgcid_3indian_1restaurant!1m4!1u2!2m2!2m1!1e1!1m4!1u1!2m2!1m1!1e1!1m4!1u1!2m2!1m1!1e2!2m1!1e2!2m1!1e5!2m1!1e1!2m1!1e3!3sIAEqAkRF,lf:1,lf_ui:9&tbm=lcl&sxsrf=AM9HkKnqdXFj_FVNzgEjVYXigqgBUOtXnw:1703948168668&q=restaurants%20in%20germany&rflfq=1&num=10&sa=X&ved=2ahUKEwinmbzKtbeDAxWfS0EAHQLRDoEQjGp6BAgXEAE&biw=1525&bih=760&dpr=0.9&rlst=f#rlfi=hd:;si:;mv:[[52.809863099999994,14.150356],[47.8622162,6.5175032]];tbs:lrf:!1m4!1u3!2m2!3m1!1e1!1m4!1u5!2m2!5m1!1sgcid_3german_1restaurant!1m4!1u5!2m2!5m1!1sgcid_3indian_1restaurant!1m4!1u2!2m2!2m1!1e1!1m4!1u1!2m2!1m1!1e1!1m4!1u1!2m2!1m1!1e2!2m1!1e2!2m1!1e5!2m1!1e1!2m1!1e3!3sIAEqAkRF,lf:1,lf_ui:9"

gastronomy_data = []

def scrapePage(url):
    print("Fetching url...")
    driver.get(url)
    print("URL fetched")
    sleep(7)

    for i in range(5):
        sleep(1)
        restaurant_link = driver.find_elements(By.CSS_SELECTOR, "a.vwVdIc")
        sleep(5)
        restaurant_link = restaurant_link[i]
        try:
            # click and wait till the clicked restaurant main page loads
            restaurant_link.click()
            restaurant_main_page = WebDriverWait(driver, 20).until(
                EC.visibility_of_element_located((By.CSS_SELECTOR, "div.kp-header"))
            )

            # restaurant name
            try:
                name = driver.find_element(By.XPATH, "//h2/span[not(@*)]").text
            except NoSuchElementException as e:
                print(e)
            sleep(2)

            # restaurant address
            try:
                address = driver.find_element(By.CSS_SELECTOR, "span.LrzXr").text
            except NoSuchElementException as e:
                print(e)
            sleep(2)

            # restaurant nationality
            try:
                nationality = driver.find_element(By.CSS_SELECTOR, "div.zloOqf span.YhemCb:nth-child(2)").text
            except NoSuchElementException as e:
                print(e)

            # restaurant telephone number
            try:
                telephone_number = driver.find_element(By.XPATH, "//a/span[starts-with(text(), '+')]").text
            except NoSuchElementException as e:
                print(e)
            sleep(2)

            # restaurant website url
            try:
                website_url = driver.find_element(By.CSS_SELECTOR, "a.mI8Pwc").get_attribute("href")
            except NoSuchElementException as e:
                print(e)
            sleep(3)

            # restaurant instagram link
            try:
                insta_link = driver.find_element(By.CSS_SELECTOR, "g-link a").get_attribute("href")
            except NoSuchElementException as e:
                print(e)
            sleep(3)

            # restaurant facebook link
            try:
                facebook = driver.find_element(By.CSS_SELECTOR, "g-link a").get_attribute("href")
            except NoSuchElementException as e:
                print(e)
            sleep(2)

            # restaurant service options
            try:
                service_options = driver.find_element(By.XPATH, "//div[@style='margin:8px 16px']").text
            except NoSuchElementException as e:
                print(e)

            data = {
                "S/N": f"{i+1}",
                "Name": name,
                "Address": address,
                "Nationality": nationality,
                "Telephone_Number": telephone_number,
                "Website_url": website_url,
                "Instagram_link": insta_link,
                "Facebook": facebook,
                "Service_options": service_options
            }
            gastronomy_data.append(data)
            print(data)

            # go back to url main page
            driver.back()
            sleep(10)
        except StaleElementReferenceException as e:
            print(f"Exception Error: {e}")

    driver.quit()
    return gastronomy_data



app = FastAPI(title="G-Maps Gastronomy Data")

@app.get("/")
async def home():
    return {"message": "Scrape data from your g-map url page then download data file"}

@app.get("/data-via-page-url")
async def scrape_page(url: str):
    data = scrapePage(url)
    return data

@app.get("/download")
async def download_file():
    header = ["S/N", "Name", "Address", "Nationality", "Telephone_Number", "Website_url", "Instagram_link", "Facebook", "Service_options"]
    with open("gastronomy_data.csv", "w", newline="") as gd:
        writer = csv.DictWriter(gd, fieldnames=header)
        writer.writeheader()

        for data in gastronomy_data:
            writer.writerow(data)

    file_path = "./gastronomy_data.csv"

    try:
        response = FileResponse(path=file_path, media_type="texc/csv", filename="gastronomy data.csv")
        return response
    except Exception as e:
        return {"error": "Data not scraped yet"}
