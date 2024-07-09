import pandas as pd
from pprint import pprint
from main_functions import get_info
import time

# Read URLs from .txt file
urls = []
with open("links\chiang-mai_estate_links.txt", "r", encoding="utf-8") as f:
    for line in f:
        urls.append(line.strip())

# List to store scraped data
data_list = []

#CSV file name
csv_filename = "chiang-mai.csv"


def crawl_link(urls):
    

    data_list = []
    # Iterate through URLs and scrape data

    start_time = time.time()
    for i, url in enumerate(urls[:8], start=1):
        print("_"*80)
        print(f"{i} __ Start scraping for {url}")
        # Scrape main info and image sources
        try:
            
            
            # Combine scraped_data and image_sources into a single dictionary
            combined_data = get_info(url)
            pprint(combined_data)
            print("="*80)
            print(f"{i} ___ Done! Scraped data from {url}")
            data_list.append(combined_data)
        except Exception as e:
            print(f"Error scraping {url}: {e}")

    end_time = time.time()  # End time
    total_time = end_time - start_time  # Total duration
    hours, remainder = divmod(total_time, 3600)
    minutes, seconds = divmod(remainder, 60)
    total_time_formatted = f"{int(hours):02}:{int(minutes):02}:{int(seconds):02}"
    df = pd.DataFrame(data_list)
    if 'Phone' in df.columns:
        df = df.drop('Phone', axis=1)
    print(f"Total time taken: {total_time_formatted} ")
    return df

# Optionally, save all scraped data to a single CSV file

df = crawl_link(urls)
print(df)
df.to_csv(csv_filename, index=False)
print(f"All data saved to {csv_filename}")
