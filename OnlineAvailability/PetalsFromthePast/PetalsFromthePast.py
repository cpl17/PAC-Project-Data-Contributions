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

driver = webdriver.Chrome(service=ser, options=options)


matches_list = []
match_urls_list = []
all_names = []

for page_number in range(1,23):

    if page_number == 1:

        home_page = "https://petalsfromthepast.com/product-category/plants/"
        driver.get(home_page)
        WebDriverWait(driver, DELAY).until(EC.presence_of_element_located((By.CSS_SELECTOR,"h2.woocommerce-loop-product__title")))
        time.sleep(5)
    
    else:

        page = f"https://petalsfromthepast.com/product-category/plants/page/{page_number}/"
        driver.get(page)
        WebDriverWait(driver, DELAY).until(EC.presence_of_element_located((By.CSS_SELECTOR,"p.woocommerce-result-count"))) #there is a random blank page (8), have to use "Showing ... results" text
        time.sleep(5)


    link_elements = driver.find_elements(By.CSS_SELECTOR,"li a.woocommerce-loop-product__link")
    links = [link_element.get_attribute("href") for link_element in link_elements]

    name_elements = driver.find_elements(By.CSS_SELECTOR,"h2.woocommerce-loop-product__title")
    names = [name_element.text for name_element in name_elements]
    all_names += names

    page_list = list(zip(links,names))

    for link_name_tuple in page_list:

        #Source name "Amsonia tabernaemontana" is found in name on webpage as "Amsonia tabernaemontana – ‘Bluestar"
        for name in all_names:
            if name in link_name_tuple[1]:
                matches_list.append(link_name_tuple[1])
                match_urls_list.append(link_name_tuple[0])
                print(name,link_name_tuple[1])
                break

    time.sleep(5)

    print(page_number,"\n")

driver.close()

pd.DataFrame({"ScientificNames":matches_list,"URLS":match_urls_list}).to_csv("PetalFromthePast.csv")

pd.Series(all_names).to_csv("PetalsFromthePast_AllNames.csv",encoding='utf-8')