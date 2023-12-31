WITH base AS (
  SELECT 
    userProfilePK,
    calendarDate,
    CAST(element_at(t.stressValuesItem, 1) AS bigint) as timestampValue,
    CAST(element_at(t.stressValuesItem, 2) AS int) as stressLevel,
    year, month, day
  FROM {{ source('garmin', 'garmin_stress') }}
  CROSS JOIN UNNEST(stressValuesArray) AS t (stressValuesItem)
)

SELECT
  userProfilePK,
  calendarDate,
  timestampValue,
  stressLevel,
  year, month, day
FROM base
