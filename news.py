import csv
import os
import sys
import pandas as pd
from datetime import datetime
from seleniumbase import Driver

app_path = os.path.dirname(sys.executable)
now = datetime.now()
dmy = now.strftime("%d-%m-%Y")

site = 'https://www.thesun.co.uk/sport/football/'

# 1. Initialize Advanced Undetected Driver in Headless Mode
driver = Driver(uc=True, headless=True)

try:
    # 2. Get the site and wait for the anti-bot verification handshake
    driver.get(site)
    driver.sleep(7) 
    
    # Optional debug safety check
    driver.save_screenshot("headless_debug.png")

    # 3. Locate structural wrappers
    containers = driver.find_elements(by='xpath', value="//div[@class = 'story__copy-container']")

    titles = []
    subtitles = []
    links = []

    # 4. Extract text (title, subtitle, link)
    for c in containers:
        try:
            title = c.find_element(by='xpath', value="./a/p").get_attribute("textContent").strip()
            subtitle = c.find_element(by='xpath', value="./a/h3").get_attribute("textContent").strip()
            link = c.find_element(by='xpath', value="./a").get_attribute('href')

            titles.append(title)
            subtitles.append(subtitle)
            links.append(link)
        except Exception:
            # Continues processing if a single card structure is malformed
            continue

    # 5. build dataframe and fill it
    df = pd.DataFrame(columns=['titles', 'subtitles', 'links'])
    df['titles'] = titles
    df['subtitles'] = subtitles
    df['links'] = links

    file_name = f'news_headline_{dmy}.csv'
    export_path = os.path.join(app_path, file_name)

    df.to_csv(export_path, index=False)
    print(f"Success! Saved {len(df)} entries to {export_path}")

finally:
    # 6. Shut down driver
    driver.quit()
