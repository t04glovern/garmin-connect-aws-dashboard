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

```sql daily_sleep_avg_stress
select
    daily_sleep_calendar_date,
    daily_sleep_avg_stress,
    daily_sleep_light_seconds / 60 / 60 as daily_sleep_light_hours,
    daily_sleep_rem_seconds / 60 / 60 as daily_sleep_rem_hours,
    daily_sleep_awake_seconds / 60 / 60 as daily_sleep_awake_hours,
from garmin.garmin_sleep_view
where daily_sleep_calendar_date between '${inputs.date_range.start}' and '${inputs.date_range.end}'
```

<CalendarHeatmap
  title="Average Sleep Stress by Date"
  data={daily_sleep_avg_stress}
  date=daily_sleep_calendar_date
  value=daily_sleep_avg_stress
/>

<LineChart 
  title="Sleep Type by Date"
  data={daily_sleep_avg_stress}
  date=daily_sleep_calendar_date
  y={['daily_sleep_light_hours','daily_sleep_rem_hours','daily_sleep_awake_hours']} 
  step=true
/>

```sql daily_sleep_time_hours
select
    daily_sleep_calendar_date,
    daily_sleep_time_seconds / 60 / 60 as daily_sleep_time_hours
from garmin.garmin_sleep_view
where daily_sleep_calendar_date between '${inputs.date_range.start}' and '${inputs.date_range.end}'
```

<BarChart
  title="Sleep Time by Date (Hours)"
  data={daily_sleep_time_hours}
  x=daily_sleep_calendar_date
  y=daily_sleep_time_hours
/>
