from .scraper import gastronomy_data_csv
from .scraper import Extractor as extractor
from fastapi import FastAPI, HTTPException
from fastapi.responses import StreamingResponse


app = FastAPI(title="G-Maps Gastronomy Data")
gastronomy_data = []

# urll = "https://www.google.com/search?client=firefox-b-d&sca_esv=594603375&tbs=lrf:!1m4!1u3!2m2!3m1!1e1!1m4!1u5!2m2!5m1!1sgcid_3german_1restaurant!1m4!1u5!2m2!5m1!1sgcid_3indian_1restaurant!1m4!1u2!2m2!2m1!1e1!1m4!1u1!2m2!1m1!1e1!1m4!1u1!2m2!1m1!1e2!2m1!1e2!2m1!1e5!2m1!1e1!2m1!1e3!3sIAEqAkRF,lf:1,lf_ui:9&tbm=lcl&sxsrf=AM9HkKnqdXFj_FVNzgEjVYXigqgBUOtXnw:1703948168668&q=restaurants%20in%20germany&rflfq=1&num=10&sa=X&ved=2ahUKEwinmbzKtbeDAxWfS0EAHQLRDoEQjGp6BAgXEAE&biw=1525&bih=760&dpr=0.9&rlst=f#rlfi=hd:;si:;mv:[[52.809863099999994,14.150356],[47.8622162,6.5175032]];tbs:lrf:!1m4!1u3!2m2!3m1!1e1!1m4!1u5!2m2!5m1!1sgcid_3german_1restaurant!1m4!1u5!2m2!5m1!1sgcid_3indian_1restaurant!1m4!1u2!2m2!2m1!1e1!1m4!1u1!2m2!1m1!1e1!1m4!1u1!2m2!1m1!1e2!2m1!1e2!2m1!1e5!2m1!1e1!2m1!1e3!3sIAEqAkRF,lf:1,lf_ui:9"
# mainz = "https://www.google.com/search?client=firefox-b-d&sca_esv=596374102&tbs=lf:1,lf_ui:9&tbm=lcl&sxsrf=ACQVn0-2G5sPef-vv6QYCfU0u1cJpeTLYw:1704641224806&q=mainz+finthen+restaurant&rflfq=1&num=10&sa=X&ved=2ahUKEwil77G1y8uDAxUvaUEAHT3CDdgQjGp6BAgSEAE&biw=1525&bih=760&dpr=0.9#rlfi=hd:;si:;mv:[[49.997862299999994,8.1819598],[49.9712104,8.1506037]];tbs:lrf:!1m4!1u3!2m2!3m1!1e1!1m4!1u5!2m2!5m1!1sgcid_3pizza_1restaurant!1m4!1u5!2m2!5m1!1sgcid_3german_1restaurant!1m4!1u2!2m2!2m1!1e1!2m1!1e2!2m1!1e5!2m1!1e3!3sIAEqAkRF,lf:1,lf_ui:9"

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

@app.get("/data-via-url")
async def scrape_page(url: str):
    if not url:
        raise HTTPException(status_code=404, detail="Input a url to scrape data")

    extractor.load_url_page(url)

    index = 1
    while extractor.click_restaurant():
        data = {
            # "S/N": extractor.restaurant_index,
            "S/N": index,
            "Name": extractor.extract_restaurant_name(),
            "Address": extractor.extract_restaurant_address(),
            "Nationality": extractor.extract_restaurant_nationality(),
            "Telephone Number": extractor.extract_restaurant_telephone_number(),
            "Website": extractor.extract_restaurant_website(),
            "Instagram Link": extractor.extract_restaurant_instagram_link(),
            "Facebook Link": extractor.extract_restaurant_facebook_link(),
            "Service Options": extractor.extract_restaurant_service_options()
        }

        gastronomy_data.append({index: data})
        print(data)
        index += 1
        extractor.close_curr_page

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
