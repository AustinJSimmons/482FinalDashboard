---
theme: dashboard
title: Mood-Focus Visualization 
toc: false
---


```js
const raw = await FileAttachment("data/hr_focus_mood.csv").csv({typed: true});

const moodOrder = ["Very Bad", "Bad", "Neutral", "Good", "Very Good"];

const data = raw.map(d => {
  const moodIndex = moodOrder.indexOf(d.Mood);   // 0–4
  const moodScore10 = (moodIndex + 1) * 2;       // 2,4,6,8,10

  return {
    ...d,
    moodScore: moodScore10,
    moodFocusEffect: d.Focus - moodScore10,
    mainActivity: (d.Activity || "").split(",")[0].trim()
  };
});


```
```js
const allActivities = [...new Set(data.map(d => d.mainActivity))].sort();
const activityOptions = ["(All Activities)", ...allActivities];

const allNames = [...new Set(data.map(d => d.Name))].sort();
const nameOptions = ["(All People)", ...allNames];

const allTimes = [...new Set(data.map(d => d["Time of Day"]))].sort();
const timeOptions = ["(All Times)", ...allTimes];

const activityInput = Inputs.select(activityOptions, {label: "Activity", value: "(All Activities)"});
const nameInput = Inputs.select(nameOptions, {label: "Person", value: "(All People)"});
const timeInput = Inputs.select(timeOptions, {label: "Time of Day", value: "(All Times)"});

const selectedActivity = Generators.input(activityInput);
const selectedName = Generators.input(nameInput);
const selectedTime = Generators.input(timeInput);


```
```js
// Filter raw rows based on controls
const filteredData = data.filter(d =>
  (selectedActivity === "(All Activities)" || d.mainActivity === selectedActivity) &&
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
  label: "Mood–Focus Effect (Focus − Mood Score)",
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
<div class='dashboard'>
  <div class='card'>
    ${activityInput}
    ${nameInput}
    ${timeInput}
  </div>

  <div class='card'>
    <b>Showing:</b> ${groupedData.length} averaged entries
  </div>

  <div class='card grid-colspan-2'>
    ${resize(width => moodEffectChart(groupedData, {width}))}
  </div>
</div>





