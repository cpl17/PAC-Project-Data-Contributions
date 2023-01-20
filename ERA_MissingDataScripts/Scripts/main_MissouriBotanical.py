import pandas as pd
import string


from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service

from selenium.webdriver.common.by import By

options = Options()
options.add_argument("start-maximized")
options.add_experimental_option("detach", True)
ser = Service("C:\Program Files (x86)\chromedriver.exe")

STATE="PA"
SOURCE_DATA_DIRECTORY = r"C:\Users\CPL17\OneDrive\Documents\Code\Dev Projects\Current\PAC_New\Data\Pennsylvania"
OUTPUT_DIRECTORY = r"C:\Users\CPL17\OneDrive\Documents\Code\Dev Projects\Current\PAC_New\ERA_MissingDataScripts\Output\AllScrapedData_Original"

source_data = pd.read_excel(SOURCE_DATA_DIRECTORY + "/ERA_{STATE}.xlsx",sheet_name="All Plants")
scientific_names = source_data["Scientific Name"].to_list()

matches = []


driver = webdriver.Chrome(service=ser, options=options)

for letter in string.ascii_uppercase:

    print(letter)

    driver.get(f"https://www.missouribotanicalgarden.org/PlantFinder/PlantFinderListResults.aspx?letter={letter}")


    outer_div = driver.find_element(By.CLASS_NAME,"p2")
    
    link_elements = outer_div.find_elements(By.CSS_SELECTOR,"div div a")
    names = [el.text.split("'")[0] for el in link_elements]
    links = [el.get_attribute("href") for el in link_elements]
    
    all_name_link_pairs = list(set(list(zip(names,links))))
    all_name_link_pairs.sort()

    for pair in all_name_link_pairs:
        if pair[0] in scientific_names:
            matches.append(pair)

driver.close()



driver = webdriver.Chrome(service=ser, options=options)

all_plant_dicts = {}

for name,link in matches:
    print(name)
    driver.get(link)

    row_elements = driver.find_elements(By.CSS_SELECTOR,"div.column-right div.row")
    plant_dict = {name:{}}
    for el in row_elements[:-1]:
        column,value = el.text.split(":")
        plant_dict[name].update({column:value})
    all_plant_dicts.update(plant_dict)


pd.DataFrame(all_plant_dicts).T.to_csv(OUTPUT_DIRECTORY + f"/MissouriBotanical_{STATE}_Unedited.csv")