import pandas as pd
import os

files = [
    "src/data/482 Project Data Recording - Armughan.csv",
    "src/data/482 Project Data Recording - Austin Simmons.csv",
    "src/data/482 Project Data Recording - Jack.csv",
    "src/data/482 Project Data Recording - Kirthik.csv",
    "src/data/482 Project Data Recording - Yousri.csv"
]

all_data = []

for file in files:
    basename = os.path.splitext(file)[0]
    name = basename.split(" - ")[-1].strip()

    df = pd.read_csv(file)
    df['Name'] = name
    all_data.append(df)

combined_df = pd.concat(all_data, ignore_index=True)

# Clean & normalize column names
combined_df.columns = (
    combined_df.columns
    .str.strip()
    .str.replace(" ", "_")
    .str.replace("-", "_")
    .str.replace("__", "_")
    .str.lower()
)

# Select only relevant columns (matching cleaned names)
final_df = combined_df[['name', 'date', 'time_of_day', 'focus', 'mood', 'time_since_meal']]

# Drop empty rows
final_df = final_df.dropna(subset=['focus', 'mood'], how='all')

# Convert datatypes
final_df['focus'] = pd.to_numeric(final_df['focus'], errors='coerce')
final_df['time_since_meal'] = pd.to_numeric(final_df['time_since_meal'], errors='coerce')
final_df['mood'] = final_df['mood'].astype(str)
final_df['time_of_day'] = final_df['time_of_day'].astype(str)

# Save inside your Observable data folder
final_df.to_csv("src/data/FinalCode.csv", index=False)
