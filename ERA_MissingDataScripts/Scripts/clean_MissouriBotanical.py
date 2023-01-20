import pandas as pd


STATE = "PA"
NURSERY = "MissouriBotanical"
WEBDATA_SOURCE_DIRECTORY = r"C:\Users\CPL17\OneDrive\Documents\Code\Dev Projects\Current\PAC_New\ERA_MissingDataScripts\Output\AllScrapedData_Original"
OUTPUT_DIRECTORY = r"C:\Users\CPL17\OneDrive\Documents\Code\Dev Projects\Current\PAC_New\ERA_MissingDataScripts\Output\AllScrapedData_Cleaned"
FORMAT_OR_UNEDITED = "Unedited"

data = pd.read_csv(WEBDATA_SOURCE_DIRECTORY + f"/{NURSERY}_{STATE}_{FORMAT_OR_UNEDITED}.csv",index_col=0)
relevant_columns = ["Sun","Flower","Bloom Time","Height","Bloom Description","Water"]
data= data[relevant_columns]


#Height -> Height (feet)
def determine_height(cell_value):
    x = cell_value.split(" to ")
    f = lambda y: str(round(float(y.strip()),1)) if "." in y else y.strip()
    x = list(map(f,x))
    return "–".join(x)


data["Height (feet)"] = data["Height"].str.replace("feet","").str.replace(".00","")
data["Height (feet)"] = data["Height (feet)"].apply(determine_height)


# Bloom Time -> Flowering Months
def clean_bloom(cell_value):
    x = cell_value.split("to")
    x = list(map(lambda y : (y.strip())[:3],x))
    return "–".join(x)


data["Flowering Months"] = data["Bloom Time"].apply(clean_bloom)


# Flower -> Showy
def determine_showy(cell_value):
    #If showy, its first in comma separated string
    if isinstance(cell_value,float):
        return cell_value
    x = cell_value.split(",")[0]
    x = x.strip()
    if x == "Showy":
        return "Yes"
    else:
        return "No" 


data["Showy"] = data["Flower"].apply(determine_showy)

#Bloom Description -> Flower Color


path = r"C:\Users\CPL17\OneDrive\Documents\Code\Dev Projects\Current\PAC_New\ERA_MissingDataScripts\Output\UniqueValues.xlsx"
era_unique = pd.read_excel(path,sheet_name="ERA_AL")


source_colors = era_unique["Flower Color"].dropna()


def determine_color(cell_value):
    if isinstance(cell_value,float):
        return cell_value
    
    x = cell_value.replace("ish","")

    for color in source_colors:
        if color == x:
            return color
    for color in source_colors:
        if color in x:
            return color


data["Flower Color"] = data["Bloom Description"].apply(determine_color)


# Sun -> Sun Exposure


def clean_exposure(cell_value):
    if isinstance(cell_value,float):
        return cell_value

    x = cell_value.split(" to ")
    for i,val in enumerate(x):
        if val.lower().strip() == "full sun":
            x[i] = "Sun"
        if val.lower().strip() == "full shade":
            x[i] = "Shade" 
        if val.lower().strip() == "part shade":
            x[i] = "Part Shade"       
        
    return ",".join(x)       


data["Sun Exposure"] = data["Sun"].apply(clean_exposure)


# Water -> Soil Moisture


import numpy as np
def get_soilmoisture(cell_value):
    if isinstance(cell_value,float):
        return cell_value
    x = cell_value.strip().title()
    if x == "Dry To Medium":
        return "Moist"
    elif x in ["Wet","Dry"]:
        return x
    else:
        return np.nan


data["Soil Moisture"] = data["Water"].apply(get_soilmoisture)



data.drop(["Height","Bloom Time","Flower","Sun","Bloom Description","Water"],axis=1,inplace=True)
data.to_csv(OUTPUT_DIRECTORY + f"/{NURSERY}_{STATE}.csv",encoding='utf-8')


