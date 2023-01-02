import pandas as pd
import time

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service

from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait

options = Options()
options.add_argument("start-maximized")
options.add_experimental_option("detach", True)
ser = Service("C:\Program Files (x86)\chromedriver.exe")

DELAY = 2


era_al = pd.read_excel("../../../Data/ERA_Alabama.xlsx",sheet_name="All Plants")
common_names = era_al["Common Name"].to_list()
scientific_names = era_al["Scientific Name"].to_list()

driver = webdriver.Chrome(service=ser, options=options)


matches_list = []
match_urls_list = []
all_names = []

#Open Home Page, Get the number of pages
home_page = "https://www.prairiemoon.com/seeds/"
driver.get(home_page)
WebDriverWait(driver, DELAY).until(EC.presence_of_element_located((By.XPATH,'//*[@id="category-listing-wrapper"]/div[3]/div/span/div/a[8]')))
num_pages = int(driver.find_element(By.XPATH,'//*[@id="category-listing-wrapper"]/div[3]/div/span/div/a[8]').text)

for page_number in range(1,num_pages+1):

    if page_number != 1:

        page = f"https://www.prairiemoon.com/seeds/?page={page_number}"
        driver.get(page)
        WebDriverWait(driver, DELAY).until(EC.presence_of_element_located((By.CSS_SELECTOR,"p.category-product-name a")))
        time.sleep(5)


    link_elements = driver.find_elements(By.CSS_SELECTOR,"p.category-product-name a")

    for link in link_elements:

        name_element = link.find_element(By.TAG_NAME,"span")
        name = name_element.text
        all_names.append(name)


        if name in scientific_names:
            print(name,page_number)
            matches_list.append(name)
            match_urls_list.append(link.get_attribute("href"))

    time.sleep(5)
    


driver.close()


era_al = era_al[["USDA Symbol","Scientific Name"]]
matches_df = pd.DataFrame({"Scientific Name":matches_list,"Root":["PrairieMoon.com"]*(len(matches_list)),"Web":match_urls_list})


final = pd.merge(matches_df,era_al,on="Scientific Name",how="left")
final.rename({"USDA Symbol":"USDA"},axis=1,inplace=True)
final = final[["USDA","Scientific Name","Root","Web"]]
final = final.drop_duplicates(subset="Scientific Name",keep="first")
final.to_csv("Output/PrairieMoon.csv",index=False)

pd.Series(all_names).to_csv("Output/PrairieMoon_FullInventory.csv",encoding='utf-8',index=False)
    


