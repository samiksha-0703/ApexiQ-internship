from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
from datetime import datetime

def format_date(date_str):
    try:
        # Remove any parenthesis or text like "(24 Jun 2025)"
        date_str = date_str.split("(")[1].split(")")[0].strip()
        dt = datetime.strptime(date_str, "%d %b %Y")
        return dt.strftime("%d-%m-%Y")
    except:
        return ""

# 1. Launch Selenium
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
url = "https://endoflife.date/oneplus"
driver.get(url)

# 2. Locate the table
table = driver.find_element(By.TAG_NAME, "table")
rows = table.find_elements(By.TAG_NAME, "tr")

data = []
# 3. Loop through rows
for row in rows[1:]:  # skip header
    cols = row.find_elements(By.TAG_NAME, "td")
    if not cols:
        continue

    version = cols[0].text.strip()
    release_str = cols[1].text.strip()
    eol_str = cols[2].text.strip()

    release_date = format_date(release_str)
    eol_date = format_date(eol_str)

    data.append({
        "Version": version,
        "Release Date": release_date,
        "EOL Date": eol_date
    })

driver.quit()

# 4. Convert to DataFrame and save
df = pd.DataFrame(data)
df.to_csv("oneplus_eol.csv", index=False, encoding="utf-8")
print("✅ CSV generated: oneplus_eol.csv")
