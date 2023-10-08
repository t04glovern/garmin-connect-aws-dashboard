WITH base AS (
  SELECT 
    userProfilePK,
    calendarDate,
    element_at(t.stressValuesItem, 1) as timestampValue,
    element_at(t.stressValuesItem, 2) as stressLevel
  FROM {{ source('garmin', 'garmin_stress') }}
  CROSS JOIN UNNEST(stressValuesArray) AS t (stressValuesItem)
)

SELECT
  userProfilePK,
  calendarDate,
  timestampValue,
  stressLevel
FROM base