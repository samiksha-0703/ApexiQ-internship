from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import time

# Setup Selenium
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

# Open the page (Python EOL table)
url = "https://endoflife.date/python"
driver.get(url)

# Wait for page to load
time.sleep(3)

# Find the table
table = driver.find_element(By.TAG_NAME, "table")
rows = table.find_elements(By.TAG_NAME, "tr")

# Extract data
data = []
for row in rows:
    cols = row.find_elements(By.TAG_NAME, "td")
    cell_data = [col.text.strip() for col in cols]
    if cell_data:
        data.append(cell_data)

# Create DataFrame with correct column count
df = pd.DataFrame(data, columns=["Release", "Released", "Active support", "Security Support", "Latest"])
print(df)
df.to_csv("python_eol.csv", index=False, encoding="utf-8")

print("✅ Data saved to python_eol.csv")
driver.quit()
