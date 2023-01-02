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


# #Function that waits until the correct page is selected
# def wait_until_page_load(page_index):

#     if int(driver.find_element(By.CLASS_NAME,"wsite-selected").text) != (page_index +2):
#         time.sleep(5)
#         wait_until_page_load(page_index)

era_al = pd.read_excel("../../../Data/ERA_Alabama.xlsx",sheet_name="All Plants")
common_names = era_al["Common Name"].to_list()
scientific_names = era_al["Scientific Name"].to_list()


matches_list = []
match_urls_list = []
all_names = []


######### Scraping #########

driver = webdriver.Chrome(service=ser, options=options)

home_page = "https://www.plantmorenatives.com/store/c26/native_perennial_plant_store#/"

driver.get(home_page)

#Wait for pop-up and close. It does not return 
time.sleep(10)
pop_up = driver.find_element(By.XPATH,"//*[@id='leadform-popup-close-576d6d25-a6a2-40cb-ab77-1205e75d2f2e']")
pop_up.click()



xpaths_for_pages = ["first page"] + [f"//*[@id='wsite-com-category-product-group-pagelist']/a[{page_number}]" for page_number in range(3,8)]
for page_index,path in enumerate(xpaths_for_pages):

    if path != "first page":

        page_element = driver.find_element(By.XPATH,path)
        page_element.click()

        time.sleep(5)

        # wait_until_page_load(page_index)

    #Get all the links and plant names on the page
    link_elements = driver.find_elements(By.CLASS_NAME,"wsite-com-category-product-link")
    links = [link.get_attribute("href") for link in link_elements]
    
    name_elements = driver.find_elements(By.CLASS_NAME,"wsite-com-link-text")
    names_full_text = [name.text for name in name_elements]
    names = [x.split("'")[0].split("(")[0].strip("\n").rstrip() for x in names_full_text]
    all_names.extend(names)

    assert len(names) == len(links)

    
    for name,link in list(zip(names,links)):


        if name in scientific_names:
            print(name,page_index)
            matches_list.append(name)
            match_urls_list.append(link)

    


driver.close()


era_al = era_al[["USDA Symbol","Scientific Name"]]
matches_df = pd.DataFrame({"Scientific Name":matches_list,"Root":["PlantMoreNatives.com"]*(len(matches_list)),"URL":match_urls_list})

final = pd.merge(matches_df,era_al,on="Scientific Name",how="left")
final.rename({"USDA Symbol":"USDA"},axis=1,inplace=True)
final = final[["USDA","Scientific Name","Root","Web"]]
final = final.drop_duplicates(subset="Scientific Name",keep="first")
final.to_csv("Output/PlantMoreNatives.csv",index=False)

pd.Series(all_names).to_csv("Output/PlantMoreNatives_FullInventory.csv",encoding='utf-8',index=False)





