
import pandas as pd
import os
import numpy as np


SOURCE_DATA_DIRECTORY = r"C:\Users\CPL17\OneDrive\Documents\Code\Dev Projects\Current\PAC_New\Data"
WEBDATA_SOURCE_DIRECTORY = r"C:\Users\CPL17\OneDrive\Documents\Code\Dev Projects\Current\PAC_New\ERA_MissingDataScripts\Output\AllScrapedData_Cleaned"
OUTPUT_DIRECTORY = r"C:\Users\CPL17\OneDrive\Documents\Code\Dev Projects\Current\PAC_New\ERA_MissingDataScripts\Output"
STATE = "PA"
DATE = "1_20"

source_data = pd.read_csv(SOURCE_DATA_DIRECTORY + f"/ERA_{STATE}_Reduced.csv",index_col=0)

print(source_data.shape)


source_dict = source_data.to_dict()

print(source_data.isna().sum())
print("Total Missing: ",source_data.isna().sum().sum())

for file in os.listdir(WEBDATA_SOURCE_DIRECTORY):

    print(file)

    if STATE not in file:
        continue 

    df = pd.read_csv(WEBDATA_SOURCE_DIRECTORY + "/" + file,dtype=str,index_col=0)

    
    df_dict = df.to_dict()

    for col in df.columns:

        for name in source_data.index:

            if source_dict[col][name] is np.nan:
                if (name in df.index) and (df_dict[col][name] is not np.nan):
                   
                    source_dict[col][name] = df_dict[col][name]

    source_data = pd.DataFrame(source_dict)
    
    print(f"After Updating: {str(df.columns.to_list())}" + " using " + file)
    print("Total Missing: ",source_data.isna().sum().sum())

    print(source_data.isna().sum())



print(source_data.columns)

    


source_data.to_csv(OUTPUT_DIRECTORY + f"/ERA_{STATE}_Cleaned_Updated_{DATE}.csv")


