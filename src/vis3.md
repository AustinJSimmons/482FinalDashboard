---
title: Visualization
toc: false
---

```js
// Load data
const data = await FileAttachment("data/FinalCode_cleaned.csv").csv({ typed: true });
```
## Controls

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

const person = view(
  Inputs.select(["All Participants", ...new Set(data.map(d => d.name))], {
    label: "Select Participant",
    value: "All Participants"
  })
);


```

## Visualization — Mood vs Focus

```js
const metricColumn = metric === "Mood" ? "mood" : "focus";

const filtered =
  person === "All Participants"
    ? data
    : data.filter(d => d.name === person);

if (filtered.length === 0) {
  html`<p style="color:red; font-size:18px;">No data available for ${person}</p>`;
} else {
  Plot.plot({
    title: `Time Since Meal vs ${metric} — ${person}`,
    subtitle: "Relationship between hunger and mood/focus",
    height: 520,
    width: 900,
    grid: true,

    x: {
      label: metric,
      domain: metric === "Mood"
        ? ["Very_Bad", "Bad", "Neutral", "Good", "Very_Good"]
        : undefined
    },

    y: {
      label: "Time Since Meal (minutes)",
      nice: true
    },

    color: {
      legend: true,
      label: "Participants"
    },

    marks: [
      // Trend line
      Plot.linearRegressionY(filtered, {
        x: metricColumn,
        y: "time_since_meal",
        stroke: "orange",
        strokeWidth: 3,
        opacity: 0.8
      }),

      // Box shading
      Plot.boxY(filtered, {
        x: metricColumn,
        y: "time_since_meal",
        fillOpacity: 0.15,
        stroke: "gray"
      }),

      // Scatter points
      Plot.dot(filtered, {
        x: metricColumn,
        y: "time_since_meal",
        fill: colorByPerson ? "name" : "black",
        r: 6,
        opacity: 0.8,
        tip: true,
        mixBlendMode: "multiply"
      })
    ]
  })
}

```

