---
theme: dashboard
title: HR-Focus-Mood Visualization 
toc: false
---

<!-- Load data -->

```js
const data = await FileAttachment("data/hr_focus_mood.csv").csv({typed: true});

// Create Inputs for interaction
const metric = view(Inputs.radio(
  ["Mood", "Focus"], 
  {label: "Compare Heart Rate with:", value: "Mood"}
));

const colorByPerson = view(Inputs.toggle(
  {label: "Color by Person", value: true}
));
```

<!-- Create Chart -->

```js
Plot.plot({
  title: `Heart Rate vs. ${metric}`,
  subtitle: "Distribution of heart rate across different states",
  marginLeft: 60,
  grid: true,
  y: {
    label: "Heart Rate (BPM)",
    domain: [40, 140]
  },
  x: {
    label: metric,
    // Filter/switch for mood and focus
    ...(metric === "Mood" ? {domain: ["Very Bad", "Bad", "Neutral", "Good", "Very Good"]} : {})
  },
  color: {
    legend: true
  },
  marks: [
    // Add a rule at the average Heart Rate
    Plot.ruleY(data, Plot.groupZ({y: "mean"}, {y: "Heart Rate", stroke: "red", strokeOpacity: 0.5})),
    
    // The main data points
    Plot.dot(data, {
      x: metric,
      y: "Heart Rate",
      fill: colorByPerson ? "Name" : "steelblue",
      tip: true,
      mixBlendMode: "multiply" // Helps see density if points overlap
    }),
    
    // Add a boxplot on top to show the median/ranges clearly
    Plot.boxY(data, {
      x: metric,
      y: "Heart Rate",
      fillOpacity: 0.2,
      strokeOpacity: 0.5
    })
  ]
})
```

<!-- HTML layout of page -->