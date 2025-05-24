import streamlit as st
from google_play_scraper import reviews, Sort, exceptions
import pandas as pd
from datetime import datetime, timedelta

def fetch_reviews(app_name):
    try:
        APP_ID = app_name

        result, _ = reviews(APP_ID, lang="en", country="us", sort=Sort.NEWEST, count=1000)

        df = pd.DataFrame(result)
        columns_to_drop = ['userImage', 'replyContent', 'repliedAt']

        for column in columns_to_drop:
            if column in df.columns:
                df.drop(columns=[column], inplace=True)
        
        # current_time = datetime.now().strftime("%Y-%m-%dT%H:%M")
        # filename = f"{APP_ID}_raw_reviews.csv_{current_time}"

        # df.to_csv(filename, index=False)

        print(f"✅ Extracted {len(df)} reviews")
        return df
    except exceptions.NotFoundError:
        st.error("❌ App not found. Please check the app name or ID.")
    except Exception as e:
        st.error(f"❌ An error occurred: {str(e)}")
        print(f"Error: {str(e)}")
        return pd.DataFrame()  # Return an empty DataFrame in case of error

def main():
    st.title("Mercury - the review scraper")

    app_name = st.text_input("Enter the app name")

    if st.button("Fetch Reviews"):
        with st.spinner('Fetching reviews...'):
            st.write(f"Fetching Reviews for {app_name}")
            app_name = app_name.strip().lower()
            reviews = fetch_reviews(app_name)
            if not reviews.empty:
                st.dataframe(reviews)
            else:
                st.write(f"Cannot find any reviews for {app_name}")

if __name__ == "__main__":
    main()
