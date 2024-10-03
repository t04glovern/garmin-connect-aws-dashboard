---
title: Garmin Data
---

<Details title='How to edit this page'>

  This page can be found in your project at `/pages/index.md`. Make a change to the markdown file and save it to see the change take effect in your browser.
</Details>

<DateRange
    name=date_range
    defaultValue={'Last 30 Days'}
/>

```sql daily_sleep
select
    daily_sleep_calendar_date,
    daily_sleep_avg_stress,
    daily_sleep_time_seconds / 60 / 60 as daily_sleep_time_hours,
    daily_sleep_nap_time_seconds / 60 / 60 as daily_sleep_nap_hours,
    daily_sleep_deep_seconds / 60 / 60 as daily_sleep_deep_hours,
    daily_sleep_light_seconds / 60 / 60 as daily_sleep_light_hours,
    daily_sleep_rem_seconds / 60 / 60 as daily_sleep_rem_hours,
    daily_sleep_awake_seconds / 60 / 60 as daily_sleep_awake_hours,
    daily_sleep_avg_spo2_value,
    daily_sleep_lowest_spo2_value,
    daily_sleep_highest_spo2_value
from garmin.garmin_sleep_view
where daily_sleep_calendar_date between '${inputs.date_range.start}' and '${inputs.date_range.end}'
```

<CalendarHeatmap
  title="Average Sleep Stress by Date"
  data={daily_sleep}
  date=daily_sleep_calendar_date
  value=daily_sleep_avg_stress
/>

<LineChart 
  title="Sleep Type by Date"
  subtitle="Most adults need around 1.5-2 hours of deep sleep per night."
  data={daily_sleep}
  date=daily_sleep_calendar_date
  y={[
    'daily_sleep_deep_hours',
    'daily_sleep_light_hours',
    'daily_sleep_rem_hours',
    'daily_sleep_awake_hours'
    ]}
  step=true
/>

<BarChart
  title="Sleep Time by Date (Hours)"
  subtitle="The recommended amount of sleep for adults is 7-9 hours per night."
  data={daily_sleep}
  x=daily_sleep_calendar_date
  y=daily_sleep_time_hours
/>

<LineChart
  title="SpO₂ Value by Date"
  subtitle="Ideally, the SpO₂ value should be between 95% and 100%. Numbers below 90% are considered low."
  data={daily_sleep}
  x=daily_sleep_calendar_date
  y={[
    'daily_sleep_avg_spo2_value',
    'daily_sleep_lowest_spo2_value',
    'daily_sleep_highest_spo2_value'
  ]}
  step=true
/>