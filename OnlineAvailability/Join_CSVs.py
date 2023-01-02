import os
import pandas as pd

all_files = list()
dir = '.'
walker = os.walk(dir)

for p,_,f in walker:
    all_files.extend(f)


relevant_files = []
for file_name in all_files:
    if (".csv" in file_name) & ("FullInventory" not in file_name):
        relevant_files.append(file_name)

full_df = None
for file_name in relevant_files:
    full_path = file_name.split(".")[0] + "/Output/" + file_name
    df = pd.read_csv(full_path)
    df.drop_duplicates(subset="Scientific Name",keep="first")

    if full_df is None:
        full_df = df
    else:
        full_df = pd.concat([full_df,df])

full_df.rename({"USDA Symbol":"USDA","URL":"Web"},axis=1,inplace=True)
full_df = full_df[["USDA","Scientific Name","Root","Web"]]
full_df.to_csv("../Output/ONLINE.csv",index=False)


      
    



    