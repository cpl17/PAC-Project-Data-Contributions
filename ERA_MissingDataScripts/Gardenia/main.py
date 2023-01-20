import pandas as pd
import json
import numpy as np


from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service

from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

options = Options()
options.add_argument("start-maximized")
options.add_experimental_option("detach", True)
ser = Service("C:\Program Files (x86)\chromedriver.exe")


source_data = pd.read_excel("../../Data/ERA_Alabama.xlsx",sheet_name="All Plants")


# names = source_data["Scientific Name"]
# names = ["-".join(name.lower().split(" ")) for name in names]

# for name in names:
#     response = requests.get(f"https://www.gardenia.net/plant/{name}")
#     if response.status_code != 200:
#         names.remove(name)

# with open("Names.txt","w") as f:
#     for name in names:
#         f.write(name + "\n")


#Names are tab separated scientific names, in accordance with the strucuture of the url
with open("Names.txt") as f:
    names = f.readlines()

full_df = None
dfs = []
list_of_unique_columns = [] #Set this to whatever is read in from UniqueColumns, if starting from a checkpoint


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


    with open("Backup.txt",'w') as f:
        json_string = json.dumps([df.to_dict() for df in dfs])
        f.write(json_string)

    with open("UniqueColumns.txt",'w') as f:
        for column in list_of_unique_columns:
            f.write(column + "\n")


driver.close()


#Skip if successful in first run. Note: this uses the unique columns gathered only after the checkpoint
#Update code to read in all columnsfrom txt file if necessary
# with open("Backup.txt") as f:
#     json_string = f.read()
#     dfs  = json.loads(json_string)


for df in dfs:
    #This is done by default when join in pd.concat()
    for name in list(set(list_of_unique_columns).difference(df.columns)):
        df[name] = np.NaN
        df.reindex(list_of_unique_columns,axis=1)

full_df = pd.concat(dfs)

full_df.to_csv("Gardenia_Unedited.csv")



