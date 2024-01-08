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


# urll = "https://www.google.com/search?client=firefox-b-d&sca_esv=594603375&tbs=lrf:!1m4!1u3!2m2!3m1!1e1!1m4!1u5!2m2!5m1!1sgcid_3german_1restaurant!1m4!1u5!2m2!5m1!1sgcid_3indian_1restaurant!1m4!1u2!2m2!2m1!1e1!1m4!1u1!2m2!1m1!1e1!1m4!1u1!2m2!1m1!1e2!2m1!1e2!2m1!1e5!2m1!1e1!2m1!1e3!3sIAEqAkRF,lf:1,lf_ui:9&tbm=lcl&sxsrf=AM9HkKnqdXFj_FVNzgEjVYXigqgBUOtXnw:1703948168668&q=restaurants%20in%20germany&rflfq=1&num=10&sa=X&ved=2ahUKEwinmbzKtbeDAxWfS0EAHQLRDoEQjGp6BAgXEAE&biw=1525&bih=760&dpr=0.9&rlst=f#rlfi=hd:;si:;mv:[[52.809863099999994,14.150356],[47.8622162,6.5175032]];tbs:lrf:!1m4!1u3!2m2!3m1!1e1!1m4!1u5!2m2!5m1!1sgcid_3german_1restaurant!1m4!1u5!2m2!5m1!1sgcid_3indian_1restaurant!1m4!1u2!2m2!2m1!1e1!1m4!1u1!2m2!1m1!1e1!1m4!1u1!2m2!1m1!1e2!2m1!1e2!2m1!1e5!2m1!1e1!2m1!1e3!3sIAEqAkRF,lf:1,lf_ui:9"
# mainz = "https://www.google.com/search?client=firefox-b-d&sca_esv=596374102&tbs=lf:1,lf_ui:9&tbm=lcl&sxsrf=ACQVn0-2G5sPef-vv6QYCfU0u1cJpeTLYw:1704641224806&q=mainz+finthen+restaurant&rflfq=1&num=10&sa=X&ved=2ahUKEwil77G1y8uDAxUvaUEAHT3CDdgQjGp6BAgSEAE&biw=1525&bih=760&dpr=0.9#rlfi=hd:;si:;mv:[[49.997862299999994,8.1819598],[49.9712104,8.1506037]];tbs:lrf:!1m4!1u3!2m2!3m1!1e1!1m4!1u5!2m2!5m1!1sgcid_3pizza_1restaurant!1m4!1u5!2m2!5m1!1sgcid_3german_1restaurant!1m4!1u2!2m2!2m1!1e1!2m1!1e2!2m1!1e5!2m1!1e3!3sIAEqAkRF,lf:1,lf_ui:9"

gastronomy_data = []

