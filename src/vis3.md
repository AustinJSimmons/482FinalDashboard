---
theme: dashboard
title:  Visualization 
toc: false
---

```js
import { FileAttachment } from "@observablehq/stdlib";
import * as Plot from "@observablehq/plot";

// Load your cleaned merged dataset
const data = FileAttachment("data/FinalCode.csv").csv({ typed: true });
```


```js
const metric = view(
  Inputs.radio(["Mood", "Focus"], {
    label: "Compare Time Since Meal with:",
    value: "Mood"
  })
);

const colorByPerson = view(
  Inputs.toggle({
    label: "Color by Person",
    value: true
  })
);
```

## Visualization — Mood vs Focus

```js
Plot.plot({
  title: `Time Since Meal vs. ${metric}`,
  subtitle: "Distribution of time-since-meal across different states",
  height: 520,
  marginLeft: 60,
  grid: true,

  y: {
    label: "Time Since Meal (hours)",
    domain: [0, d3.max(data, d => d.time_since_meal)]
  },

  x: {
    label: metric,
    // If metric = Mood, order the categories nicely
    ...(metric === "Mood"
      ? {
          domain: ["Very Bad", "Bad", "Neutral", "Good", "Very Good"]
        }
      : {})
  },

  color: {
    legend: true
  },

  marks: [
    // Mean time since meal line
    Plot.ruleY(
      data,
      Plot.groupZ({ y: "mean" }, { y: "time_since_meal", stroke: "red", strokeOpacity: 0.5 })
    ),

    // Dots
    Plot.dot(data, {
      x: metric,
      y: "time_since_meal",
      fill: colorByPerson ? "name" : "steelblue",
      tip: true,
      mixBlendMode: "multiply",
      r: 5
    }),

    // Boxplot for distribution clarity
    Plot.boxY(data, {
      x: metric,
      y: "time_since_meal",
      fillOpacity: 0.2,
      strokeOpacity: 0.5
    })
  ]
})
```
