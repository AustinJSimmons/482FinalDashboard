import pandas as pd
import os

files = [
    "482 Project Data Recording - Armughan.csv",
    "482 Project Data Recording - Austin.csv",
    "482 Project Data Recording - Jack.csv",
    "482 Project Data Recording - Kirthik.csv"
]

all_data = []

for file in files:
    basename = os.path.splitext(file)[0]
    name = basename.split(" - ")[-1].strip()

    df = pd.read_csv(file)
    df['Name'] = name
    all_data.append(df)

combined_df = pd.concat(all_data, ignore_index=True)

final_df = combined_df[['Name', 'Date', 'Time of Day', 'Focus', 'Mood', 'Heart Rate']]

final_df = final_df.dropna(subset=['Focus', 'Mood', 'Heart Rate'], how='all')

final_df['Focus'] = final_df['Focus'].round().astype('Int64')
final_df['Heart Rate'] = final_df['Heart Rate'].round().astype('Int64')

final_df.to_csv('hr_focus_mood.csv', index=False)

