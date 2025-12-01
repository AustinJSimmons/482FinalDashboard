---
theme: dashboard
title: Weather Correlation Visualization
toc: false
---

```js
const weatherData = await FileAttachment("data/weather_corr.csv").csv({
  typed: true,
});

weatherData.sort((a, b) => a.Correlation - b.Correlation);

display(
  Plot.plot({
    title: "Impact of Weather on Mood-Focus",
    marginLeft: 110,
    x: { label: "Correlation (r)", domain: [0, 1], grid: true },
    y: { label: null },
    color: { scheme: "ylorrd", legend: true, label: "Strength" },
    caption:
      "This chart displays the Pearson correlation (r) between Mood and Focus, categorized by weather type. Higher values (near 1.00) indicate a strong link where focus mirrors mood; lower values (near 0.00) indicate that mood and focus are decoupled.",
    marks: [
      Plot.ruleY(weatherData, {
        x1: 0,
        x2: "Correlation",
        y: "Weather",
        stroke: "gray",
        strokeWidth: 2,
      }),
      Plot.dot(weatherData, {
        x: "Correlation",
        y: "Weather",
        fill: "Correlation",
        r: 8,
        tip: true,
      }),
    ],
  })
);
```
