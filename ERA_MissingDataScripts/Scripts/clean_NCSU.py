import pandas as pd

STATE = "PA"
NURSERY = "NCSU"
WEBDATA_SOURCE_DIRECTORY = r"C:\Users\CPL17\OneDrive\Documents\Code\Dev Projects\Current\PAC_New\ERA_MissingDataScripts\Output\AllScrapedData_Original"
OUTPUT_DIRECTORY = r"C:\Users\CPL17\OneDrive\Documents\Code\Dev Projects\Current\PAC_New\ERA_MissingDataScripts\Output\AllScrapedData_Cleaned"
FORMAT_OR_UNEDITED = "Formatted"



data = pd.read_csv(WEBDATA_SOURCE_DIRECTORY + f"/{NURSERY}_{STATE}_{FORMAT_OR_UNEDITED}.csv",index_col=0)
relevant_columns = ["Dimensions","Flower Value To Gardener","Light"]
data= data[relevant_columns]


# ## Dimensions -> Height (feet)
def determine_height(cell_value):
    if isinstance(cell_value,float):
        return cell_value

    x = cell_value.split("|")[0]

    x = x.replace("Height:","").replace("- ","")

    x = x.split(".")

    min_feet,max_feet = int(x[0].strip().replace(" ft","")),int(x[2].strip().replace(" ft",""))
    min_inches,max_inches = int(x[1].strip().replace(" in","")), int(x[3].strip().replace(" in",""))

    range_min = str(round((((min_feet*12) + min_inches) / 12),1))
    range_max = str(round((((max_feet*12) + max_inches) / 12),1))
    
    #Removing extra sig fig
    if ("0." not in range_min) | ("0.0"in range_min):
        range_min = range_min.replace(".0","")
    if ("0." not in range_max) | ("0.0"in range_max):
        range_max = range_max.replace(".0","")
    
    return "–".join([range_min,range_max])


data["Height (feet)"] = data["Dimensions"].apply(determine_height)


# ## Flower Value -> Showy
def determine_showy(cell_value):
    if isinstance(cell_value,float):
        return cell_value
    
    x = cell_value.split("|")

    if "Showy" in x:
        return "Yes"
    else:
        return "No"



data["Showy"] = data["Flower Value To Gardener"].apply(determine_showy)


# ## Light -> Sun Exposure
import numpy as np
def clean_exposure(cell_value):
    if isinstance(cell_value,float):
        return cell_value

    x = cell_value.split(" (")[0].strip().title()

    if x == "Full Sun":
        return "Sun"

    if x == "Partial Shade":
        return "Part Shade"
    
    if x == "Deep Shade":
        return "Shade"
    
    else:
        return np.nan
     
         


data["Sun Exposure"] = data["Light"].apply(clean_exposure)
data.drop(["Dimensions","Flower Value To Gardener","Light"],axis=1,inplace=True)
data.to_csv(OUTPUT_DIRECTORY + f"/{NURSERY}_{STATE}.csv",encoding='utf-8')


