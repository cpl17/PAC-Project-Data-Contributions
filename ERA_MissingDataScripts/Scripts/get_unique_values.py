# # Imports and Data
import pandas as pd
import os

os.mkdir(r"C:\Users\CPL17\OneDrive\Documents\Code\Dev Projects\Current\PAC_New\ERA_MissingDataScripts\Temp")

STATE = "PA"
ERA_SOURCE_DATA_DIRECTORY = r"C:\Users\CPL17\OneDrive\Documents\Code\Dev Projects\Current\PAC_New\Data"
WEBDATA_SOURCE_DIRECTORY = r"C:\Users\CPL17\OneDrive\Documents\Code\Dev Projects\Current\PAC_New\ERA_MissingDataScripts\Output\AllScrapedData_Original"
OUTPUT_DIRECTORY = r"C:\Users\CPL17\OneDrive\Documents\Code\Dev Projects\Current\PAC_New\ERA_MissingDataScripts\Temp"
NURSERY_NAME = "Gardenia"
FORMATTED_UNEDITED = "Formatted"
RELEVANT_COLUMNS = ["Exposure","Height","Characteristics"]

os.mkdir(OUTPUT_DIRECTORY)
source_data = pd.read_excel(ERA_SOURCE_DATA_DIRECTORY + f"/ERA_{STATE}.xlsx",sheet_name="All Plants")


# # Summaries
data = pd.read_csv(WEBDATA_SOURCE_DIRECTORY + f"/{NURSERY_NAME}_{STATE}_{FORMATTED_UNEDITED}.csv",index_col=0)


full_df = None

for col in data:
    df = data[col].value_counts().reset_index()
    df.columns = [df.columns[1],"Count"]
    if full_df is not None:
        full_df = pd.concat([full_df,df],axis=1)
    else:
        full_df = df

full_df.to_csv(OUTPUT_DIRECTORY + f"/{NURSERY_NAME}_{STATE}_UniqueValues_All.csv",index=False)


def get_unique_values(df, column_name):
    unique_values = []
    for cell_value in df[column_name]:
        if isinstance(cell_value,float):
            continue   
        values = ",".join(str(cell_value).split("|")).split(",")
        for value in values:
            if value not in unique_values:
                unique_values.append(value)
    return unique_values


_ = {}
for col in data[RELEVANT_COLUMNS]:
    _[col] = get_unique_values(data,col)

max_length = 0
for key in _:
    if len(_[key]) > max_length:
        max_length = len(_[key])

for key in _:
    number_of_pads = max_length - len(_[key])
    _[key] += [""]*number_of_pads

df = pd.DataFrame(_)
for col in df:
    df[col] = df[col].apply(lambda x: x.strip().title() if not isinstance(x,float) else x).drop_duplicates()

df.to_csv(OUTPUT_DIRECTORY + f"/{NURSERY_NAME}_{STATE}_UniqueUniqueValues.csv",index=False)
