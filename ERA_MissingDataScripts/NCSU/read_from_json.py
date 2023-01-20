import pandas as pd
import json

with open("Backup.json") as f:
    all_full_plant_dicts = json.loads(f.read())


list_of_dfs = None
for full_plant_dict in all_full_plant_dicts:
    df = pd.DataFrame.from_dict(full_plant_dict, orient='index')
    if list_of_dfs:
        list_of_dfs.append(df)
    else:
        list_of_dfs = [df]

full_df = pd.concat(list_of_dfs)
full_df.to_csv("NCSU_Final.csv")