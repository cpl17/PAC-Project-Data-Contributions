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


home_page = "https://midatlanticnatives.com/product-category/bare-root-native-plants/"

driver.get(home_page)

#TODO: Make this dynamic
for i in range(7):
    driver.execute_script("window.scrollTo(0,document.body.scrollHeight)")
    time.sleep(3)

#Find link elements for each plant, use a cleaned version of the link text (Full inventory text)
#to create a list of all the plants on the page. 
link_elements = driver.find_elements(By.CSS_SELECTOR,"div h2 a")
all_names_text = [element.text for element in link_elements]
all_names = [" ".join(x.split(" ")[:2]).strip(",") for x in all_names_text]
pd.Series(all_names).to_csv("Output/MidAtlantic_FullInventory.csv",encoding='utf-8',index=False)


#Find Matches. All relevant links have a child italize tag that holds the name 
for link in link_elements:
    try:
        name = " ".join((link.text).split(" ")[:2]).strip(",")

    except:
        continue

    if name in scientific_names:
        matches_list.append(name)
        match_urls_list.append(link.get_attribute("href"))



driver.close()


era_al = era_al[["USDA Symbol","Scientific Name"]]
matches_df = pd.DataFrame({"Scientific Name":matches_list,"Root":["MidAtlanticNatives.com"]*(len(matches_list)),"Web":match_urls_list})
final = pd.merge(matches_df,era_al,on="Scientific Name",how="left")
final.rename({"USDA Symbol":"USDA"},axis=1,inplace=True)
final = final[["USDA","Scientific Name","Root","Web"]]
final = final.drop_duplicates(subset="Scientific Name",keep="first")
final.to_csv("Output/MidAtlantic.csv",index=False)

pd.Series(all_names).to_csv("Output/MidAtlantic_FullInventory.csv",encoding='utf-8',index=False)




    
