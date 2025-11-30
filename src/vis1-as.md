---
theme: dashboard
title: HR-Focus-Mood Visualization 
toc: false
---

<!-- JS -->

```js
const data = await FileAttachment("data/hr_focus_mood.csv").csv({typed: true});

// Create Inputs for interaction
const metricInput = Inputs.radio(
  ["Mood", "Focus"], 
  {label: "Compare Heart Rate with:", value: "Mood"}
);

const colorInput = Inputs.toggle(
  {label: "Color by Person", value: true}
);

const metricValue = Generators.input(metricInput);
const colorValue = Generators.input(colorInput);

function heartRateChart(data, {width, metric, colorByPerson}) {
    return Plot.plot({
        width,
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
            mixBlendMode: "screen" // Helps see density if points overlap
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
}
```

<!-- HTML layout of page -->
<div class='dashboard'>
    <h1>HR-Focus-Mood Visualization</h1>
    <div class='card'>
            ${metricInput}
            ${colorInput}
    </div>
    <div class='grid grid-cols-2'>
        <div class='card grid-colspan-2'>
            ${resize((width) => heartRateChart(data, 
            {width, metric: metricValue, colorByPerson: colorValue}))}
        </div>
    </div>
</div>

<!-- Style/CSS -->
<style>
.dashboard {
  font-family: var(--sans-serif);
  text-wrap: balance;
  text-align: center;
  overflow: hidden;
}

.dashboard h1 {
  background: linear-gradient(30deg, var(--theme-foreground-focus), currentColor);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  max-width: none;
  font-weight: 900;
  line-height: 1;
}

.dashboard h2 {
  margin: 0;
  max-width: 34em;
  font-size: 20px;
  font-style: initial;
  font-weight: 500;
  line-height: 1.5;
  color: var(--theme-foreground-muted);
}

@media (min-width: 640px) {
  .dashboard h1 {
    font-size: 60px;
  }
}
</style>