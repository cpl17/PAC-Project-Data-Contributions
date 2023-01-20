
import pandas as pd
import requests
from bs4 import BeautifulSoup
import json

BASE_URL = "https://plants.ces.ncsu.edu/plants/"
HEADERS = {
    "Accept-Language": "en-US,en;q=0.9",
    "User-Agent": "Chrome/87.0.4280.141"
}

source_data = pd.read_excel("../../Data/ERA_Alabama.xlsx",sheet_name="All Plants")


def create_dict(lst):

    '''This function will iterate through the list and create a new key-value pair in the dictionary
    whenever it encounters an element with a colon in it. This excludes the first element which will be 
    the outer key of the dictionary. 
    
    The value for each key will be a list of all the
    elements after the key element until the next element with a colon.'''
    
    #Set outer key as the group name (i.e. "Attributes")
    group_name = lst[0]
    result = {group_name:{}}
    

    current_key = None
    current_value = []
    for item in lst:
        if item == group_name:
            continue
        
        if ':' in item:

            #Edge Cases
            
            if ((item.startswith(("Height:","Width:","USA:","Canada:","Canada:","United States:","US:","Native:","INTRODUCED","Members of","This is a larval","This plant","It","Poison"))) | ("SOURCE:" in item)):
                current_value.append(item)
                continue

            #Set the current key's values to the current list of values
            if current_key:
                result[group_name][current_key] = current_value
            
            #Reset key and value list
            current_key = item
            current_value = []
        else:
            
            #THIS COULD CAUSE PROBLEMS
            if item != "":
                current_value.append(item)

    result[group_name][current_key] = current_value

    #Join the list into a string 
    for key in result[group_name].keys():
        result[group_name][key] = "|".join(result[group_name][key])



    return result



names = ["-".join(name.split()).lower() for name in source_data["Scientific Name"]]

all_full_plant_dicts = []



for name in names:

    print(name)
    
    #Create a Soup object from the request response text
    full_url = BASE_URL + name
    response = requests.get(url = full_url, headers = HEADERS)
    page = response.text 
    soup = BeautifulSoup(page,features='lxml')

    #Select all groups (Flowers) which contain the column:value pairs in a definition list format
    all_groups = soup.select("li.list-group-item dl")

    #If page not found is returned
    if len(all_groups) == 0:
        continue

    plant_dicts = [create_dict(x) for x in [group.text.split("\n")[1:] for group in all_groups]]

    full_plant_dict = {name:{}}
    #[{Flowers:{Flower Color:Red,...},...}...]
    for group_plant_dict in plant_dicts:
        #{Flower Color:Red,...}
        for column_value_dict in group_plant_dict.values():
            full_plant_dict[name].update(column_value_dict)

    #Write group-column groupings in case of future multi-indexing

    for plant_dict in plant_dicts:
        group_column_pairings = []
        group = list(plant_dict.keys())[0]
        for column in plant_dict[group].keys():
            group_column_pairings.append((group,column))
        
        if all_full_plant_dicts == []:
            with open("GC_pairings.txt","w") as f:
                f.write(str(group_column_pairings) + "\n")
        else:
            with open("GC_pairings.txt","a") as f:
                f.write(str(group_column_pairings)+ "\n")
    

    all_full_plant_dicts.append(full_plant_dict)


    #Backup in case of error
    # with open("Backup.json",'w') as f:
    #     json_string = json.dumps(all_full_plant_dicts)
    #     f.write(json_string)


#Create a df of each dict and concatenate
list_of_dfs = None
for full_plant_dict in all_full_plant_dicts:
    df = pd.DataFrame.from_dict(full_plant_dict, orient='index')
    if list_of_dfs:
        list_of_dfs.append(df)
    else:
        list_of_dfs = [df]

full_df = pd.concat(list_of_dfs)
full_df.to_csv("NCSU_Unedited.csv")

