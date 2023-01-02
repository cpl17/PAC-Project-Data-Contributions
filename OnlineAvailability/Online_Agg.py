import pandas as pd


#Note: The inexplicable USDA back and forth is to keep with the naming conventions for each sheet
#Likely does not matter
data = pd.read_csv("Output/ONLINE.csv")
data.rename({"USDA":"USDA Symbol"},axis=1,inplace=True)

metadata = pd.read_excel("../Data/ERA_Alabama.xlsx",sheet_name="All Plants")


f = lambda x: ', '.join(map(str, set(x)))
online_agg = data.groupby("USDA Symbol").agg({"Root":[f,len],"Web":f})

online_agg.reset_index(inplace=True)
online_agg.columns = ["USDA Symbol","Root","COUNT","Web"]

metadata = metadata[["USDA Symbol","Scientific Name","Common Name"]]
metadata.columns = ["USDA Symbol","Scientific Name","Common Name"]

final = online_agg.merge(metadata,on="USDA Symbol",how="left")
final["Common Name"] = final["Common Name"].str.title()
final["String"] = [f"{row['Common Name']} ({row['Scientific Name']}): {row['Root']}" for _,row in final.iterrows()]

final.rename({"USDA Symbol":"USDA"},axis=1,inplace=True)

final.to_csv("Output/ONLINE_AGG.csv",index=0)