def scrapePage(url):
    wait = WebDriverWait(driver, 10)
    print("Fetching url...")
    driver.get(url)
    print("URL fetched")
    sleep(5)

    for i in range(5):
        sleep(2)
        # retry mechanism for error sake
        for attempt in range(3):
            try:
                restaurants_links = wait.until(EC.visibility_of_all_elements_located(locator=(By.CSS_SELECTOR, "a.vwVdIc")))
                # driver.find_elements(By.CSS_SELECTOR, "a.vwVdIc")
                sleep(10)
                print(f"Scraping {i+1} of {len(restaurants_links)} restaurants")
                restaurant = restaurants_links[i]
                break
            except Exception as e:
                print(f"Attempt {attempt+1} to get restaurants failed: {e}")
                if attempt < 2:
                    sleep(3)

        # click and wait till the clicked restaurant main page loads
        restaurant.click()
        wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "div.kp-header")))

        page = soup(driver.page_source, "html.parser")

        try:
            # restaurant name
            try:
                name =  page.select("h2.qrShPb span")[0].text
                print(f"Name: {name}")
            except IndexError:
                name = driver.find_element(By.XPATH, "//h2/span[not(@*)]").text
                print(f"Name: {name}")
            except NoSuchElementException as e:
                print(e)
                name = "Nil"

            # restaurant address
            try:
                address = page.select("span.LrzXr")[0].text
                print(f"Address: {address}")
            except IndexError:
                address = driver.find_element(By.CSS_SELECTOR, "span.LrzXr").text
                print(f"Address: {address}")
            except NoSuchElementException as e:
                print("Element not found")
                address = "Nil"

            # restaurant nationality
            for attempt in range(3):
                try:
                    nationality = page.select("span.YhemCb")[1].text
                    print(f"Nationality: {nationality}")
                    break
                except IndexError:
                    nationality = driver.find_element(By.CSS_SELECTOR, "div.zloOqf span.YhemCb:nth-child(2)").text
                    print(f"Nationality: {nationality}")
                    break
                except NoSuchElementException:
                    print("No such element")
                    nationality = "Nil"
                except Exception as e:
                    print(f"Attempt {attempt+1} failed: {e}")
                    if attempt < 2:
                        sleep(3)

            # restaurant telephone number
            for attempt in range(3):
                try:
                    telephone_number = page.select("span.LrzXr a span")[0].text
                    print(f"Telephone Number: {telephone_number}")
                    break
                except IndexError:
                    telephone_number = driver.find_element(By.XPATH, "//a/span[starts-with(text(), '+')]").text
                    print(f"Telephone Number: {telephone_number}")
                    break
                except NoSuchElementException:
                    print("Error: No nosuch element")
                    telephone_number = "Nil"
                    print(telephone_number)
                except Exception as e:
                    print(f"Attempt {attempt+1} failed: {e}")
                    if attempt < 2:
                        sleep(3)

            # restaurant website url
            for attempt in range(3):
                try:
                    website_url = driver.find_element(By.CSS_SELECTOR, "a.mI8Pwc").get_attribute("href")
                    print(f"Website: {website_url}")
                    break
                except NoSuchElementException:
                    print("Error: No such element")
                    website_url = "Nil"
                except Exception as e:
                    print(f"Attempt {attempt+1} failed: {e}")
                    if attempt < 2:
                        sleep(3)

            # restaurant instagram link
            for attempt in range(3):
                try:
                    insta_link_element = driver.find_element(By.XPATH, "//g-link/a[starts-with(@href, 'https://www.instagram.com/')]")
                    insta_link = insta_link_element.get_attribute("href")
                    print(f"Instagram Link: {insta_link}")
                    break
                except NoSuchElementException:
                    insta_link = page.select_one("g-link a[href^='https://www.instagram.com/']")["href"]
                    print(f"Instagram Link: {insta_link}")
                    break
                except Exception as e:
                    print(f"Attempt {attempt+1} to get IG link failed: {e}")
                    insta_link = "Nil"
                    if attempt < 2:
                        sleep(3)

            # restaurant facebook link
            for attempt in range(3):
                try:
                    facebook_link_element = driver.find_element(By.XPATH, "//g-link/a[starts-with(@href, 'https://www.facebook.com/')]")
                    facebook_link = facebook_link_element.get_attribute("href")
                    print(f"Facebook Link: {facebook_link}")
                    break
                except NoSuchElementException:
                    facebook_link = page.select("g-link a[href^='https://www.facebook.com/']")["href"]
                    print(f"Facebook Link: {facebook_link}")
                    break
                except Exception as e:
                    print(f"Attempt {attempt+1} to get FB link failed: {e}")
                    facebook_link = "Nil"
                    if attempt < 2:
                        sleep(3)

            # restaurant service options
            try:
                service_options = driver.find_element(By.XPATH, "//div[@style='margin:8px 16px']").text
                service_options = service_options.split(":")[1].strip()
                print(f"service options: {service_options}")
            except NoSuchElementException:
                service_options = page.find("div", {"style": "margin:8px 16px", "data-ved": "2ahUKEwjY1ICtsMmDAxWY3gIHHQ0MD7IQ8_cGegQIIBAA", "data-hveid": "CCAQAA"}).get_text(strip=True)
                print(f"service options: {service_options}")
            except IndexError as e:
                service_options = "Nil"
                print(e)

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

# scrapePage(mainz)

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
