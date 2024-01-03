from time import sleep
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import StaleElementReferenceException, TimeoutException
# from bs4 import BeautifulSoup

'''
name
address
telephone number
website url
insta link
facebook
nationality
service options
'''

# url = "https://www.google.com/search?client=firefox-b-d&sca_esv=594603375&tbs=lrf:!1m4!1u3!2m2!3m1!1e1!1m4!1u5!2m2!5m1!1sgcid_3german_1restaurant!1m4!1u5!2m2!5m1!1sgcid_3indian_1restaurant!1m4!1u2!2m2!2m1!1e1!1m4!1u1!2m2!1m1!1e1!1m4!1u1!2m2!1m1!1e2!2m1!1e2!2m1!1e5!2m1!1e1!2m1!1e3!3sIAEqAkRF,lf:1,lf_ui:9&tbm=lcl&sxsrf=AM9HkKnqdXFj_FVNzgEjVYXigqgBUOtXnw:1703948168668&q=restaurants%20in%20germany&rflfq=1&num=10&sa=X&ved=2ahUKEwinmbzKtbeDAxWfS0EAHQLRDoEQjGp6BAgXEAE&biw=1525&bih=760&dpr=0.9&rlst=f#rlfi=hd:;si:;mv:[[52.809863099999994,14.150356],[47.8622162,6.5175032]];tbs:lrf:!1m4!1u3!2m2!3m1!1e1!1m4!1u5!2m2!5m1!1sgcid_3german_1restaurant!1m4!1u5!2m2!5m1!1sgcid_3indian_1restaurant!1m4!1u2!2m2!2m1!1e1!1m4!1u1!2m2!1m1!1e1!1m4!1u1!2m2!1m1!1e2!2m1!1e2!2m1!1e5!2m1!1e1!2m1!1e3!3sIAEqAkRF,lf:1,lf_ui:9"
url = "https://www.google.com/search?q=restaurants+in+ikeja&client=firefox-b-d&sca_esv=595105071&tbm=lcl&sxsrf=AM9HkKmegn85nzAuG2L8Ytf0nBZzhW95Jg%3A1704275331432&ei=gy2VZZ2AGrqvhbIP7pm52A8&oq=restaurants+in+&gs_lp=Eg1nd3Mtd2l6LWxvY2FsIg9yZXN0YXVyYW50cyBpbiAqAggDMgQQIxgnMgQQIxgnMgoQABiABBiKBRhDMgsQABiABBixAxiDATIFEAAYgAQyBRAAGIAEMgUQABiABDIFEAAYgAQyBRAAGIAEMgUQABiABEjYRlDSEljlF3AAeACQAQOYAdAFoAGiFKoBCzItMS4wLjIuMS4xuAEDyAEA-AEBiAYB&sclient=gws-wiz-local"

chrome_options = Options()
# chrome_options.add_argument("--headless=new")
# chrome_options.add_argument("--disable-blink-features=AutomationControlled")
# chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
# chrome_options.add_experimental_option("useAutomationExtension", False)

driver = webdriver.Chrome(options=chrome_options)
# driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
driver.get(url)
sleep(40)

gastronomy_data = []

for i in range(20):
    sleep(1)
    restaurant_link = driver.find_elements(By.CSS_SELECTOR, "a.vwVdIc")
    sleep(3)
    restaurant_link = restaurant_link[i]
    try:
        # click and wait till the clicked restaurant main page loads
        restaurant_link.click()
        restaurant_main_page = WebDriverWait(driver, 30).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, "div.kp-header"))
        )

        name = driver.find_element(By.XPATH, "//h2/span[not(@*)]").text
        address = driver.find_element(By.CSS_SELECTOR, "span.LrzXr").text
        # nationality = driver.find_element(By.XPATH, "//span[@class='YhemCb']").text
        telephone_number = driver.find_element(By.XPATH, "//a/span[starts-with(text(), '+')]").text
        website_url = driver.find_element(By.CSS_SELECTOR, "a.mI8Pwc").get_attribute("href")
        insta_link = driver.find_element(By.XPATH, "//g-link/a[starts-with(text(), 'https://www.instagram')]/@href").get_attribute("href")
        facebook = driver.find_element(By.XPATH, "//g-link/a[starts-with(text(), 'https://www.facebook')]").get_attribute("href")
        service_options = driver.find_element(By.XPATH, "//div[@style='margin:8px 16px']").text

        info = {
            f"{i+1}": {
                "Name": name,
                "Address": address,
                # "Nationality": nationality,
                "Telephone_Number": telephone_number,
                "Website_url": website_url,
                "Insta_link": insta_link,
                "Facebook": facebook,
                "Service_options": service_options
            }
        }
        # gastronomy_data.append(info)
        print(info)

        # go back to url main page
        driver.back()
        sleep(10)

    except StaleElementReferenceException as e:
        print(f"Exception Error: {e}")


driver.quit()
# print(gastronomy_data)
