
import pandas as pd
import time

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service

from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By

from selenium.common.exceptions import TimeoutException

options = Options()
options.add_argument("start-maximized")
options.add_experimental_option("detach", True)
ser = Service("C:\Program Files (x86)\chromedriver.exe")





source_data = pd.read_excel("../../Data/ERA_Alabama.xlsx",sheet_name="All Plants")


temp = pd.read_csv("SearchResults.csv")
symbols_in_USDA = temp["Accepted Symbol"]
symbols = source_data["USDA Symbol"]
symbols_in_both = symbols[symbols.isin(symbols_in_USDA)]



# Scrape All
list_of_dfs = []
errors = []


driver = webdriver.Chrome(service=ser, options=options)
wait = WebDriverWait(driver, 3)

for symbol in symbols_in_both:

    print(symbol)

    time.sleep(5)

    
    driver.get(f"https://plants.usda.gov/home/plantProfile?symbol={symbol}")

    try:
        wait.until(EC.presence_of_element_located(((By.ID,"characteristics"))))  

    except TimeoutException:
        errors.append(symbol)
        continue



    charactersitics_div = driver.find_element(By.ID,"characteristics")
   
    source = charactersitics_div.get_attribute("innerHTML")

    
    try:
        table = pd.read_html(source)[0]
    
    except:
        errors.append(symbol)
        continue
  

    table.columns = ["Column","Value"]

    group_index = (table["Column"]==table["Value"])
    table = table[~group_index]

    table.set_index("Column",inplace=True)
    table = table.T
    table.index = [symbol]
    table.columns.names = [None]

    list_of_dfs.append(table)

    print(errors)


full_df = pd.concat(list_of_dfs)
full_df.to_csv("USDA_Plants.csv")

