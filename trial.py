from selenium import webdriver
from selenium.webdriver.common.by import By
import csv
import time
from datetime import datetime

# Function to reformat date to dd-mm-yyyy
def format_date(date_str):
    try:
        return datetime.strptime(date_str.strip(), "%B %d, %Y").strftime("%d-%m-%Y")
    except:
        return date_str.strip()

driver = webdriver.Chrome()
driver.get("https://www.paloaltonetworks.com/services/support/end-of-life-announcements/end-of-life-summary")
time.sleep(5)

data = []

# Get all tables under divs
tables = driver.find_elements(By.XPATH, "//div//table")

for table in tables:
    software_name = None
    header_row_index = 0

    # 1️⃣ Try to get name from THEAD
    try:
        software_name = table.find_element(By.XPATH, ".//thead//*[self::b or self::th or self::td]").text.strip()
    except:
        pass

    # 2️⃣ If not in THEAD, search all tbody rows for <b>
    if not software_name:
        rows = table.find_elements(By.XPATH, ".//tr")
        for idx, row in enumerate(rows, start=1):
            try:
                b_tag = row.find_element(By.XPATH, ".//b")
                software_name = b_tag.text.strip()
                header_row_index = idx   # store the row index where name was found
                break
            except:
                continue

    if not software_name:
        continue  # skip if we still couldn't find a name

    # 3️⃣ Extract all rows after the software name row
    rows = table.find_elements(By.XPATH, f".//tr[position() > {header_row_index}]")

    for row in rows:
        cols = row.find_elements(By.XPATH, ".//td")
        if len(cols) >= 3:
            version = cols[0].text.strip()
            release_date = format_date(cols[1].text)
            eol_date = format_date(cols[2].text)

            data.append([software_name, version, eol_date, release_date])

# ✅ Save to CSV
with open("eol.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(["Software Name", "Version", "EOL Date", "Release Date"])
    writer.writerows(data)

driver.quit()
print("Data scraped and saved to eol_summary.csv with", len(data), "rows")
