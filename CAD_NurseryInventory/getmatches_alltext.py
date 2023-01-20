import pandas as pd
import os

#The source database
era_al = pd.read_excel("../Data/ERA_Alabama.xlsx",sheet_name="All Plants")
era_al = era_al[["Scientific Name","Common Name","USDA Symbol"]]
era_al_copy = era_al.copy()

for col in era_al:
    era_al[col] = era_al[col].str.lower()


count_dict = {}
list_of_dfs = []

#For each file -> read file into string,check common and scientific names for each plant against the string. Using a copy of the 
# source dataframe, remove all non-matched values,  and append to a list

for file in os.listdir("./TextFiles"):

    full_path = "./TextFiles/" + file

    with open(full_path,encoding='unicode_escape') as f:
        string = f.read().lower()
    
    df = era_al.copy()
    df["Match"] = 0

    com_names = df["Common Name"].to_list()
    scientific_names = df["Scientific Name"].to_list()


    #Check the string for the common name and scientific name. 
    # If there is a match, replace match with a 1
    for i,tup in enumerate(list(zip(com_names,scientific_names))):
        common_name = tup[0]
        scientific_name = tup[1]
        if ((common_name in string) | (scientific_name in string)):
            df.loc[i,"Match"] = 1
            print("match")

    #Create a nursery column
    nursery = file.split(".")[0]
    df["Nursery"] = nursery
    
    #Reduce the df to only where there is a match
    df = df[df.Match == 1]

    #Find the number of matches and append to the count dict
    count = df.Match.sum()
    count_dict.update({nursery:count})

    df.drop("Match",axis=1,inplace=True)
    list_of_dfs.append(df)

nursery_matches_source = pd.concat(list_of_dfs)

### Output: A long df with entries SYMBOL NURSERY URL. ###
# Note: URLS are the nursery urls NOT the urls used for the http requests. 
local_long = nursery_matches_source.copy()
nursery_info = pd.read_excel("./Source Data/Local_Catalog_URLS.xlsx",sheet_name="AL")

# nursery_info = nursery_info.loc[(nursery_info["Solved_Open"] == "Yes"),["Nursery","Nursery URL"]].drop_duplicates(subset="Nursery")
mapping = nursery_info.set_index("Nursery").to_dict()["Nursery URL"] #Nursery to URL


local_long["URL"] = local_long["Nursery"].map(mapping)
local_long = local_long[["USDA Symbol","Nursery","URL"]]
local_long.columns = ["USDA Symbol","Source","URL"]
local_long["USDA Symbol"] = local_long["USDA Symbol"].str.upper()
local_long.to_csv("./Output/Local_Long.csv")

### Output: Aggegrate along symbol to get SYMBOL URLS COUNT df ###
df = nursery_matches_source.copy()
df["URL"] = df["Nursery"].map(mapping)
df = df[["USDA Symbol","Nursery","URL"]]

f = lambda x: ', '.join(map(str, set(x)))
local_agg = df.groupby("USDA Symbol").agg({"URL":[f,len],"Nursery":f})
local_agg.reset_index(inplace=True)
local_agg.columns = ["USDA Symbol","URLS","COUNT","Source"]
local_agg["USDA Symbol"] = local_agg["USDA Symbol"].str.upper()
local_agg = pd.merge(local_agg,era_al_copy,on="USDA Symbol",how="left")
local_agg["Common Name"] = local_agg["Common Name"].str.title()
local_agg["String"] = [f"{row['Common Name']} ({row['Scientific Name']}): {row['Source']}" for _,row in local_agg.iterrows()]
local_agg.to_csv("./Output/Local_Agg.csv")


### Output: A dataframe of number of matches found for each nursery ###
count_df = pd.DataFrame(index = count_dict.keys(), data=count_dict.values(),columns=["Counts"])
count_df.to_csv("./Output/Counts.csv")
    
    



