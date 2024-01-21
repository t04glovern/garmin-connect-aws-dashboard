WITH garmin_sleep AS (
  SELECT 
    bodyBatteryChange,
    restingHeartRate,
    remSleepData,
    restlessMomentsCount,
    dailySleepDTO.id AS daily_sleep_id,
    dailySleepDTO.userProfilePK AS daily_sleep_user_profile_pk,
    dailySleepDTO.calendarDate AS daily_sleep_calendar_date,
    dailySleepDTO.sleepTimeSeconds AS daily_sleep_time_seconds,
    dailySleepDTO.napTimeSeconds AS daily_sleep_nap_time_seconds,
    dailySleepDTO.sleepWindowConfirmed AS daily_sleep_window_confirmed,
    dailySleepDTO.sleepWindowConfirmationType AS daily_sleep_window_confirmation_type,
    dailySleepDTO.sleepStartTimestampGMT AS daily_sleep_start_timestamp_gmt,
    dailySleepDTO.sleepEndTimestampGMT AS daily_sleep_end_timestamp_gmt,
    dailySleepDTO.sleepStartTimestampLocal AS daily_sleep_start_timestamp_local,
    dailySleepDTO.sleepEndTimestampLocal AS daily_sleep_end_timestamp_local,
    dailySleepDTO.autoSleepStartTimestampGMT AS daily_sleep_auto_start_timestamp_gmt,
    dailySleepDTO.autoSleepEndTimestampGMT AS daily_sleep_auto_end_timestamp_gmt,
    dailySleepDTO.sleepQualityTypePK AS daily_sleep_quality_type_pk,
    dailySleepDTO.sleepResultTypePK AS daily_sleep_result_type_pk,
    dailySleepDTO.unmeasurableSleepSeconds AS daily_sleep_unmeasurable_seconds,
    dailySleepDTO.deepSleepSeconds AS daily_sleep_deep_seconds,
    dailySleepDTO.lightSleepSeconds AS daily_sleep_light_seconds,
    dailySleepDTO.remSleepSeconds AS daily_sleep_rem_seconds,
    dailySleepDTO.awakeSleepSeconds AS daily_sleep_awake_seconds,
    dailySleepDTO.deviceRemCapable AS daily_sleep_device_rem_capable,
    dailySleepDTO.retro AS daily_sleep_retro,
    dailySleepDTO.sleepFromDevice AS daily_sleep_from_device,
    dailySleepDTO.averageSpO2Value AS daily_sleep_avg_spo2_value,
    dailySleepDTO.lowestSpO2Value AS daily_sleep_lowest_spo2_value,
    dailySleepDTO.highestSpO2Value AS daily_sleep_highest_spo2_value,
    dailySleepDTO.averageSpO2HRSleep AS daily_sleep_avg_spo2_hr_sleep,
    dailySleepDTO.averageRespirationValue AS daily_sleep_avg_respiration_value,
    dailySleepDTO.lowestRespirationValue AS daily_sleep_lowest_respiration_value,
    dailySleepDTO.highestRespirationValue AS daily_sleep_highest_respiration_value,
    dailySleepDTO.awakeCount AS daily_sleep_awake_count,
    dailySleepDTO.avgSleepStress AS daily_sleep_avg_stress,
    dailySleepDTO.ageGroup AS daily_sleep_age_group,
    dailySleepDTO.sleepScoreFeedback AS daily_sleep_score_feedback,
    dailySleepDTO.sleepScoreInsight AS daily_sleep_score_insight,
    dailySleepDTO.sleepVersion AS daily_sleep_version,
    wellnessSpO2SleepSummaryDTO.userProfilePk AS wellness_spO2_user_profile_pk,
    wellnessSpO2SleepSummaryDTO.deviceId AS wellness_spO2_device_id,
    wellnessSpO2SleepSummaryDTO.sleepMeasurementStartGMT AS wellness_spO2_measurement_start_gmt,
    wellnessSpO2SleepSummaryDTO.sleepMeasurementEndGMT AS wellness_spO2_measurement_end_gmt,
    wellnessSpO2SleepSummaryDTO.alertThresholdValue AS wellness_spO2_alert_threshold,
    wellnessSpO2SleepSummaryDTO.numberOfEventsBelowThreshold AS wellness_spO2_events_below_threshold,
    wellnessSpO2SleepSummaryDTO.durationOfEventsBelowThreshold AS wellness_spO2_duration_below_threshold,
    wellnessSpO2SleepSummaryDTO.averageSPO2 AS wellness_spO2_avg,
    wellnessSpO2SleepSummaryDTO.averageSpO2HR AS wellness_spO2_avg_hr,
    wellnessSpO2SleepSummaryDTO.lowestSPO2 AS wellness_spO2_lowest,
    year, month, day
  FROM {{ source('garmin', 'garmin_sleep') }}
),

sleep_restless_moments_base AS (
  SELECT 
    dailySleepDTO.userProfilePK,
    dailySleepDTO.calendarDate,
    t.sleepRestlessMomentsItem.value as sleep_restless_value,
    t.sleepRestlessMomentsItem.startGMT as sleep_restless_start_gmt
  FROM {{ source('garmin', 'garmin_sleep') }}
  CROSS JOIN UNNEST(sleepRestlessMoments) AS t (sleepRestlessMomentsItem)
)

SELECT
  g.*,
  r.sleep_restless_value,
  r.sleep_restless_start_gmt,
  from_unixtime(r.sleep_restless_start_gmt / 1000) AS sleep_restless_start_datetime
FROM garmin_sleep AS g
LEFT JOIN sleep_restless_moments_base AS r 
ON g.daily_sleep_user_profile_pk = r.userProfilePK AND g.daily_sleep_calendar_date = r.calendarDate;