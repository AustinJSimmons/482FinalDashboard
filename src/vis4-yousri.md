---
theme: dashboard
title: Mood–Focus Relationship by Activity
toc: false
---

# Mood–Focus Relationship by Activity

This visualization explores **Question 4** from our project:  
> Do certain types of activities strengthen or weaken the relationship between mood and focus?



```js
// Load the combined CSV
const data = await FileAttachment("data/full_dataset.csv").csv({typed: true});

// Map mood categories to an ordered numeric scale (1–5)
const moodOrder = ["Very Bad", "Bad", "Neutral", "Good", "Very Good"];

// Add moodScore and mainActivity to each data point
const processedData = data.map(d => ({
  ...d,
  moodScore: moodOrder.indexOf(d.Mood) + 1,
  mainActivity: d.Activity ? d.Activity.split(',')[0].trim() : 'Unknown'
}));

// Dynamically get all unique activities from the data
const allActivities = Array.from(
  new Set(processedData.map(d => d.mainActivity))
).sort();
```

```js
// Create checkbox input for activities
const selectedActivities = view(
  Inputs.checkbox(allActivities, {
    label: "Select activities to compare (choose 2-5 for best readability)",
    value: allActivities.slice(0, 4) 
  })
);
```

```js
const showPoints = view(
  Inputs.toggle({
    label: "Show individual data points",
    value: true
  })
);
```

```js
const colorByPerson = view(
  Inputs.toggle({
    label: "Color by Person (instead of Activity)",
    value: false
  })
);
```

```js
// Filter data based on selected activities
const filtered = processedData.filter(d => 
  selectedActivities.includes(d.mainActivity)
);

// Add jitter for better visibility
const filteredWithJitter = filtered.map(d => ({
  ...d,
  moodScoreJittered: d.moodScore + (Math.random() - 0.5) * 0.15
}));
```

```js
// Render scatterplot with regression lines
Plot.plot({
  height: 500,
  marginLeft: 60,
  marginRight: 150,
  grid: true,
  x: {
    label: "Mood (Very Bad → Very Good)",
    domain: [1, 5],
    tickFormat: d => moodOrder[d - 1] || ""
  },
  y: {
    label: "Focus (0–10)",
    domain: [0, 10]
  },
  color: {
    legend: true,
    type: "categorical",
    scheme: "tableau10",
    label: colorByPerson ? "Person" : "Activity"
  },
  marks: [
    // Regression lines for each activity 
    !colorByPerson ? Plot.linearRegressionY(filtered, {
      x: "moodScore",
      y: "Focus",
      stroke: "mainActivity",
      strokeWidth: 3
    }) : null,
    
    // Individual data points 
    showPoints ? Plot.dot(filteredWithJitter, {
      x: "moodScoreJittered",
      y: "Focus",
      fill: colorByPerson ? "Name" : "mainActivity",
      r: 3.5,
      fillOpacity: 0.5,
      stroke: "white",
      strokeWidth: 0.5,
      tip: {
        format: {
          x: false,
          y: true,
          fill: true,
          Mood: true,
          Focus: true,
          Name: true
        }
      }
    }) : null
  ].filter(d => d !== null)
})
```