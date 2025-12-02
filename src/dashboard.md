---
theme: dashboard
title: Interactive Dashboard
toc: false
---

<!-- JS  -->

```js
const data = await FileAttachment("data/hr_focus_mood.csv").csv({
  typed: true,
});

// Create Inputs for interaction with HR visualization
const metricInput = Inputs.radio(["Mood", "Focus"], {
  label: "Compare Heart Rate with:",
  value: "Mood",
});

const pointInput = Inputs.toggle({ label: "Hide points", value: true });

const colorInput = Inputs.toggle({ label: "Color by Person", value: true });

const metricValue = Generators.input(metricInput);

const colorValue = Generators.input(colorInput);

const pointValue = Generators.input(pointInput);

function heartRateChart(data, { width, metric, colorByPerson, points }) {
  return Plot.plot({
    title: `Heart Rate vs. ${metric}`,
    subtitle: "Distribution of heart rate across different states",
    width,
    height: 800,
    marginLeft: 60,
    grid: true,
    y: {
      label: "Heart Rate (BPM)",
      domain: [40, 140],
    },
    x: {
      label: metric,
      // Filter/switch for mood and focus
      ...(metric === "Mood"
        ? { domain: ["Very Bad", "Bad", "Neutral", "Good", "Very Good"] }
        : {}),
    },
    color: {
      legend: true,
    },
    marks: [
      metric === "Focus"
        ? Plot.linearRegressionY(data, {
            x: metric,
            y: "Heart Rate",
            stroke: "red",
          })
        : Plot.ruleY(
            data,
            Plot.groupZ(
              { y: "mean" },
              { y: "Heart Rate", stroke: "red", strokeOpacity: 0.5 }
            )
          ),

      // The main data points
      points === true
        ? null
        : Plot.dot(data, {
            x: metric,
            y: "Heart Rate",
            fill: colorByPerson ? "Name" : "steelblue",
            tip: true,
            mixBlendMode: "screen", // Helps see density if points overlap
          }),

      // Add a boxplot on top to show the median/ranges clearly
      Plot.boxY(data, {
        x: metric,
        y: "Heart Rate",
        fillOpacity: 0.2,
        strokeOpacity: 0.5,
      }),
    ],
  });
}

const weatherData = await FileAttachment("data/weather_corr.csv").csv({
  typed: true,
});

weatherData.sort((a, b) => a.Correlation - b.Correlation);

function weatherImpactChart(weatherData, { width }) {
  return Plot.plot({
    width,
    height: 300,
    title: "Impact of Weather on Mood-Focus",
    marginLeft: 110,
    x: { label: "Correlation (r)", domain: [0, 1], grid: true },
    y: { label: null },
    color: { scheme: "ylorrd", legend: true, label: "Strength" },
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
  });
}
```

```js
const raw = await FileAttachment("data/FinalCode_cleaned.csv").csv({
  typed: true,
});

// Convert time_since_meal into HOURS (optional)
const data2 = raw.map((d) => ({
  ...d,
  time_since_meal_hours: d.time_since_meal / 60,
}));

const personInput = Inputs.select(
  ["All Participants", ...new Set(data2.map((d) => d.name))],
  {
    label: "Select Participant",
    value: "All Participants",
  }
);

const metricInput2 = Inputs.radio(["Mood", "Focus"], {
  label: "Compare Time Since Meal with:",
  value: "Mood",
});

const colorInput2 = Inputs.toggle({
  label: "Color by Person",
  value: true,
});

const personValue = Generators.input(personInput);
const metricValue2 = Generators.input(metricInput2);
const colorValue2 = Generators.input(colorInput2);
```

```js
const xColumn = metricValue2 === "Mood" ? "mood" : "focus";
```

```js
const filtered =
  personValue === "All Participants"
    ? data2
    : data2.filter((d) => d.name === personValue);
```

```js
function mealChart(filtered, { width, metric, colorByPerson, person }) {
  return Plot.plot({
    width,
    height: 300,
    title: `How Time Since Meal Influences ${metric} Across the Day — ${person}`,
    subtitle:
      "Comparison of hunger effects by time of day, with median (gold) and mean (white) lines for clarity",
    grid: true,
    facet: {
      data: filtered,
      x: "time_of_day",
      label: "Time of Day",
    },

    x: {
      label: metric,
      padding: 0.4,
      domain:
        metric === "Mood"
          ? ["Very Bad", "Bad", "Neutral", "Good", "Very Good"]
          : undefined,
    },

    y: {
      label: "Time Since Meal (hours)",
      nice: true,
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
        dx: () => (Math.random() - 0.5) * 20,
      }),
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
            strokeOpacity: 0.9,
          }
        )
      ),
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
            strokeOpacity: 0.9,
          }
        )
      ),
    ],
  });
}
```

