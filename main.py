from google_play_scraper import reviews,Sort
import pandas as pd
from datetime import datetime, timedelta
one_year_ago = datetime.now() - timedelta(days=365)



APP_ID = 'com.chase.sig.android'

result,_ = reviews(APP_ID,lang="en",country="us",sort=Sort.NEWEST,count=4000)

filtered  = [r for r in result if r['at']>=one_year_ago]

data = []
for r in filtered:
    data.append({
        'Date': r['at'].strftime("%Y-%m-%d"),
        'Rating': r['score'],
        'Review': r['content']
    })

df = pd.DataFrame(data)
filename = f"{APP_ID}_raw_reviews.xlsx"

df.to_excel(filename, index=False)

print(f"✅ Extracted {len(df)} reviews and saved to {filename}")

