import csv
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By

# Setup WebDriver (e.g., Chrome)
driver = webdriver.Chrome()

try:
    driver.get("https://www.paloaltonetworks.com/services/support/end-of-life-announcements/hardware-end-of-life-dates")
    
    # Adjust the XPath expressions based on actual page structure.
    # Here we assume each product entry is within some table rows or divs with known patterns.
    
    # Sample extraction logic:
    products = driver.find_elements(By.XPATH, "//tr")  # adjust based on actual table markup
    
    data_rows = []
    
    for row in products:
        try:
            product_name = row.find_element(By.XPATH, "./td[1]").text.strip()
            eol_date_raw = row.find_element(By.XPATH, "./td[3]").text.strip()
            resource = row.find_element(By.XPATH, "./td[4]/a").get_attribute("href").strip()
            recommended = row.find_element(By.XPATH, "./td[6]").text.strip()
        except:
            continue
        
        # Convert date to dd-mm-yyyy:
        try:
            dt = datetime.strptime(eol_date_raw, "%b %d, %Y")
        except ValueError:
            try:
                dt = datetime.strptime(eol_date_raw, "%B %d, %Y")
            except ValueError:
                continue
        eol_date = dt.strftime("%d-%m-%Y")
        
        data_rows.append({
            "vendor": "Palo Alto",
            "productName": product_name,
            "EOL Date": eol_date,
            "resource": resource,
            "Recommended replacement": recommended
        })
    
    # Export to CSV
    with open("palo_alto_eol.csv", "w", newline="") as csvfile:
        fieldnames = ["vendor", "productName", "EOL Date", "resource", "Recommended replacement"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for entry in data_rows:
            writer.writerow(entry)

finally:
    driver.quit()
