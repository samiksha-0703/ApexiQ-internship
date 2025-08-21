from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
from datetime import datetime

# Function to format date
def format_date(date_str):
    try:
        date_str = date_str.split("[")[0].strip()  # remove [1] refs
        parsed_date = datetime.strptime(date_str, "%B %d, %Y")
        return parsed_date.strftime("%d-%m-%Y")
    except:
        return ""

# Setup Selenium
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
url = "https://en.wikipedia.org/wiki/Windows_10_version_history"
driver.get(url)

# Locate the first wikitable
tables = driver.find_elements(By.XPATH, "//table")
target_table = tables[1] 


# Get all rows in the target table
rows = target_table.find_elements(By.XPATH, ".//tr")

data = []
last_version = ""
last_release_date = ""

for row in rows[1:]:
    cols = row.find_elements(By.XPATH, ".//td")
    if len(cols) >= 5:  
        # Version handling
        version = cols[0].text.strip()
        if version:
            last_version = version
        version = last_version + ".x"

        # Release Date handling — detect dynamically
        # If row has 6+ cols → Release Date at index 3
        # If row has only 5 cols → Release Date at index 2
        if len(cols) >= 6:
            release_date = cols[3].text.strip()
        else:
            release_date = cols[2].text.strip()

        if release_date:
            last_release_date = release_date
        release_date_fmt = format_date(last_release_date)

        # EOL Dates
        if len(cols) >= 6:
            home_pro_eol_fmt = format_date(cols[4].text.strip())
            ent_edu_eol_fmt = format_date(cols[5].text.strip())
        else:
            home_pro_eol_fmt = format_date(cols[3].text.strip())
            ent_edu_eol_fmt = format_date(cols[4].text.strip())

        # Support Duration
        try:
            start_dt = datetime.strptime(release_date_fmt, "%d-%m-%Y")
            end_dt = datetime.strptime(home_pro_eol_fmt, "%d-%m-%Y")
            support_duration = (end_dt - start_dt).days
        except:
            support_duration = ""

        data.append([
            version,
            release_date_fmt,
            home_pro_eol_fmt,
            ent_edu_eol_fmt,
            support_duration
        ])

driver.quit()

# Create DataFrame
df = pd.DataFrame(data, columns=[
    "Version",
    "Release Date",
    "Home/Pro EOL Date",
    "Enterprise/Education EOL Date",
    "Support Duration (days)"
])

# Save CSV
df.to_csv("windows10_eol.csv", index=False, encoding="utf-8")
print("✅ CSV saved: windows10_eol.csv")
