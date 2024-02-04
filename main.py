from scraper import Extractor
from fastapi import FastAPI, HTTPException, Request, Response
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
import pandas as pd
from io import BytesIO


app = FastAPI(title="G-Maps Gastronomy Data")

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

extractor = Extractor()
# gastronomy_data: dict[str, dict[str, str]] = {
#         1: {'S/N': 1, 'Name': 'Manny', 'Address': 'Ibeju-Lekki', 'Nationality': 'Nil', 'Telephone Number': '', 'Website': '', 'Instagram Link': '', 'Facebook Link': '', 'Service Options': ''},
#         2: {'S/N': 2, 'Name': 'Escobar Buritos', 'Address': 'Badore', 'Nationality': 'Nil', 'Telephone Number': '', 'Website': '', 'Instagram Link': '', 'Facebook Link': '', 'Service Options': ''},
#         3: {'S/N': 3, 'Name': 'Small-Ville', 'Address': 'Ajah', 'Nationality': 'Nil', 'Telephone Number': '', 'Website': '', 'Instagram Link': '', 'Facebook Link': '', 'Service Options': ''}
#     }

df_data = {
        "S/N": [],
        "Name": [],
        "Address": [],
        "Nationality": [],
        "Telephone Number": [],
        "Website": [],
        "Instagram Link": [],
        "Facebook Link": [],
        "Service Options": []
    }
df = pd.DataFrame(df_data)

# urll = "https://www.google.com/search?client=firefox-b-d&sca_esv=594603375&tbs=lrf:!1m4!1u3!2m2!3m1!1e1!1m4!1u5!2m2!5m1!1sgcid_3german_1restaurant!1m4!1u5!2m2!5m1!1sgcid_3indian_1restaurant!1m4!1u2!2m2!2m1!1e1!1m4!1u1!2m2!1m1!1e1!1m4!1u1!2m2!1m1!1e2!2m1!1e2!2m1!1e5!2m1!1e1!2m1!1e3!3sIAEqAkRF,lf:1,lf_ui:9&tbm=lcl&sxsrf=AM9HkKnqdXFj_FVNzgEjVYXigqgBUOtXnw:1703948168668&q=restaurants%20in%20germany&rflfq=1&num=10&sa=X&ved=2ahUKEwinmbzKtbeDAxWfS0EAHQLRDoEQjGp6BAgXEAE&biw=1525&bih=760&dpr=0.9&rlst=f#rlfi=hd:;si:;mv:[[52.809863099999994,14.150356],[47.8622162,6.5175032]];tbs:lrf:!1m4!1u3!2m2!3m1!1e1!1m4!1u5!2m2!5m1!1sgcid_3german_1restaurant!1m4!1u5!2m2!5m1!1sgcid_3indian_1restaurant!1m4!1u2!2m2!2m1!1e1!1m4!1u1!2m2!1m1!1e1!1m4!1u1!2m2!1m1!1e2!2m1!1e2!2m1!1e5!2m1!1e1!2m1!1e3!3sIAEqAkRF,lf:1,lf_ui:9"
# mainz = "https://www.google.com/search?client=firefox-b-d&sca_esv=596374102&tbs=lf:1,lf_ui:9&tbm=lcl&sxsrf=ACQVn0-2G5sPef-vv6QYCfU0u1cJpeTLYw:1704641224806&q=mainz+finthen+restaurant&rflfq=1&num=10&sa=X&ved=2ahUKEwil77G1y8uDAxUvaUEAHT3CDdgQjGp6BAgSEAE&biw=1525&bih=760&dpr=0.9#rlfi=hd:;si:;mv:[[49.997862299999994,8.1819598],[49.9712104,8.1506037]];tbs:lrf:!1m4!1u3!2m2!3m1!1e1!1m4!1u5!2m2!5m1!1sgcid_3pizza_1restaurant!1m4!1u5!2m2!5m1!1sgcid_3german_1restaurant!1m4!1u2!2m2!2m1!1e1!2m1!1e2!2m1!1e5!2m1!1e3!3sIAEqAkRF,lf:1,lf_ui:9"

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/data-via-url", response_class=HTMLResponse)
async def scrape_page(request: Request, url: str):
    print(f'Provided URL: {url}')
    if not url:
        raise HTTPException(status_code=404, detail="Input a url to scrape data")

    extractor.load_url_page(url)

    index = 1
    while extractor.click_restaurant():
        data = {
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

        new_row = pd.Series(data)
        df.loc[len(df)] = new_row
        print(data, '\n')
        index += 1
        extractor.close_current_page()

    extractor.quit_browser()
    result = df.to_dict(orient="records")
    return templates.TemplateResponse("result.html", {"request": request, "gastronomy_data": result})


@app.get("/download")
async def download_data():
    try:
        buffer = BytesIO()
        writer = pd.ExcelWriter(buffer, engine='openpyxl')
        df.to_excel(writer, sheet_name='Sheet1', index=False)
        writer._save()

        response = Response(
            content=buffer.getvalue(),
            media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        )
        response.headers["Content-Disposition"] = "attachment; filename=gastronomy_data.xlsx"

        return response
    except Exception as e:
        return Response(content=str(e), status_code=400)