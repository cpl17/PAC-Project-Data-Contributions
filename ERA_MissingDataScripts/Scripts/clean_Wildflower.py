
# # Imports and Data
import pandas as pd


STATE = "PA"
ERA_SOURCE_DIRECTORY = r"C:\Users\CPL17\OneDrive\Documents\Code\Dev Projects\Current\PAC_New\Data"
NURSERY = "Wildflower"
WEBDATA_SOURCE_DIRECTORY = r"C:\Users\CPL17\OneDrive\Documents\Code\Dev Projects\Current\PAC_New\ERA_MissingDataScripts\Output\AllScrapedData_Original"
OUTPUT_DIRECTORY = r"C:\Users\CPL17\OneDrive\Documents\Code\Dev Projects\Current\PAC_New\ERA_MissingDataScripts\Output\AllScrapedData_Cleaned"
FORMAT_OR_UNEDITED = "Unedited"


source_data = pd.read_excel(ERA_SOURCE_DIRECTORY + f"\ERA_{STATE}.xlsx",sheet_name="All Plants")
data = pd.read_csv(WEBDATA_SOURCE_DIRECTORY + f"/{NURSERY}_{STATE}_{FORMAT_OR_UNEDITED}.csv",index_col=0)
relevant_columns = ["Bloom Time","Bloom Color", "Soil Moisture","Light Requirement","Size Class"]
data= data[relevant_columns]


# Height 

data["Height (feet)"] = data["Size Class"].apply(lambda x: x.split()[0].strip().replace(" ft.","").replace("-","–") if not isinstance(x,float) else x)

# ## Bloom Time -> Flowering Months


def det_bloom(cell_value):
    if isinstance(cell_value,float):
        return cell_value
    
    x = cell_value.split(",")

    if len(x) == 1:
        return x[0]
    else:
        return "–".join([x[0],x[-1]])


data["Flowering Months"] = data["Bloom Time"].apply(det_bloom)


# ## Bloom Color -> Flower Color


def det_color(cell_value):
    if isinstance(cell_value,float):
        return cell_value
    
    x = cell_value.split(",")

    if len(x) == 1:
        return x[0].strip()
    else:
        return "–".join(x[:2]).strip()


data["Flower Color"] = data["Bloom Color"].apply(det_color)


# ## Soil Moisture


data["Soil Moisture"] = data["Soil Moisture"].str.strip()


# ## Light Requirement


data.rename({"Light Requirement":"Sun Exposure"},axis=1,inplace=True)


# Lookup Scientific Name

data.drop(["Bloom Time","Bloom Color","Size Class"],axis=1,inplace=True)
cols = data.columns
data = data.reset_index()
data.columns = ["USDA Symbol"] + cols.to_list()

source_to_join = source_data[["USDA Symbol","Scientific Name"]]

data = data.merge(source_to_join,on="USDA Symbol")
data.drop("USDA Symbol",axis=1,inplace=True)
data.set_index("Scientific Name",inplace=True)



data.to_csv(OUTPUT_DIRECTORY + f"/{NURSERY}_{STATE}.csv",encoding='utf-8')


