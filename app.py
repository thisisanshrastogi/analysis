import streamlit as st
from google_play_scraper import reviews,reviews_all, Sort, exceptions
import pandas as pd
from datetime import datetime, timedelta

def fetch_reviews(app_name):
    try:
        APP_ID = app_name
        timethreshold=datetime.now() - timedelta(days=180)

        result, _ = reviews(APP_ID, lang="en", country="us", sort=Sort.NEWEST, count=5000)
        filtered  = [r for r in result if r['at']>=timethreshold]

        df = pd.DataFrame(filtered)
        columns_to_drop = ['userImage', 'replyContent', 'repliedAt']

        for column in columns_to_drop:
            if column in df.columns:
                df.drop(columns=[column], inplace=True)
        


        print(f"✅ Extracted {len(df)} reviews")
        

        # print(f"Total reviews fetched: {len(dfbig)}")
        return df
    except exceptions.NotFoundError:
        st.error("❌ App not found. Please check the app name or ID.")
    except Exception as e:
        st.error(f"❌ An error occurred: {str(e)}")
        print(f"Error: {str(e)}")
        return pd.DataFrame() 

def main():
    st.title("Mercury - the review scraper")

    app_name = st.text_input("Enter the app name")


    if st.button("Fetch Reviews"):
        with st.spinner('Fetching reviews...'):
            st.write(f"Fetching Reviews for {app_name}")
            app_name = app_name.strip().lower()
            reviews = fetch_reviews(app_name)
            if not reviews.empty:
                data=[]
                for index, row in reviews.iterrows():
                    data.append({
                        'App Name': app_name,
                        'Review': row['content'],
                        'Rating': row['score'],
                        'Date': row['at'],
                        'User': row['userName']
                    })
                st.success(f"✅ Successfully fetched {len(reviews)} reviews for {app_name} with last review on {reviews['at'].min().strftime('%d-%m-%Y')}")
                st.dataframe(reviews)
            else:
                st.write(f"Cannot find any reviews for {app_name}")

if __name__ == "__main__":
    main()
