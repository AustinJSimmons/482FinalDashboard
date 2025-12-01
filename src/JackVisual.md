---
theme: dashboard
title: vis
toc: false
---


```js
const raw = await FileAttachment("data/hr_focus_mood.csv").csv({typed: true});

const moodOrder = ["Very Bad", "Bad", "Neutral", "Good", "Very Good"];

const data = raw.map(d => ({
  ...d,
  moodScore: moodOrder.indexOf(d.Mood) + 1,
  moodFocusEffect: d.Focus - (moodOrder.indexOf(d.Mood) + 1),
  mainActivity: d.Activity.split(",")[0].trim()
}));

```
```js
const allActivities = Array.from(new Set(data.map(d => d.mainActivity))).sort();
const activityOptions = ["(All Activities)", ...allActivities];

const allNames = Array.from(new Set(data.map(d => d.Name))).sort();
const nameOptions = ["(All People)", ...allNames];

const allTimes = Array.from(new Set(data.map(d => d["Time of Day"]))).sort();
const timeOptions = ["(All Times)", ...allTimes];

const activityInput = Inputs.select(activityOptions, {
  label: "Activity",
  value: "(All Activities)"
});

const nameInput = Inputs.select(nameOptions, {
  label: "Person",
  value: "(All People)"
});

const timeInput = Inputs.select(timeOptions, {
  label: "Time of Day",
  value: "(All Times)"
});

const colorInput = Inputs.toggle({
  label: "Colour by Person",
  value: false
});

const selectedActivity = Generators.input(activityInput);
const selectedName = Generators.input(nameInput);
const selectedTime = Generators.input(timeInput);
const colorByPerson = Generators.input(colorInput);

```
```js
const filteredData = data.filter(d =>
  (selectedActivity === "(All Activities)" || d.mainActivity === selectedActivity) &&
  (selectedName === "(All People)" || d.Name === selectedName) &&
  (selectedTime === "(All Times)" || d["Time of Day"] === selectedTime)
);

```

```js
function moodEffectChart(filtered, {width, colorByPerson}) {
  return Plot.plot({
    title: "How Mood Affects Focus",
    subtitle: "Positive = Mood boosts focus; Negative = Mood drags it down",
    width,
    height: 500,
    marginLeft: 60,
    marginBottom: 60,
    grid: true,
    x: { label: "Time of Day" },
    y: {
      label: "Mood–Focus Effect (Focus − Mood Score)",
      domain: [-5, 5]
    },
    color: { legend: true },
    marks: [
      Plot.dot(
        filtered.map(d => ({
          ...d,
          jitteredEffect: d.moodFocusEffect + (Math.random() - 0.5) * 0.2
        })),
        {
          x: "Time of Day",
          y: "jitteredEffect",
          fill: colorByPerson ? "Name" : "mainActivity",
          r: 5,
          tip: true,
          stroke: "white",
          strokeWidth: 0.5
        }
      ),
      Plot.ruleY(
        filtered,
        Plot.groupZ({y: "mean"}, {
          y: "moodFocusEffect",
          stroke: "red",
          strokeOpacity: 0.5,
          strokeWidth: 2
        })
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
<div class='dashboard'>
  <div class='card'>
    ${activityInput}
    ${nameInput}
    ${timeInput}
    ${colorInput}
  </div>

  <div class='card'>
    <b>Showing:</b> ${filteredData.length} entries
  </div>

  <div class='card grid-colspan-2'>
    ${resize((width) =>
      moodEffectChart(filteredData, {
        width,
        colorByPerson
      })
    )}
  </div>
</div>




