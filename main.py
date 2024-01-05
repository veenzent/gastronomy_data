from time import sleep
from fastapi import FastAPI, HTTPException
from fastapi.responses import StreamingResponse
from selenium import webdriver
from selenium.webdriver.common.by import By
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
driver = webdriver.Chrome(options=chrome_options)
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
        print(f"Found {len(restaurant_link)} restaurants")
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
            if not name:
                name = "Nil"
            sleep(2)

            # restaurant address
            try:
                address = driver.find_element(By.CSS_SELECTOR, "span.LrzXr").text
            except NoSuchElementException as e:
                print(e)
            if not address:
                address = "Nil"
            sleep(2)

            # restaurant nationality
            try:
                nationality = driver.find_element(By.CSS_SELECTOR, "div.zloOqf span.YhemCb:nth-child(2)").text
            except NoSuchElementException as e:
                print(e)
            if not nationality:
                nationality = "Nil"
            sleep(2)

            # restaurant telephone number
            try:
                telephone_number = driver.find_element(By.XPATH, "//a/span[starts-with(text(), '+')]").text
                # telephone_number = driver.find_element(By.CSS_SELECTOR, "a[data-dtype='d3ph'] span").text
            except NoSuchElementException as e:
                print(e)
            sleep(2)
            if not telephone_number:
                telephone_number = "Nil"

            # restaurant website url
            try:
                website_url = driver.find_element(By.CSS_SELECTOR, "a.mI8Pwc").get_attribute("href")
            except NoSuchElementException as e:
                print(e)
            if not website_url:
                website_url = "Nil"
            sleep(3)

            # restaurant instagram link
            try:
                insta_link = driver.find_element(By.CSS_SELECTOR, "g-link a").get_attribute("href")
            except NoSuchElementException as e:
                print(e)
            if not insta_link:
                insta_link = "Nil"
            sleep(3)

            # restaurant facebook link
            try:
                facebook = driver.find_element(By.CSS_SELECTOR, "g-link a").get_attribute("href")
            except NoSuchElementException as e:
                print(e)
            if not facebook:
                facebook = "Nil"
            sleep(2)

            # restaurant service options
            try:
                service_options = driver.find_element(By.XPATH, "//div[@style='margin:8px 16px']").text
            except NoSuchElementException as e:
                print(e)
            if not service_options:
                service_options = "Nil"

            data = {
                "S/N": str(f"{i+1}"),
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

def gastronomy_data_csv():
    header = ["S/N", "Name", "Address", "Nationality", "Telephone_Number", "Website_url", "Instagram_link", "Facebook", "Service_options"]
    yield ",".join(header) + "\n"

    for values in gastronomy_data:
        yield ",".join(values[key] for key in header) + "\n"


app = FastAPI(title="G-Maps Gastronomy Data")

@app.get("/")
async def home():
    """
    Click on "Try it out" button at the top right of every route, provide needed details and click on "Execute" to run the code
    """
    return {
        1: "Steps to scrape gastronomy data",
        2: "Query your browser manually for city you want gastronomy data on e.g restaurants in Germany",
        3: "Click on 'more places' to load list of restaurants in google maps",
        4: "Copy url of page frop step 2.",
        5: "Sampled_url = https://www.google.com/search?client=firefox-b-d&sca_esv=594603375&tbs=lrf:!1m4!1u3!2m2!3m1!1e1!1m4!1u5!2m2!5m1!1sgcid_3german_1restaurant!1m4!1u5!2m2!5m1!1sgcid_3indian_1restaurant!1m4!1u2!2m2!2m1!1e1!1m4!1u1!2m2!1m1!1e1!1m4!1u1!2m2!1m1!1e2!2m1!1e2!2m1!1e5!2m1!1e1!2m1!1e3!3sIAEqAkRF,lf:1,lf_ui:9&tbm=lcl&sxsrf=AM9HkKnqdXFj_FVNzgEjVYXigqgBUOtXnw:1703948168668&q=restaurants%20in%20germany&rflfq=1&num=10&sa=X&ved=2ahUKEwinmbzKtbeDAxWfS0EAHQLRDoEQjGp6BAgXEAE&biw=1525&bih=760&dpr=0.9&rlst=f#rlfi=hd:;si:;mv:[[52.809863099999994,14.150356],[47.8622162,6.5175032]];tbs:lrf:!1m4!1u3!2m2!3m1!1e1!1m4!1u5!2m2!5m1!1sgcid_3german_1restaurant!1m4!1u5!2m2!5m1!1sgcid_3indian_1restaurant!1m4!1u2!2m2!2m1!1e1!1m4!1u1!2m2!1m1!1e1!1m4!1u1!2m2!1m1!1e2!2m1!1e2!2m1!1e5!2m1!1e1!2m1!1e3!3sIAEqAkRF,lf:1,lf_ui:9",
        6: "Paste url in url-field of scrape-Page route",
        7: "Click on Execute to scrape data",
        8: "The scraping would take some time before it completes so as to avoid Googles suspicion and captcha test",
        9: "Append /docs to this page's url to continue"
    }

@app.get("/data-via-page-url")
async def scrape_page(url: str):
    if not url:
        raise HTTPException(status_code=404, detail="Input a url to scrape data")
    try:
        data = scrapePage(url)
    except Exception as e:
        print(e)
        return e
    return data

@app.get("/download")
async def download_data():
    filename = "gastronomy_data.csv"
    try:
        if not gastronomy_data:
            return {"error": "Data not scraped yet"}
        response = StreamingResponse(
            gastronomy_data_csv(),
            media_type="text/csv",
            headers={"Content-Disposition": f"attachment; filename={filename}"}
        )
        return response                     
    except Exception as e:
        print(e)
        return {"error": "Data not scraped yet"}
