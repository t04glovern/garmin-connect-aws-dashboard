---
title: Garmin Data
---

<Details title='How to edit this page'>

  This page can be found in your project at `/pages/index.md`. Make a change to the markdown file and save it to see the change take effect in your browser.
</Details>

```sql daily_sleep_avg_stress
select
    daily_sleep_calendar_date,
    daily_sleep_avg_stress
from garmin.garmin_sleep_view
where daily_sleep_calendar_date >= '2023-01-01'
```

<CalendarHeatmap 
  data={daily_sleep_avg_stress}
  date=daily_sleep_calendar_date
  value=daily_sleep_avg_stress
  title="Average Sleep Stress by Date"
/>

```sql daily_sleep_time_hours
select
    daily_sleep_calendar_date,
    daily_sleep_time_seconds / 60 / 60 as daily_sleep_time_hours
from garmin.garmin_sleep_view
where daily_sleep_calendar_date >= '2023-01-01'
```

<BarChart 
  data={daily_sleep_time_hours}
  x=daily_sleep_calendar_date
  y=daily_sleep_time_hours
  title="Sleep Time by Date (Hours)"
/>