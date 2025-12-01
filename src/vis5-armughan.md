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
      "Correlation (r) represents the strength and direction of the relationship between weather conditions and mood-related focus. Values closer to 1.00 indicate a strong positive association, while values near 0.00 indicate little or no relationship.",
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
