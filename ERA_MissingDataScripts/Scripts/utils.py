def is_showy(x):
    if isinstance(x,float):
        return x
    else:
        return "Yes" if "Showy" in x else "No"

def determine_height(x):
  
    if isinstance(x,float):
        return x 


    x = x.split(" (")[0] 
    if '"' in x:
        range_list = x.split(" to ")
        bottom,top = range_list[0],range_list[1]
        
        if '"' in bottom:
            range_list[0] = str(round(int(range_list[0].replace('"','')) / 12,1))
        if '"' in top:
            range_list[1] = str(round(int(range_list[1].replace('"','')) / 12,1)) 

        return "–".join(range_list).replace("'","")
    
    else:

        return x.replace(" to ","–").replace("'","")


def determine_height_2(cell_value):
    x = cell_value.split("to")
    f = lambda y: str(round(float(y.strip()),1)) if "." in y else y.strip()
    x = list(map(f,x))
    return "–".join(x)


def get_unique_values(df, column_name):
    unique_values = []
    for cell_value in df[column_name]:
        if isinstance(cell_value,float):
            continue

        #TODO: make values a triple split using ;,| so it can be reused
        if column_name == "Pollinators":
            values = str(cell_value).split(";")
        else:
            values = str(cell_value).split(",")
        for value in values:
            if value not in unique_values:
                unique_values.append(value)
    return unique_values