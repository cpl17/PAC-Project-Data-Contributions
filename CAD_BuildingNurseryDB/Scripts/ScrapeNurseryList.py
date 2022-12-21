import pandas as pd
import time

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service

from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

options = Options()
options.add_argument("start-maximized")
options.add_experimental_option("detach", True)
ser = Service("C:\Program Files (x86)\chromedriver.exe")

driver = webdriver.Chrome(service=ser, options=options)

states = ["Alabama", "Alaska", "Arizona", "Arkansas", "California", "Colorado", "Connecticut", "Delaware", "Florida", 
"Georgia", "Hawaii", "Idaho", "Illinois", "Indiana", "Iowa", "Kansas", "Kentucky", "Louisiana", "Maine", 
"Maryland", "Massachusetts", "Michigan", "Minnesota", "Mississippi", "Missouri", "Montana", "Nebraska", "Nevada", 
"New Hampshire", "New Jersey", "New Mexico", "New York", "North Carolina","North Dakota", "Ohio", "Oklahoma", "Oregon", "Pennsylvania", "Rhode Island", "South Carolina", "South Dakota", "Tennessee",
 "Texas", "Utah", "Vermont", "Virginia", "West Virginia", "Wisconsin", "Wyoming"] #Washington is not available


states = list(map(lambda x: "%20".join(x.split(" ")),states))

full_df = None

#Get Data from <table> on each page 
for state in states:
    print(state)

    driver.get(f"https://www.nurserytrees.com/States/state%20{state}.htm")

    time.sleep(5)

    tables = driver.find_elements(By.CSS_SELECTOR,"table")

    #There are multiple tables on each page
    full_state_table = None
    for table in tables:
        section_df = pd.read_html(table.get_attribute("outerHTML"))[0]
        if full_state_table is None:
            full_state_table = section_df
        else:
            full_state_table = pd.concat([full_state_table,section_df])


    full_state_table[4] = state

    if full_df is None:
        
        full_df = full_state_table 
    else:
        full_df = pd.concat([full_df,full_state_table])
    
    
    
    

#Write to csv
full_df.columns = ["City","Name","Address","Phone Number","State"]
full_df.reset_index(drop=True,inplace=True)
full_df.to_csv("NurseryTreeList.csv")