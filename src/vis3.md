---
title: Eating-Focus/Mood Visualization
toc: false
---

```js
const raw = await FileAttachment("data/FinalCode_cleaned.csv").csv({ typed: true });

// Convert time_since_meal into HOURS (optional)
const data = raw.map(d => ({
  ...d,
  time_since_meal_hours: d.time_since_meal / 60
}));

// Inputs
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

const person = view(
  Inputs.select(["All Participants", ...new Set(data.map(d => d.name))], {
    label: "Select Participant",
    value: "All Participants"
  })
);

```

## Visualization — Mood vs Focus now

```js
// Filter dataset if a single participant is selected
const filtered = person === "All Participants"
  ? data
  : data.filter(d => d.name === person);
```  
```js  
const xColumn = metric === "Mood" ? "mood" : "focus";

// Specify ordering for Mood axis
const moodOrder = ["Very Bad", "Bad", "Neutral", "Good", "Very Good"];
```
<div style="margin-bottom:10px;">
  <span style="color:gold; font-weight:bold; font-size:14px;">■ Median (Gold)</span>
  &nbsp;&nbsp;&nbsp;
  <span style="color:white; font-weight:bold; font-size:14px;">■ Mean (White)</span>
</div>


```js            

Plot.plot({
  title: `How Time Since Meal Influences ${metric} Across the Day — ${person}`,
  subtitle: "Comparison of hunger effects by time of day, with median (gold) and mean (white) lines for clarity",
  height: 700,
  width: 1000,
  grid: true,

  facet: {
    data: filtered,
    x: "time_of_day",
    label: "Time of Day"
  },

  x: {
    label: metric,
    padding: 0.4,
    domain: metric === "Mood" 
      ? ["Very Bad", "Bad", "Neutral", "Good", "Very Good"]
      : undefined
  },

  y: {
    label: "Time Since Meal (hours)",
    nice: true
  },

  color: { legend: true },

  marks: [
  // Scatter points
  Plot.dot(filtered, {
    facet: "include",
    x: xColumn,
    y: "time_since_meal_hours",
    fill: colorByPerson ? "name" : "steelblue",
    r: 5,
    opacity: 0.8,
    tip: true,
    dx: () => (Math.random() - 0.5) * 20
  }),

  // ⭐ MEDIAN LINE
  Plot.ruleY(
    filtered,
    Plot.groupX(
      { y: "median" },
      {
        facet: "include",
        x: xColumn,
        y: "time_since_meal_hours",
        stroke: "gold",
        strokeWidth: 3,
        strokeOpacity: 0.9
      }
    )
  ),

  // OPTIONAL: ⭐ MEAN LINE
  Plot.ruleY(
    filtered,
    Plot.groupX(
      { y: "mean" },
      {
        facet: "include",
        x: xColumn,
        y: "time_since_meal_hours",
        stroke: "white",
        strokeWidth: 2.5,
        strokeOpacity: 0.9
      }
    )
  )
]
})


```

