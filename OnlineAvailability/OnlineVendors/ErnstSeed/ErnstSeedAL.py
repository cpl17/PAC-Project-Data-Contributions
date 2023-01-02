import pandas as pd
import time

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service

from selenium.webdriver.common.by import By

import os
print(os.getcwd())
options = Options()
options.add_argument("start-maximized")
options.add_experimental_option("detach", True)
ser = Service("C:\Program Files (x86)\chromedriver.exe")

driver = webdriver.Chrome(service=ser, options=options)

DELAY = 2

#Metadata and Source Data
era_al = pd.read_excel("../Data/ERA_Alabama.xlsx",sheet_name="All Plants")
common_names = era_al["Common Name"].to_list()
scientific_names = era_al["Scientific Name"].to_list()

#Lists to fill with Names of Matches and URLs
matches_list = []
match_urls_list = []

#Open Species Page (Contains all Seeds on the site)
home_page = "https://www.ernstseed.com/products/individual-species/"
driver.get(home_page)


#Get the full inventory and create a csv
name_elements = driver.find_elements(By.CSS_SELECTOR,"div h3 strong a i")
all_names = [name.text for name in name_elements]
pd.Series(all_names).to_csv("Output/ErnstSeed_FullInventory",index=False)

#Get Link Elements - Anchor tags that contain the direct link and the name of the plant
link_elements = driver.find_elements(By.CSS_SELECTOR,"div h3 strong a")

#Find Matches. All relevant links have a child italize tag that holds the name 
for link in link_elements:
    try:
        name_element = link.find_element(By.TAG_NAME,"i")
        name = name_element.text.split(',')[0] 
        print(name)
    except:
        continue

    if name in scientific_names:
        matches_list.append(name)
        match_urls_list.append(link.get_attribute("href"))


driver.close()


era_al = era_al[["USDA Symbol","Scientific Name"]]
matches_df = pd.DataFrame({"Scientific Name":matches_list,"Root":["ErnstSeed.com"]*(len(matches_list)),"Web":match_urls_list})

final = pd.merge(matches_df,era_al,on="Scientific Name",how="left")
final = final.drop_duplicates(subset="Scientific Name",keep='first')
final.rename({"USDA Symbol":"USDA"},axis=1,inplace=True)
final = final[["USDA","Scientific Name","Root","Web"]]
final = final.drop_duplicates(subset="Scientific Name",keep="first")
final.to_csv("Output/ErnstSeed.csv",index=False)





