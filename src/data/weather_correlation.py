import pandas as pd
import os

files = [
    "482 Project Data Recording - Armughan.csv",
    "482 Project Data Recording - Austin.csv",
    "482 Project Data Recording - Jack.csv",
    "482 Project Data Recording - Kirthik.csv",
    "482 Project Data Recording - Yousri.csv"
]

all_data = []

for file in files:
    name = os.path.splitext(file)[0].split(" - ")[-1]
    df = pd.read_csv(file)
    df["Name"] = name
    all_data.append(df)

df = pd.concat(all_data, ignore_index=True)[["Name","Date","Focus","Mood","Weather"]].dropna()
df["Focus"] = df["Focus"].round().astype("Int64")
df["Mood_Normalized"] = df["Mood"].map({"Very Bad":1,"Bad":2,"Neutral":3,"Good":4,"Very Good":5})

weather_corr = (
    df.groupby("Weather")[["Mood_Normalized","Focus"]]
      .corr().unstack().iloc[:,1]
      .round(2)
      .reset_index(name="Correlation")
)

weather_corr.to_csv("weather_corr.csv", index=False)
df.to_csv("mood_focus_weather.csv", index=False)
