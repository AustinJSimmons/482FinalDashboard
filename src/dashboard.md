---
theme: dashboard
title: Interactive Dashboard
toc: false
---

<!-- JS  -->
```js
const data = await FileAttachment("data/hr_focus_mood.csv").csv({typed: true});

// Create Inputs for interaction with HR visualization
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
            metric === "Focus"
                ? Plot.linearRegressionY(data, {x: metric, y: "Heart Rate", stroke: "red"})
                : Plot.ruleY(data, Plot.groupZ({y: "mean"}, {y: "Heart Rate", stroke: "red", strokeOpacity: 0.5})),
            
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

const weatherData = await FileAttachment("data/weather_corr.csv").csv({
  typed: true,
});

weatherData.sort((a, b) => a.Correlation - b.Correlation);

function weatherImpactChart(weatherData, {width}) {
  return Plot.plot({
    width,
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
}
```
<!-- HTML -->
<div class='dashboard'>
    <h1>Interactive Dashboard</h1>
    <div class='grid grid-cols-4'>
        <div class='grid grid-colspan-3' style='margin: 0;'>
            <div class='grid grid-cols-2' style='margin: 0;'>
                <div class='card'>
                    ${resize((width) => heartRateChart(data, 
                    {width, metric: metricValue, colorByPerson: colorValue}))}
                </div>
                <div class='card'>
                    ${resize((width) => weatherImpactChart(weatherData, {width}))}
                </div>
                <div class='card'>
                </div>
                <div class='card'>
                </div>
                <div class='card grid-colspan-2 control-panel'></div>
            </div>
        </div>
        <div class='card grid-colspan-1'>
            <h2>Control Panel</h2>
            <div class='card'>
                <h3>Heart Rate Chart</h3>
                ${metricInput}
                ${colorInput}
            </div>
            <div class='card'>
                <h3>Filler</h3>
            </div>
            <div class='card'>
                <h3>Filler</h3>
            </div>
            <div class='card'>
                <h3>Filler</h3>
            </div>
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
    font-size: 75px;
  }
}
</style>