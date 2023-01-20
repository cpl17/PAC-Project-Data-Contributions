import pandas as pd
import numpy as np


from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service

options = Options()
options.add_argument("start-maximized")
options.add_experimental_option("detach", True)
ser = Service("C:\Program Files (x86)\chromedriver.exe")

STATE = "PA"
ERA_SOURCE_DIRECTORY = r"C:\Users\CPL17\OneDrive\Documents\Code\Dev Projects\Current\PAC_New\Data"
OUTPUT_DIRECTORY = r"C:\Users\CPL17\OneDrive\Documents\Code\Dev Projects\Current\PAC_New\ERA_MissingDataScripts\Output\AllScrapedData_Original"

source_data = pd.read_excel(ERA_SOURCE_DIRECTORY + f"/ERA_{STATE}.xlsx",sheet_name="All Plants")
names = source_data["Scientific Name"]


full_df = None
dfs = []
list_of_unique_columns = []


driver = webdriver.Chrome(service=ser, options=options)

for name in names:

    print(name)

    driver.get(f"https://www.gardenia.net/plant/{name}")
    source = driver.page_source

    #Some pages don't exist but still return 200
    try:
        tables = pd.read_html(source)
    except ValueError:
        continue

    #The table is 2xm, first column are the plant characteristics names, the second are the values
    plant_df = tables[0].set_index(0).T
    plant_df.index = [name.replace("-"," ")]


    dfs.append(plant_df)


    for column in plant_df.columns:
        if column not in list_of_unique_columns:
            list_of_unique_columns.append(column)



driver.close()



for df in dfs:
    #This is done by default when join in pd.concat()
    for name in list(set(list_of_unique_columns).difference(df.columns)):
        df[name] = np.NaN
        df.reindex(list_of_unique_columns,axis=1)

full_df = pd.concat(dfs)

full_df.to_csv(OUTPUT_DIRECTORY +  f"/Gardenia_{STATE}_Unedited.csv")



