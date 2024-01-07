from time import sleep
from fastapi import FastAPI, HTTPException
from fastapi.responses import StreamingResponse
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


# url = "https://www.google.com/search?client=firefox-b-d&sca_esv=594603375&tbs=lrf:!1m4!1u3!2m2!3m1!1e1!1m4!1u5!2m2!5m1!1sgcid_3german_1restaurant!1m4!1u5!2m2!5m1!1sgcid_3indian_1restaurant!1m4!1u2!2m2!2m1!1e1!1m4!1u1!2m2!1m1!1e1!1m4!1u1!2m2!1m1!1e2!2m1!1e2!2m1!1e5!2m1!1e1!2m1!1e3!3sIAEqAkRF,lf:1,lf_ui:9&tbm=lcl&sxsrf=AM9HkKnqdXFj_FVNzgEjVYXigqgBUOtXnw:1703948168668&q=restaurants%20in%20germany&rflfq=1&num=10&sa=X&ved=2ahUKEwinmbzKtbeDAxWfS0EAHQLRDoEQjGp6BAgXEAE&biw=1525&bih=760&dpr=0.9&rlst=f#rlfi=hd:;si:;mv:[[52.809863099999994,14.150356],[47.8622162,6.5175032]];tbs:lrf:!1m4!1u3!2m2!3m1!1e1!1m4!1u5!2m2!5m1!1sgcid_3german_1restaurant!1m4!1u5!2m2!5m1!1sgcid_3indian_1restaurant!1m4!1u2!2m2!2m1!1e1!1m4!1u1!2m2!1m1!1e1!1m4!1u1!2m2!1m1!1e2!2m1!1e2!2m1!1e5!2m1!1e1!2m1!1e3!3sIAEqAkRF,lf:1,lf_ui:9"

gastronomy_data = []

def scrapePage(url):
    print("Fetching url...")
    driver.get(url)
    print("URL fetched")
    sleep(5)

    for i in range(5):
        sleep(1)
        restaurant_link = driver.find_elements(By.CSS_SELECTOR, "a.vwVdIc")
        print(f"Scraping {i+1} of {len(restaurant_link)} restaurants")
        sleep(3)
        restaurant = restaurant_link[i]
        
        # click and wait till the clicked restaurant main page loads
        restaurant.click()
        WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, "div.kp-header"))
        )

        page = soup(driver.page_source, "html.parser")

        try:
            # restaurant name
            try:
                name =  page.select("h2.qrShPb span")[0].text
                print(f"Name: {name}")
                # name = driver.find_element(By.XPATH, "//h2/span[not(@*)]").text
            except Exception as e:
                print(e)
            if not name:
                name = "Nil"

            # restaurant address
            try:
                # address = driver.find_element(By.CSS_SELECTOR, "span.LrzXr").text
                address = page.select("span.LrzXr")[0].text
                print(f"Address: {address}")
            except Exception as e:
                print(e)
            if not address:
                address = "Nil"

            # restaurant nationality
            try:
                nationality = page.select("span.YhemCb")[1].text
                # nationality = driver.find_element(By.CSS_SELECTOR, "div.zloOqf span.YhemCb:nth-child(2)").text
                print(f"Nationality: {nationality}")
            except Exception as e:
                print(e)
            if not nationality:
                nationality = "Nil"

            # restaurant telephone number
            try:
                telephone_number = page.select("span.LrzXr a span")[0].text
                # telephone_number = driver.find_element(By.XPATH, "//a/span[starts-with(text(), '+')]").text
                print(f"Telephone Number: {telephone_number}")
            except Exception as e:
                print(e)
            if not telephone_number:
                telephone_number = "Nil"

            # restaurant website url
            try:
                website_url = driver.find_element(By.CSS_SELECTOR, "a.mI8Pwc").get_attribute("href")
                print(f"Website: {website_url}")
            except NoSuchElementException as e:
                print(e)
            if not website_url:
                website_url = "Nil"

            # restaurant instagram link
            try:
                insta_link = driver.find_element(By.XPATH, "//g-link/a[starts-with(@href, 'https://www.instagram.com/')]").get_attribute("href")
                # insta_link = driver.find_element(By.CSS_SELECTOR, "g-link a").get_attribute("href")
                # insta_link = page.select("g-link a")[0]["href"]
                print(f"Instagram Link: {insta_link}")
            except NoSuchElementException as e:
                print(e)
            if not insta_link:
                insta_link = "Nil"

            # restaurant facebook link
            try:
                facebook_link = driver.find_element(By.XPATH, "//g-link/a[starts-with(@href, 'https://www.facebook.com/')]").get_attribute("href")
                # facebook = driver.find_element(By.CSS_SELECTOR, "g-link a").get_attribute("href")
                # facebook_link = page.select("g-link a")[1]["href"]
                print(f"Facebool Link: {facebook_link}")
            except NoSuchElementException as e:
                print(e)
            if not facebook_link:
                facebook_link = "Nil"

            # restaurant service options
            try:
                service_options = driver.find_element(By.XPATH, "//div[@style='margin:8px 16px']").text
                # service_options = page.find("div", {"style": "margin:8px 16px", "data-ved": "2ahUKEwjY1ICtsMmDAxWY3gIHHQ0MD7IQ8_cGegQIIBAA", "data-hveid": "CCAQAA"}).get_text(strip=True)
                service_options = service_options.split(":")[1].strip()
                print(f"service options: {service_options}")
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
                "Facebook": facebook_link,
                "Service_options": service_options
            }
            gastronomy_data.append(data)
            print(data)

            # go back to url main page
            driver.back()
            sleep(5)
        except Exception as e:
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

    except WebDriverException:
        return {"Connection Error": "Please ensure your internet connection is secure and try again"}
    
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
