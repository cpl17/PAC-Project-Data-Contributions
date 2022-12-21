import pandas as pd
import numpy as np
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

number_of_pages = 15
start = 0
full_df = None

#Get Data from <table> on each page 
for i in range(0,number_of_pages):

    driver.get(f"https://www.wildflower.org/suppliers/search.php?start={start}&pagecount=100")

    time.sleep(5)

    table = driver.find_element(By.CSS_SELECTOR,"div table")
    list_of_table_dfs =  pd.read_html(table.get_attribute("outerHTML"))

    df = list_of_table_dfs[0]
    
    if start == 0: 
        column_names = df.iloc[0,:].to_list()
    
    #Two rows of column names
    df.drop(index=df.index[0], axis=0, inplace=True)
    df.drop(index=df.index[-1], axis=0, inplace=True)

    if full_df is None:
        
        full_df = df 
    else:
        full_df = pd.concat([full_df,df])
    
    start += 100

#Write to csv
full_df.columns = column_names
full_df.reset_index(drop=True,inplace=True)
full_df.to_csv("WildflowerNurseryList.csv")


#Clean Data
full_df["State"] = full_df["location"].apply(lambda x: x.split(",")[1].strip() if isinstance(x,str) else x) #location is city,state
full_df["City"] = full_df["location"].apply(lambda x: x.split(",")[0] if isinstance(x,str) else x)
full_df.columns = pd.Series(full_df.columns).str.capitalize()
full_df.drop("Location",axis=1,inplace=True)

state_codes = ["AL", "AK", "AZ", "AR", "CA", "CO", "CT", "DE", "DC", "FL", "GA", "HI", "ID", "IL", "IN", 
"IA", "KS", "KY", "LA", "ME", "MD", "MA", "MI", "MN", "MS", "MO", "MT", "NE", "NV", "NH", "NJ", "NM", 
"NY", "NC", "ND", "OH", "OK", "OR", "PA", "PR", "RI", "SC", "SD", "TN", "TX", "UT", "VT", "VA", "VI", 
"WA", "WV", "WI", "WY"]

full_df["State"] = full_df["State"].apply(lambda x: x if x in state_codes else np.nan)

full_df.dropna(subset=["State"],inplace=True)
full_df.to_csv("WildflowerNurseryList2.csv")