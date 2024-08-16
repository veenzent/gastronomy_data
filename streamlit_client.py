import streamlit as st
import pandas as pd
from scraper import Extractor
from selenium.common.exceptions import WebDriverException


st.markdown('<h1 style="color: lightblue; text-align: center;">GASTRONOMY DATA</h1>', unsafe_allow_html=True)

st.markdown("""
    <h2>Steps to scrape gastronomy data from Google maps</h2>
        <ol>
            <li>Query your browser manually for city you want gastronomy data on e.g restaurants in Germany</li>
            <li>Click on 'more places' to load list of restaurants in google maps</li>
            <li>Copy and paste url of page from step 2 in the field below.</li>
            <li>
                Sampled_url = 
                <a href="https://www.google.com/search?client=firefox-b-d&sca_esv=594603375&tbs=lrf:!1m4!1u3!2m2!3m1!1e1!1m4!1u5!2m2!5m1!1sgcid_3german_1restaurant!1m4!1u5!2m2!5m1!1sgcid_3indian_1restaurant!1m4!1u2!2m2!2m1!1e1!1m4!1u1!2m2!1m1!1e1!1m4!1u1!2m2!1m1!1e2!2m1!1e2!2m1!1e5!2m1!1e1!2m1!1e3!3sIAEqAkRF,lf:1,lf_ui:9&tbm=lcl&sxsrf=AM9HkKnqdXFj_FVNzgEjVYXigqgBUOtXnw:1703948168668&q=restaurants%20in%20germany&rflfq=1&num=10&sa=X&ved=2ahUKEwinmbzKtbeDAxWfS0EAHQLRDoEQjGp6BAgXEAE&biw=1525&bih=760&dpr=0.9&rlst=f#rlfi=hd:;si:;mv:[[52.809863099999994,14.150356],[47.8622162,6.5175032]];tbs:lrf:!1m4!1u3!2m2!3m1!1e1!1m4!1u5!2m2!5m1!1sgcid_3german_1restaurant!1m4!1u5!2m2!5m1!1sgcid_3indian_1restaurant!1m4!1u2!2m2!2m1!1e1!1m4!1u1!2m2!1m1!1e1!1m4!1u1!2m2!1m1!1e2!2m1!1e2!2m1!1e5!2m1!1e1!2m1!1e3!3sIAEqAkRF,lf:1,lf_ui:9" class="sample" target="_blank">Restaurants in Germany</a>
            </li>
            <li>Click on the Scrape to start scraping data</li>
            <li>The scraping would take some time before it completes. This is an explicit action to avoid Googles suspicion and captcha test.</li>
        </ol>
    """, unsafe_allow_html=True
)

# create an instance of Extractor
extrator = Extractor()

def scrapeData(url: str):
    # create a dataframe
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

    # load url
    try:
        extractor.load_url_page(url)
    except WebDriverException as e:
        st.toast('Please check your network connection for internet access')
        extractor.retry(extractor.load_url_page, args=(url))

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

        # update dataframe: append new row
        new_row = pd.Series(data)
        df.loc[len(df)] = new_row

        # display new row
        st.table(pd.DataFrame(data), index=[0])

        print(data, '\n')
        index += 1
        extractor.close_current_page()

        # limit scraping to 10 results(10 restaurants)
        if index == 11:
            # display dataframe
            st.dataframe(df)
            break

    extractor.quit_browser()


# create a form
form = st.form(key="my_form")
url = form.text_input("Enter URL")

def scrapeCaller(url):
    if url:
        scrapeData(url)
    else:
        st.write("Insert a url to scrape")

form.form_submit_button("Scrape", on_click=scrapeCaller, args=[url])

