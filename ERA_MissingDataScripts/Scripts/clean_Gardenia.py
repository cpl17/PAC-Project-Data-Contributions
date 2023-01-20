import pandas as pd


STATE = "PA"
NURSERY = "Gardenia"
WEBDATA_SOURCE_DIRECTORY = r"C:\Users\CPL17\OneDrive\Documents\Code\Dev Projects\Current\PAC_New\ERA_MissingDataScripts\Output\AllScrapedData_Original"
OUTPUT_DIRECTORY = r"C:\Users\CPL17\OneDrive\Documents\Code\Dev Projects\Current\PAC_New\ERA_MissingDataScripts\Output\AllScrapedData_Cleaned"
FORMAT_OR_UNEDITED = "Formatted"


data = pd.read_csv(WEBDATA_SOURCE_DIRECTORY + f"/{NURSERY}_{STATE}_{FORMAT_OR_UNEDITED}.csv",index_col=0)
relevant_columns = ["Exposure","Height","Characteristics"]
data= data[relevant_columns]


# Clean Height
def determine_height(x):
  
    if isinstance(x,float):
        return x 


    x = x.split(" (")[0].replace("'","") 
    
    if '"' in x:
        #Range list looks like ['6"', "1'"]
        range_list = x.split(" to ")
        bottom,top = range_list[0],range_list[1]
        
        if '"' in bottom:
            range_list[0] = str(round(int(range_list[0].replace('"','')) / 12,1))
        if '"' in top:
            range_list[1] = str(round(int(range_list[1].replace('"','')) / 12,1)) 

        return "–".join(range_list)
    
    else:

        return x.replace(" to ","–")

data["Height (feet)"] = data.Height.apply(determine_height)

#Clean Showy
def is_showy(x):
    if isinstance(x,float):
        return x
    else:
        return "Yes" if "Showy" in x else "No"

data["Showy"] = data.Characteristics.apply(is_showy)

#Clean Exposure
def clean_exposure(cell_value):
    if isinstance(cell_value,float):
        return cell_value

    x = cell_value.split(",")
    for i,val in enumerate(x):
        if val == " Partial Sun":
            x[i] = " Partial Shade"
    return ",".join(x)       

data["Sun Exposure"] = data["Exposure"].apply(clean_exposure)


data.drop(["Exposure","Height","Characteristics"],axis=1,inplace=True)
data.to_csv(OUTPUT_DIRECTORY + f"/{NURSERY}_{STATE}.csv",encoding='utf-8')


