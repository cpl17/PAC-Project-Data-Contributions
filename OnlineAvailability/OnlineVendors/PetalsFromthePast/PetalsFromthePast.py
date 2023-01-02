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


era_al = pd.read_excel("../Data/ERA_Alabama.xlsx",sheet_name="All Plants")
common_names = era_al["Common Name"].to_list()
scientific_names = era_al["Scientific Name"].to_list()

driver = webdriver.Chrome(service=ser, options=options)


matches_list = []
match_urls_list = []
all_names = []

for page_number in range(1,23):

    if page_number == 1:

        home_page = "https://petalsfromthepast.com/product-category/plants/"
        driver.get(home_page)
        WebDriverWait(driver, DELAY).until(EC.presence_of_element_located((By.CSS_SELECTOR,"h2.woocommerce-loop-product__title")))
        time.sleep(2)
    
    else:

        page = f"https://petalsfromthepast.com/product-category/plants/page/{page_number}/"
        driver.get(page)
        WebDriverWait(driver, DELAY).until(EC.presence_of_element_located((By.CSS_SELECTOR,"p.woocommerce-result-count"))) #there is a random blank page (8), have to use "Showing ... results" text
        time.sleep(2)


    link_elements = driver.find_elements(By.CSS_SELECTOR,"li a.woocommerce-loop-product__link")
    links = [link_element.get_attribute("href") for link_element in link_elements]

    name_elements = driver.find_elements(By.CSS_SELECTOR,"h2.woocommerce-loop-product__title")
    names = [name_element.text for name_element in name_elements]
    all_names += names

    page_list = list(zip(links,names))

    for link_name_tuple in page_list:

        #Source name "Amsonia tabernaemontana" is found in name on webpage as "Amsonia tabernaemontana – ‘Bluestar"
        for name in scientific_names:
            if name in link_name_tuple[1]:
                matches_list.append(name)
                match_urls_list.append(link_name_tuple[0])
                print(name,link_name_tuple[1])
                break
        
        for i,name in enumerate(common_names):
            if name in link_name_tuple[1]:
                matches_list.append(scientific_names[i]) #Need a consistent column to match on, if common name found, store match my it's corresponding scientific name
                match_urls_list.append(link_name_tuple[0])
                print(name,link_name_tuple[1])
                break
        

        

    time.sleep(5)

    print(page_number,"\n")

driver.close()


era_al = era_al[["USDA Symbol","Scientific Name"]]
petals_matches_df = pd.DataFrame({"Scientific Name":matches_list,"Root":["PetalsFromthePast.com"]*(len(matches_list)),"Web":match_urls_list})
final = pd.merge(petals_matches_df,era_al,on="Scientific Name",how="left")
final.rename({"USDA Symbol":"USDA"},axis=1,inplace=True)
final = final[["USDA","Scientific Name","Root","Web"]]
final = final.drop_duplicates(subset="Scientific Name",keep="first")
final.to_csv("Output/PetalFromthePast.csv",index=False)

pd.Series(all_names).to_csv("Output/PetalsFromthePast_FullInventory.csv",encoding='utf-8')