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

const pointInput = Inputs.toggle(
  {label: "Hide points", value: true}
);

const colorInput = Inputs.toggle(
  {label: "Color by Person", value: true}
);

const metricValue = Generators.input(metricInput);

const colorValue = Generators.input(colorInput);

const pointValue = Generators.input(pointInput);

function heartRateChart(data, {width, metric, colorByPerson, points}) {
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
            // Add a rule at the average Heart Rate for mood
            // Lin reg for focus
            metric === "Focus"
                ? Plot.linearRegressionY(data, {x: metric, y: "Heart Rate", stroke: "red"})
                : Plot.ruleY(data, Plot.groupZ({y: "mean"}, {y: "Heart Rate", stroke: "red", strokeOpacity: 0.5})),
            
            // The main data points
            points === true ? null : Plot.dot(data, {
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
            ${pointInput}
    </div>
    <div class='grid grid-cols-2'>
        <div class='card grid-colspan-2'>
            ${resize((width) => heartRateChart(data, 
            {width, metric: metricValue, colorByPerson: colorValue, points: pointValue}))}
        </div>
    </div>
</div>

## Inpiration

The question we thought of in the beginning was "Does an individual’s physiological state (measured via heart rate) correlate with focus or mood, and are these correlations consistent across different activities?" and looking back HR measured once per period of day was a poor way to experiment with this. That being said, there is a positive correlation between heart rate and mood as shown in the figure above. As for Focus (1-10), the results were more varied. However after plotting a linear regression onto the focus chart we can see a slight positive correlation between heart rate and Focus.

As for the second part of the question, the figure below attempts to analyze the trends depending on activity.

```js
const data2 = await FileAttachment("data/hr_activity.csv").csv({typed: true});

const allActivities = [...new Set(data2.map(d => d.Activity))].sort();

const activityInput = Inputs.select(allActivities, {
  label: "Filter by Activity",
  multiple: false,
  sort: true,
  unique: true,
  value: allActivities[0] // Select all by default
});

const activitySelection = Generators.input(activityInput);

const moodOrder = ["Very Bad", "Bad", "Neutral", "Good", "Very Good"];

function focusHRChart(filteredData, {width}) {
    return Plot.plot({
        width,
        grid: true,
        x: { label: "Focus Level (1-10)", domain: [0, 11] },
        y: { label: "Heart Rate (BPM)", domain: [40, 140] },
        marks: [
            // Trend line to show correlation direction
            Plot.linearRegressionY(filteredData, {x: "Focus", y: "Heart Rate", stroke: "red", strokeOpacity: 0.7}),
            
            // Data points
            Plot.dot(filteredData, {
                x: "Focus", 
                y: "Heart Rate", 
                fill: "steelblue", 
                tip: true,
                mixBlendMode: "screen"
            })
        ]
    });
}

function moodHRChart(filteredData, {width}) {
    return Plot.plot({
        width,
        grid: true,
        x: { label: "Mood", domain: ["Very Bad", "Bad", "Neutral", "Good", "Very Good"] },
        y: { label: "Heart Rate (BPM)", domain: [40, 140] },
        marks: [
            Plot.boxY(filteredData, {
                x: "Mood", 
                y: "Heart Rate", 
                fillOpacity: 0.2
            }),
            Plot.dot(filteredData, {
                x: "Mood", 
                y: "Heart Rate", 
                fill: "steelblue", 
                r: 3,
                mixBlendMode: "screen",
                fillOpacity: 0.8,  // See density better
                tip: true
            })
        ]
    })
}
```

```js
const filteredData = data2.filter(d => d.Activity === activitySelection);

```

<div class='dashboard'>
    <h3>Heart Rate, Mood and Focus per Activity</h3>
    <div class='card'>
        ${activityInput}
    </div>
    <div class='grid grid-cols-2'>
        <div class='card grid-colspan-1'>
            ${resize((width) => focusHRChart(filteredData, {width}))}
        </div>
        <div class='card grid-colspan-1'>
            ${resize((width) => moodHRChart(filteredData, {width}))}
        </div>
    </div>
</div>




<!-- Style/CSS -->
<style>
.dashboard {
  font-family: var(--sans-serif);
  text-wrap: balance;
  text-align: center;
  align-items: center;
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