import pandas as pd
import os

#The source database
era_al = pd.read_excel("./Data/ERA_Alabama.xlsx",sheet_name="All Plants")
era_al = era_al[["Scientific Name","Common Name","USDA Symbol"]]

for col in era_al:
    era_al[col] = era_al[col].str.lower()


count_dict = {}
list_of_dfs = []

#For each file -> read file into string,check common and scientific names for each plant against the string. Using a copy of the 
# source dataframe, remove all non-matched values,  and append to a list

nursery = "TomDodd"
full_path = f"./CAD_NurseryInventory/TextFiles/{nursery}.txt"

with open(full_path,encoding='unicode_escape') as f:
    string = f.read().lower().replace("'","")
    print(string)

df = era_al.copy()
df["Match"] = 0 #Set all plants to no match

com_names = df["Common Name"].to_list()
scientific_names = df["Scientific Name"].to_list()


#Check the string for the common name and scientific name. 
# If there is a match, replace match with a 1
for i,tup in enumerate(list(zip(com_names,scientific_names))):
    common_name = tup[0]
    scientific_name = tup[1]
    if ((common_name in string) | (scientific_name in string)):
        df.loc[i,"Match"] = 1

#Create a nursery column
df["Nursery"] = nursery
print(df.head(10))

#Reduce the df to only where there is a match
df = df[df.Match == 1]

df.to_csv("TomDodd.csv")


    
    



