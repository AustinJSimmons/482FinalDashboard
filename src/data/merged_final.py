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

    # Add a uniform lowercase name column
    df['name'] = name

    all_data.append(df)

combined_df = pd.concat(all_data, ignore_index=True)

# --- Clean & normalize --- #
combined_df.columns = (
    combined_df.columns
    .str.strip()
    .str.lower()
    .str.replace(" ", "_")
    .str.replace("-", "_")
)

# --- FIX COLUMN NAME VARIATIONS --- #
# Some files may use "time_since_last_meal" or similar
rename_map = {
    "time_since_last_meal": "time_since_meal",
    "time_since_meal_(minutes)": "time_since_meal",
    "time_since_meal_minutes": "time_since_meal"
}

combined_df = combined_df.rename(columns=rename_map)

# --- Make sure required columns exist --- #
required = ["name", "date", "time_of_day", "focus", "mood", "time_since_meal"]

missing_cols = [c for c in required if c not in combined_df.columns]
if missing_cols:
    raise ValueError(f"Missing columns: {missing_cols}")

final_df = combined_df[required]

# Drop rows where mood and focus are missing
final_df = final_df.dropna(subset=["focus", "mood"], how="all")

# Convert numeric columns
final_df['focus'] = pd.to_numeric(final_df['focus'], errors='coerce')
final_df['time_since_meal'] = pd.to_numeric(final_df['time_since_meal'], errors='coerce')

# Convert to strings for Observable
final_df['mood'] = final_df['mood'].astype(str)
final_df['time_of_day'] = final_df['time_of_day'].astype(str)

# Save final dataset
final_df.to_csv("src/data/FinalCode.csv", index=False)

print("FinalCode.csv created successfully!")