```js
// Load the combined CSV
const data3 = await FileAttachment("data/full_dataset.csv").csv({
  typed: true,
});

// Map mood categories to an ordered numeric scale (1–5)
const moodOrder = ["Very Bad", "Bad", "Neutral", "Good", "Very Good"];

// Add moodScore and mainActivity to each data point
const processedData = data3.map((d) => ({
  ...d,
  moodScore: moodOrder.indexOf(d.Mood) + 1,
  mainActivity: d.Activity ? d.Activity.split(",")[0].trim() : "Unknown",
}));

// Dynamically get all unique activities from the data
const allActivities = Array.from(
  new Set(processedData.map((d) => d.mainActivity))
).sort();

const selectedActivitiesInput = Inputs.checkbox(allActivities, {
  label: "Select activities to compare (choose 2-5 for best readability)",
  value: allActivities.slice(0, 4),
});

const showPointsInput = Inputs.toggle({
  label: "Show individual data points",
  value: true,
});

const colorInput3 = Inputs.toggle({
  label: "Color by Person (instead of Activity)",
  value: false,
});

const showPointsValue = Generators.input(showPointsInput);
const selectedActivitesValue = Generators.input(selectedActivitiesInput);
const colorValue3 = Generators.input(colorInput3);
```

```js
// Filter data based on selected activities
const filtered2 = processedData.filter((d) =>
  selectedActivitesValue.includes(d.mainActivity)
);
```

```js
// Add jitter for better visibility
const filteredWithJitter = filtered2.map((d) => ({
  ...d,
  moodScoreJittered: d.moodScore + (Math.random() - 0.5) * 0.15,
}));
```

```js
function activityChart(
  filteredWithJitter,
  { width, selectedActivites, showPoints, colorByPerson, filtered }
) {
  return Plot.plot({
    width,
    height: 300,
    title: "Mood–Focus Relationship by Activity",
    grid: true,
    x: {
      label: "Mood (Very Bad → Very Good)",
      domain: [1, 5],
      tickFormat: (d) => moodOrder[d - 1] || "",
    },
    y: {
      label: "Focus (0–10)",
      domain: [0, 10],
    },
    color: {
      legend: true,
      type: "categorical",
      scheme: "tableau10",
      label: colorByPerson ? "Person" : "Activity",
    },
    marks: [
      // Regression lines for each activity
      !colorByPerson
        ? Plot.linearRegressionY(filtered, {
            x: "moodScore",
            y: "Focus",
            stroke: "mainActivity",
            strokeWidth: 3,
          })
        : null,

      // Individual data points
      showPoints
        ? Plot.dot(filteredWithJitter, {
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
                Name: true,
              },
            },
          })
        : null,
    ].filter((d) => d !== null),
  });
}
```

```js
const data4 = data.map((d) => {
  const moodIndex = moodOrder.indexOf(d.Mood); // 0–4
  const moodScore10 = (moodIndex + 1) * 2;      // 2–10 scale

  return {
    ...d,
    moodScore: moodScore10,
    moodFocusEffect: d.Focus - moodScore10,
    mainActivity: d.Activity.split(",")[0].trim(),
  };
});


const allActivities = Array.from(
  new Set(data4.map((d) => d.mainActivity))
).sort();
const activityOptions = ["(All Activities)", ...allActivities];

const allNames = Array.from(new Set(data4.map((d) => d.Name))).sort();
const nameOptions = ["(All People)", ...allNames];

const allTimes = Array.from(new Set(data4.map((d) => d["Time of Day"]))).sort();
const timeOptions = ["(All Times)", ...allTimes];

const activityInput = Inputs.select(activityOptions, {
  label: "Activity",
  value: "(All Activities)",
});

const nameInput = Inputs.select(nameOptions, {
  label: "Person",
  value: "(All People)",
});

const timeInput = Inputs.select(timeOptions, {
  label: "Time of Day",
  value: "(All Times)",
});

const colorInput4 = Inputs.toggle({
  label: "Colour by Person",
  value: false,
});

const selectedActivity = Generators.input(activityInput);
const selectedName = Generators.input(nameInput);
const selectedTime = Generators.input(timeInput);
const colorByPerson = Generators.input(colorInput4);
```

