from scraper import Extractor
from fastapi import FastAPI, HTTPException
from fastapi.responses import StreamingResponse


app = FastAPI(title="G-Maps Gastronomy Data")
extractor = Extractor()
# gastronomy_data: dict[str, dict[str, str]] = {}
gastronomy_data = {
        "1": {
            "S/N": 1,
            "Name": "Steins Traube",
            "Address": "Poststraße 4, 55126 Mainz, Germany",
            "Nationality": "Nil",
            "Telephone Number": "+49 6131 40249",
            "Website": "https://steins-traube.de/",
            "Instagram Link": "https://www.instagram.com/steinstraube/",
            "Facebook Link": "Nil",
            "Service Options": "Reservations required · Has outdoor seating"
        },
        "2": {
            "S/N": 2,
            "Name": "Gasthaus Hotel Adler",
            "Address": "Flugplatzstraße 1, 55126 Mainz, Germany",
            "Nationality": "Nil",
            "Telephone Number": "+49 6131 40447",
            "Website": "http://www.hotel-adler-finthen.de/",
            "Instagram Link": "Nil",
            "Facebook Link": "Nil",
            "Service Options": "Has outdoor seating · Has Wi-Fi · High chairs available"
        },
        "3": {
            "S/N": 3,
            "Name": "Finthener Döner & kebap Haus Mainz",
            "Address": "Kurmainzstraße 21, 55126 Mainz, Germany",
            "Nationality": "Nil",
            "Telephone Number": "+49 6131 6224774",
            "Website": "Nil",
            "Instagram Link": "Nil",
            "Facebook Link": "Nil",
            "Service Options": "lieferando.de\n Providers"
        },
        "4": {
            "S/N": 4,
            "Name": "Tower One",
            "Address": "Am Flugpl. 36, 55126 Mainz, Germany",
            "Nationality": "Nil",
            "Telephone Number": "+49 6131 5545030",
            "Website": "http://www.tower-one.de/",
            "Instagram Link": "https://www.instagram.com/tower.one/",
            "Facebook Link": "Nil",
            "Service Options": "Has outdoor seating · Has private dining room · Serves vegetarian dishes"
        },
        "5": {
            "S/N": 5,
            "Name": "Zum Turnerheim",
            "Address": "Poststraße 41, 55126 Mainz, Germany",
            "Nationality": "Nil",
            "Telephone Number": "+49 6131 40383",
            "Website": "https://de-de.facebook.com/pages/Gasthaus-zum-Turnerheim/183596208321531",
            "Instagram Link": "Nil",
            "Facebook Link": "Nil",
            "Service Options": "Reservations required · Has outdoor seating · Has kids' menu"
        },
        "6": {
            "S/N": 6,
            "Name": "Stern Döner Finthen",
            "Address": "Poststraße 53a, 55126 Mainz, Germany",
            "Nationality": "Nil",
            "Telephone Number": "+49 6131 6693691",
            "Website": "Nil",
            "Instagram Link": "Nil",
            "Facebook Link": "Nil",
            "Service Options": "Nil"
        },
        "7": {
            "S/N": 7,
            "Name": "Il Mondo GmbH",
            "Address": "Kurmainzstraße 24, 55126 Mainz, Germany",
            "Nationality": "Nil",
            "Telephone Number": "+49 6131 604352",
            "Website": "http://www.ilmondo-mainz.de/",
            "Instagram Link": "Nil",
            "Facebook Link": "Nil",
            "Service Options": "Reservations required · Has outdoor seating · Has private dining room"
        },
        "8": {
            "S/N": 8,
            "Name": "Fontana Stuben",
            "Address": "Waldthausenstraße 87, 55126 Mainz, Germany",
            "Nationality": "Nil",
            "Telephone Number": "+49 6131 472349",
            "Website": "https://la-fontana-mainz.eatbu.com/?lang=de",
            "Instagram Link": "Nil",
            "Facebook Link": "Nil",
            "Service Options": "Serves happy-hour food · Serves vegetarian dishes · Has Wi-Fi"
        },
        "9": {
            "S/N": 9,
            "Name": "Fontana Stuben",
            "Address": "Waldthausenstraße 87, 55126 Mainz, Germany",
            "Nationality": "Nil",
            "Telephone Number": "+49 6131 472349",
            "Website": "https://la-fontana-mainz.eatbu.com/?lang=de",
            "Instagram Link": "Nil",
            "Facebook Link": "Nil",
            "Service Options": "Serves happy-hour food · Serves vegetarian dishes · Has Wi-Fi"
        },
        "10": {
            "S/N": 10,
            "Name": "مغازه",
            "Address": "Kurmainzstraße 48, 55126 Mainz, Germany",
            "Nationality": "Nil",
            "Telephone Number": "Nil",
            "Website": "Nil",
            "Instagram Link": "Nil",
            "Facebook Link": "Nil",
            "Service Options": "Nil"
        },
        "11": {
            "S/N": 11,
            "Name": "Saifi Kabul Sheer Yakh Restaurant",
            "Address": "Kurmainzstraße 17, 55126 Mainz, Germany",
            "Nationality": "Nil",
            "Telephone Number": "+49 176 43487131",
            "Website": "Nil",
            "Instagram Link": "https://www.instagram.com/saifi_kabul_sheer_yakh/",
            "Facebook Link": "Nil",
            "Service Options": "Has outdoor seating · Serves vegetarian dishes · High chairs available"
        },
        "12": {
            "S/N": 12,
            "Name": "Adagio Restaurant",
            "Address": "Flugplatzstraße 44, 55126 Mainz, Germany",
            "Nationality": "Nil",
            "Telephone Number": "+49 6131 4910",
            "Website": "http://www.atrium-mainz.de/adagio/",
            "Instagram Link": "https://www.instagram.com/atriummainz/",
            "Facebook Link": "https://www.facebook.com/AtriumHotelMainz",
            "Service Options": "Serves vegetarian dishes · Has Wi-Fi · High chairs available"
        },
        "13": {
            "S/N": 13,
            "Name": "Adagio Restaurant",
            "Address": "Flugplatzstraße 44, 55126 Mainz, Germany",
            "Nationality": "Nil",
            "Telephone Number": "+49 6131 4910",
            "Website": "http://www.atrium-mainz.de/adagio/",
            "Instagram Link": "https://www.instagram.com/atriummainz/",
            "Facebook Link": "https://www.facebook.com/AtriumHotelMainz",
            "Service Options": "Serves vegetarian dishes · Has Wi-Fi · High chairs available"
        },
        "14": {
            "S/N": 14,
            "Name": "wahid Memar",
            "Address": "Kurmainzstraße 48, 55126 Mainz, Germany",
            "Nationality": "Nil",
            "Telephone Number": "+49 6131 6988077",
            "Website": "Nil",
            "Instagram Link": "Nil",
            "Facebook Link": "Nil",
            "Service Options": "Nil"
        },
        "15": {
            "S/N": 15,
            "Name": "Pizzeria Etna da Davide Mainz",
            "Address": "Uhlerbornstraße 10, 55126 Mainz, Germany",
            "Nationality": "Nil",
            "Telephone Number": "+49 6131 477389",
            "Website": "https://pizzeria-etna-mainz.com/10803?utm_source=google&utm_medium=mybusiness&utm_campaign=gb",
            "Instagram Link": "Nil",
            "Facebook Link": "Nil",
            "Service Options": "Doesn't accept reservations"
        },
        "16": {
            "S/N": 16,
            "Name": "Pizzeria Etna da Davide Mainz",
            "Address": "Uhlerbornstraße 10, 55126 Mainz, Germany",
            "Nationality": "Nil",
            "Telephone Number": "+49 6131 477389",
            "Website": "https://pizzeria-etna-mainz.com/10803?utm_source=google&utm_medium=mybusiness&utm_campaign=gb",
            "Instagram Link": "Nil",
            "Facebook Link": "Nil",
            "Service Options": "Doesn't accept reservations"
        },
        "17": {
            "S/N": 17,
            "Name": "Pizzeria Da Alessandro",
            "Address": "Sertoriusring 51, 55126 Mainz, Germany",
            "Nationality": "Nil",
            "Telephone Number": "+49 6131 6233244",
            "Website": "http://www.pizzeriadaalessandro.de/",
            "Instagram Link": "Nil",
            "Facebook Link": "Nil",
            "Service Options": "pizzeriadaalessandro.de"
        },
        "18": {
            "S/N": 18,
            "Name": "Pizzeria Bacio da Vito Mainz",
            "Address": "Sertoriusring 51, 55126 Mainz, Germany",
            "Nationality": "Nil",
            "Telephone Number": "+49 6131 9302021",
            "Website": "https://www.lieferando.de/speisekarte/pizzeria-bacio-da-vito",
            "Instagram Link": "Nil",
            "Facebook Link": "https://www.facebook.com/pizzeriabaciodavito/",
            "Service Options": "Has outdoor seating · Serves vegetarian dishes · Has Wi-Fi"
        },
        "19": {
            "S/N": 19,
            "Name": "Persisches Restaurant Kababsara",
            "Address": "Kurmainzstraße 48, 55126 Mainz, Germany",
            "Nationality": "Nil",
            "Telephone Number": "+49 6131 6988077",
            "Website": "https://persischesrestaurant-mainz.de/",
            "Instagram Link": "Nil",
            "Facebook Link": "Nil",
            "Service Options": "Has outdoor seating · Serves vegetarian dishes · High chairs available"
        },
        "20": {
            "S/N": 20,
            "Name": "Parkwiese Heidenfahrt",
            "Address": "Heidenfahrt 2, 55262 Ingelheim am Rhein, Germany",
            "Nationality": "Nil",
            "Telephone Number": "Nil",
            "Website": "Nil",
            "Instagram Link": "Nil",
            "Facebook Link": "Nil",
            "Service Options": "Nil"
        }
        }
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

        gastronomy_data.update({index: data})
        print(data, '\n')
        index += 1
        extractor.close_current_page()
    extractor.quit_browser()
    return gastronomy_data

def gastronomy_data_csv():
    header = ["S/N", "Name", "Address", "Nationality", "Telephone Number", "Website", "Instagram Link", "Facebook Link", "Service Options"]
    yield ",".join(header) + "\n"

    # {1: {data}, 2: {data}, 3: {data}, 4: {data}, 5: {data}, 6: {data}, 7: {data}, 8: {data}, 9: {data}}
    for values in gastronomy_data.values():
        yield ",".join(str(values[key]) for key in header) + "\n"

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
