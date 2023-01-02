import requests 
import pandas as pd

era_al = pd.read_excel("../../../Data/ERA_Alabama.xlsx",sheet_name="All Plants")
common_names = era_al["Common Name"].to_list()
scientific_names = era_al["Scientific Name"].to_list()

matches_list = []
match_urls_list = []

for name in scientific_names:
    test_url = f"https://www.toadshade.com/{'-'.join(name.split())}.html"
    response = requests.get(test_url)
    status_code = response.status_code
    if status_code == 200:
        matches_list.append(name)
        match_urls_list.append(response.url)
        print(name,len(matches_list))
    


era_al = era_al[["USDA Symbol","Scientific Name"]]
matches_df = pd.DataFrame({"Scientific Name":matches_list,"Root":["ToadShade.com"]*(len(matches_list)),"Web":match_urls_list})
final = pd.merge(matches_df,era_al,on="Scientific Name",how="left")
final.rename({"USDA Symbol":"USDA"},axis=1,inplace=True)
final = final[["USDA","Scientific Name","Root","Web"]]

final.to_csv("Output/ToadShade.csv",index=False)

