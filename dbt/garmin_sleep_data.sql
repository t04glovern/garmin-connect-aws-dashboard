CREATE EXTERNAL TABLE IF NOT EXISTS garmin_sleep (
    bodyBatteryChange int,
    restingHeartRate int,
    remSleepData boolean,
    restlessMomentsCount int,
    dailySleepDTO struct<
        id: bigint,
        userProfilePK: int,
        calendarDate: date,
        sleepTimeSeconds: int,
        napTimeSeconds: int,
        sleepWindowConfirmed: boolean,
        sleepWindowConfirmationType: string,
        sleepStartTimestampGMT: bigint,
        sleepEndTimestampGMT: bigint,
        sleepStartTimestampLocal: bigint,
        sleepEndTimestampLocal: bigint,
        autoSleepStartTimestampGMT: bigint,
        autoSleepEndTimestampGMT: bigint,
        sleepQualityTypePK: bigint,
        sleepResultTypePK: bigint,
        unmeasurableSleepSeconds: int,
        deepSleepSeconds: int,
        lightSleepSeconds: int,
        remSleepSeconds: int,
        awakeSleepSeconds: int,
        deviceRemCapable: boolean,
        retro: boolean,
        sleepFromDevice: boolean,
        averageSpO2Value: float,
        lowestSpO2Value: int,
        highestSpO2Value: int,
        averageSpO2HRSleep: float,
        averageRespirationValue: float,
        lowestRespirationValue: float,
        highestRespirationValue: float,
        awakeCount: int,
        avgSleepStress: float,
        ageGroup: string,
        sleepScoreFeedback: string,
        sleepScoreInsight: string,
        sleepVersion: int,
        sleepScores: struct<
            totalDuration: struct<
                qualifierKey: string,
                optimalStart: float,
                optimalEnd: float
            >,
            stress: struct<
                qualifierKey: string,
                optimalStart: float,
                optimalEnd: float
            >,
            awakeCount: struct<
                qualifierKey: string,
                optimalStart: float,
                optimalEnd: float
            >,
            overall: struct<
                value: int,
                qualifierKey: string
            >,
            remPercentage: struct<
                value: int,
                qualifierKey: string,
                optimalStart: float,
                optimalEnd: float,
                idealStartInSeconds: float,
                idealEndInSeconds: float
            >,
            restlessness: struct<
                qualifierKey: string,
                optimalStart: float,
                optimalEnd: float
            >,
            lightPercentage: struct<
                value: int,
                qualifierKey: string,
                optimalStart: float,
                optimalEnd: float,
                idealStartInSeconds: float,
                idealEndInSeconds: float
            >,
            deepPercentage: struct<
                value: int,
                qualifierKey: string,
                optimalStart: float,
                optimalEnd: float,
                idealStartInSeconds: float,
                idealEndInSeconds: float
            >
        >
    >,
    sleepMovement array<struct<
        startGMT: timestamp,
        endGMT: timestamp,
        activityLevel: float
    >>,
    sleepLevels array<struct<
        startGMT: string,
        endGMT: string,
        activityLevel: float
    >>,
    sleepRestlessMoments array<struct<
        value: int,
        startGMT: bigint
    >>,
    wellnessSpO2SleepSummaryDTO struct<
        userProfilePk: int,
        deviceId: bigint,
        sleepMeasurementStartGMT: string,
        sleepMeasurementEndGMT: string,
        alertThresholdValue: int,
        numberOfEventsBelowThreshold: int,
        durationOfEventsBelowThreshold: int,
        averageSPO2: float,
        averageSpO2HR: float,
        lowestSPO2: int
    >,
    wellnessEpochSPO2DataDTOList array<struct<
        userProfilePK: int,
        epochTimestamp: timestamp,
        deviceId: bigint,
        calendarDate: timestamp,
        epochDuration: int,
        spo2Reading: int,
        readingConfidence: int
    >>,
    wellnessEpochRespirationDataDTOList array<struct<
        startTimeGMT: bigint,
        respirationValue: float
    >>,
    sleepHeartRate array<struct<
        value: int,
        startGMT: bigint
    >>,
    sleepStress array<struct<
        value: int,
        startGMT: bigint
    >>,
    sleepBodyBattery array<struct<
        value: int,
        startGMT: bigint
    >>
)
PARTITIONED BY (
    year int,
    month int,
    day int
)
ROW FORMAT SERDE 'org.apache.hive.hcatalog.data.JsonSerDe'
WITH SERDEPROPERTIES ( "timestamp.formats"="yyyy-MM-dd'T'HH:mm:ss.S" )
LOCATION 's3://garmin-connection-aws-cron-s3bucket-ucg6p4b0lajd/sleep/'
TBLPROPERTIES (
    "projection.enabled" = "true",
    "projection.year.type" = "integer",
    "projection.year.range" = "2023,2033",
    "projection.month.type" = "integer",
    "projection.month.range" = "1,12",
    "projection.month.digits" = "2",
    "projection.day.type" = "integer",
    "projection.day.range" = "1,31",
    "projection.day.digits" = "2",
    "storage.location.template" = "s3://garmin-connection-aws-cron-s3bucket-ucg6p4b0lajd/sleep/${year}-${month}-${day}"
);