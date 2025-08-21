from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import csv
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

driver = webdriver.Chrome()
driver.get("https://www.troemner.com/Calibration-Weights/Balance-Calibration-Weights/OIML-Calibration-Weight-Sets/c/3944")
time.sleep(5)

# CSV setup
csv_file = open("abc.csv", "w", newline="", encoding="utf-8")
csv_writer = csv.writer(csv_file)
csv_writer.writerow(['vendor', 'productName', 'model', 'description', 'productURL', 'cost'])

# --- Scroll until all products load ---
last_height = driver.execute_script("return document.body.scrollHeight")
while True:
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(3)  # wait for lazy loading
    new_height = driver.execute_script("return document.body.scrollHeight")
    if new_height == last_height:
        break
    last_height = new_height

# ✅ NOW grab all products after scrolling
wait = WebDriverWait(driver, 20)
products = wait.until(EC.presence_of_all_elements_located((By.XPATH, '//li[contains(@class,"product-item")]')))

# Extract product data
for product in products:
    vendor = "troemner"
    
    # Product Name and URL
    try:
        link_element = product.find_element(By.XPATH, './/header/h3/a')
        product_name = link_element.text.strip()
        product_url = link_element.get_attribute("href")
    except:
        product_name = ""
        product_url = ""
    
    # Model (number inside card)
    try:
        model_span = product.find_element(By.XPATH, './/header/h3/span[contains(@class,"code")]')
        model = model_span.text.strip().replace("(", "").replace(")", "")
    except:
        model = ""
    
    # Description
    try:
        description_div = product.find_element(By.XPATH, './/div[contains(@class,"description product-description")]')
        description = description_div.text.strip()
    except:
        description = ""
    
    # Cost
    try:
        cost = product.find_element(By.XPATH, './/span[contains(@class,"price")]').text.strip()
    except:
        cost = ""
    
    csv_writer.writerow([vendor, product_name, model, description, product_url, cost])

csv_file.close()
driver.quit()
print("CSV created successfully with all products!")
