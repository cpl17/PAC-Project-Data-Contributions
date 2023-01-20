import pandas as pd 

df = pd.read_excel(r"C:\Users\CPL17\OneDrive\Documents\Code\Dev Projects\Current\PAC_New\Data\CNP_PA_Full_10_27.xlsx",sheet_name="ERA_PA")
df = df[['Sun Exposure', 'Soil Moisture', 'Pollinators', 'Flowering Months','Height (feet)', 'Showy', 'Flower Color']]

print(df.isna().sum())