```js
const filteredData = data4.filter(
  (d) =>
    (selectedActivity === "(All Activities)" ||
      d.mainActivity === selectedActivity) &&
    (selectedName === "(All People)" || d.Name === selectedName) &&
    (selectedTime === "(All Times)" || d["Time of Day"] === selectedTime)
);
```
```js
const groupedData = (() => {
  const agg = new Map();

  for (const d of filteredData) {
    const time = d["Time of Day"];
    const activity = d.mainActivity;
    if (!time || !activity) continue;

    const key = `${time}|||${activity}`;
    const prev = agg.get(key);
    if (prev) {
      prev.sum += d.moodFocusEffect;
      prev.count += 1;
    } else {
      agg.set(key, {
        "Time of Day": time,
        mainActivity: activity,
        sum: d.moodFocusEffect,
        count: 1
      });
    }
  }

  return Array.from(agg.values()).map(d => ({
    "Time of Day": d["Time of Day"],
    mainActivity: d.mainActivity,
    moodFocusEffect: d.sum / d.count
  }));
})();


```

```js
function moodEffectChart(data, {width}) {
  return Plot.plot({
    title: "How Mood Affects Focus (Averaged)",
    subtitle: "Each dot = average mood-focus effect for that person/activity/time",
    width,
    height: 500,
    marginLeft: 60,
    marginBottom: 60,
    grid: true,
    x: { label: "Time of Day" },
y: {
  label: "Mood–Focus Effect (Focus − Mood Score [2–10])",
  domain: [-5, 5]
},
    color: { legend: true },
    marks: [
      Plot.dot(
        data.map(d => ({
          ...d,
          jitteredEffect: d.moodFocusEffect + (Math.random() - 0.5) * 0.15
        })),
        {
          x: "Time of Day",
          y: "jitteredEffect",
          fill: "mainActivity",
          r: 7,
          tip: true,
          stroke: "white",
          strokeWidth: 0.8
        }
      ),
      Plot.ruleY([0], {
        stroke: "black",
        strokeOpacity: 0.3,
        strokeDasharray: "4"
      })
    ]
  });
}

```

# Mood & Focus Analysis

<div class='card control-panel'>
    <h2>Control Panel</h2>
    <div class='grid grid-cols-4'>
        <div class='card'>
            <h3>Heart Rate Chart</h3>
            ${metricInput}
            ${colorInput}
            ${pointInput}
        </div>
        <div class='card'>
            <h3>Activites Chart</h3>
            ${selectedActivitiesInput}
            ${colorInput3}
            ${showPointsInput}
        </div>
        <div class='card'>
            <h3>Mood-Focus Effect Chart</h3>
            ${activityInput}
            ${nameInput}
            ${timeInput}
            ${colorInput}
        </div>
        <div class='card'>
            <h3>Time Last Meal Chart</h3>
            ${metricInput2}
            ${colorInput2}
            ${personInput}
        </div>
    </div>
</div>

<div style="display: grid; grid-template-columns: 1fr 1fr; gap: 1rem;">
  <div style="display: flex; flex-direction: column; gap: 1rem;">
    <div class='card'>
      ${resize((width) => heartRateChart(data, {width, metric: metricValue, colorByPerson: colorValue, points: pointValue}))}
    </div>
  </div>
  <div style="display: flex; flex-direction: column; gap: 1rem;">
    <div class='card'>
      ${resize((width) => weatherImpactChart(weatherData, {width}))}
    </div>
    <div class='card'>
      ${resize((width) => activityChart(filteredWithJitter, {width, selectedActivites: selectedActivitesValue, showPoints: showPointsValue, colorByPerson: colorValue3, filtered: filtered2}))}
    </div>
  </div>
</div>
<div class='card' style="margin-top: 1rem;">
  ${resize((width) => moodEffectChart(groupedData, {width}))}
</div>
<div class='card' style="margin-top: 1rem;">
  ${resize((width) => mealChart(filtered, {width, metric: metricValue2, colorByPerson: colorValue2, person: personValue}))}
</div>
