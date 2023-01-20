
# # Imports and Data

import pandas as pd

STATE = "PA"
ERA_SOURCE_DIRECTORY = r"C:\Users\CPL17\OneDrive\Documents\Code\Dev Projects\Current\PAC_New\Data"
NURSERY = "Gardenia"
WEBDATA_SOURCE_DIRECTORY = r"C:\Users\CPL17\OneDrive\Documents\Code\Dev Projects\Current\PAC_New\ERA_MissingDataScripts\Output\AllScrapedData_Original"
OUTPUT_DIRECTORY = r"C:\Users\CPL17\OneDrive\Documents\Code\Dev Projects\Current\PAC_New\ERA_MissingDataScripts\Output\AllScrapedData_Cleaned"
FORMAT_OR_UNEDITED = "Formatted"


source_data = pd.read_excel(ERA_SOURCE_DIRECTORY + f"\ERA_{STATE}.xlsx",sheet_name="All Plants")
data = pd.read_csv(WEBDATA_SOURCE_DIRECTORY + f"/{NURSERY}_{STATE}_{FORMAT_OR_UNEDITED}.csv",index_col=0)
relevant_columns = ["Height, Mature (feet)","Flower Color"]
data= data[relevant_columns]



# # Cleaning


# ## Height -> Height (feet)


def determine_height(cell_value):
    if isinstance(cell_value,float):
        return cell_value

    if ((".0" in cell_value) | ("0.0" in cell_value)):
        return str(int(float(cell_value)))
    
    else:
        return cell_value
    



data["Height (feet)"] = data["Height, Mature (feet)"].astype("str").apply(determine_height)
data["Height (feet)"] = data["Height (feet)"].astype(str)


# Note: Flower Color and Height are formatted correctly

data = data.reset_index()
data.drop("Height, Mature (feet)",axis=1,inplace=True)
data.columns = ["USDA Symbol","Flower Color","Height (feet)"]

source_to_join = source_data[["USDA Symbol","Scientific Name"]]

data = data.merge(source_to_join,on="USDA Symbol")
data.drop("USDA Symbol",axis=1,inplace=True)
data.set_index("Scientific Name",inplace=True)


data.to_csv("../Output/FinalCleanWebDataCSVs/USDAPlants.csv")


