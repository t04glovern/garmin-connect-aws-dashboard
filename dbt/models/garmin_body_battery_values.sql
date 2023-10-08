WITH battery_base AS (
  SELECT 
    userProfilePK,
    calendarDate,
    element_at(t.bodyBatteryValuesArray, 1) as bodyBatteryTimestamp,
    element_at(t.bodyBatteryValuesArray, 2) as bodyBatteryStatus,
    element_at(t.bodyBatteryValuesArray, 3) as bodyBatteryLevel,
    element_at(t.bodyBatteryValuesArray, 4) as bodyBatteryVersion
  FROM {{ source('garmin', 'garmin_stress') }}
  CROSS JOIN UNNEST(bodyBatteryValuesArray) AS t (bodyBatteryValuesArray)
)

SELECT
  userProfilePK,
  calendarDate,
  bodyBatteryTimestamp,
  bodyBatteryStatus,
  bodyBatteryLevel,
  bodyBatteryVersion
FROM battery_base