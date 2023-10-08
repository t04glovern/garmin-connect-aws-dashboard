CREATE EXTERNAL TABLE IF NOT EXISTS garmin_stress (
    userProfilePK bigint,
    calendarDate date,
    startTimestampGMT timestamp,
    endTimestampGMT timestamp,
    startTimestampLocal timestamp,
    endTimestampLocal timestamp,
    maxStressLevel int,
    avgStressLevel int,
    stressChartValueOffset int,
    stressChartYAxisOrigin int,
    stressValueDescriptorsDTOList array<struct <
        key: string,
        index: int>>,
    stressValuesArray array<array<bigint>>,
    bodyBatteryValueDescriptorsDTOList array<struct <
        bodyBatteryValueDescriptorIndex: int,
        bodyBatteryValueDescriptorKey: string>>,
    bodyBatteryValuesArray array<array<string>>
)
PARTITIONED BY (
    year string,
    month string,
    day string
)
ROW FORMAT SERDE 'org.apache.hive.hcatalog.data.JsonSerDe'
WITH SERDEPROPERTIES ( "timestamp.formats"="yyyy-MM-dd'T'HH:mm:ss.SSSSSSZZ" )
LOCATION 's3://garmin-connection-aws-cron-s3bucket-ucg6p4b0lajd/stress/'
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
    "storage.location.template" = "s3://garmin-connection-aws-cron-s3bucket-ucg6p4b0lajd/stress/${year}-${month}-${day}"
);