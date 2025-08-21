from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd

# Setup Selenium
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
url = "https://en.wikipedia.org/wiki/Windows_10_version_history"
driver.get(url)

# Locate the second table (Windows 10 version history)
tables = driver.find_elements(By.XPATH, "//table")
target_table = tables[1]

# Get all rows in the table
rows = target_table.find_elements(By.XPATH, ".//tr")

# Extract header row
header_cells = rows[0].find_elements(By.XPATH, ".//th")
header = [th.text.strip() for th in header_cells]

# Extract data rows
table_data = []
for row in rows[1:]:
    cells = row.find_elements(By.XPATH, ".//td")
    table_data.append([cell.text.strip() for cell in cells])

# Match header length to longest row
max_cols = max(len(r) for r in table_data)
if len(header) < max_cols:
    header += [f"Extra_{i}" for i in range(len(header) + 1, max_cols + 1)]

# Create DataFrame
df = pd.DataFrame(table_data, columns=header)

# Save CSV
df.to_csv("windows10_version_history.csv", index=False, encoding="utf-8")
driver.quit()

print("✅ CSV saved: windows10_version_history.csv")

