import boto3
import datetime
import os
import json
import uuid

import garth

s3_client = boto3.client('s3')
secrets_client = boto3.client('secretsmanager')

S3_BUCKET = os.environ['S3_BUCKET']
GARMIN_USERNAME_SECRET = os.environ['GARMIN_USERNAME']
GARMIN_PASSWORD_SECRET = os.environ['GARMIN_PASSWORD']


def get_secret_value(secret_arn):
    response = secrets_client.get_secret_value(SecretId=secret_arn)
    return response.get('SecretString')


def sleep_data(garth_client):
    '''
    {
        "dailySleepDTO": {
            "id": 1696611960000,
            "userProfilePK": 000000000,
            "calendarDate": "2023-10-07",
            "sleepTimeSeconds": 24540,
            "napTimeSeconds": 0,
            "sleepWindowConfirmed": true,
            "sleepWindowConfirmationType": "enhanced_confirmed_final",
            "sleepStartTimestampGMT": 1696611960000,
            "sleepEndTimestampGMT": 1696636500000,
            "sleepStartTimestampLocal": 1696640760000,
            "sleepEndTimestampLocal": 1696665300000,
            "autoSleepStartTimestampGMT": null,
            "autoSleepEndTimestampGMT": null,
            "sleepQualityTypePK": null,
            "sleepResultTypePK": null,
            "unmeasurableSleepSeconds": 0,
            "deepSleepSeconds": 6900,
            "lightSleepSeconds": 14400,
            "remSleepSeconds": 3240,
            "awakeSleepSeconds": 0,
            "deviceRemCapable": true,
            "retro": false,
            "sleepFromDevice": true,
            "averageSpO2Value": 96.0,
            "lowestSpO2Value": 91,
            "highestSpO2Value": 98,
            "averageSpO2HRSleep": 62.0,
            "averageRespirationValue": 12.0,
            "lowestRespirationValue": 9.0,
            "highestRespirationValue": 15.0,
            "awakeCount": 0,
            "avgSleepStress": 17.0,
            "ageGroup": "ADULT",
            "sleepScoreFeedback": "POSITIVE_CONTINUOUS",
            "sleepScoreInsight": "NONE",
            "sleepScores": {
                "totalDuration": {
                    "qualifierKey": "FAIR",
                    "optimalStart": 28800.0,
                    "optimalEnd": 28800.0
                },
                "stress": {
                    "qualifierKey": "FAIR",
                    "optimalStart": 0.0,
                    "optimalEnd": 15.0
                },
                "awakeCount": {
                    "qualifierKey": "EXCELLENT",
                    "optimalStart": 0.0,
                    "optimalEnd": 1.0
                },
                "overall": {
                    "value": 79,
                    "qualifierKey": "FAIR"
                },
                "remPercentage": {
                    "value": 13,
                    "qualifierKey": "FAIR",
                    "optimalStart": 21.0,
                    "optimalEnd": 31.0,
                    "idealStartInSeconds": 5153.4,
                    "idealEndInSeconds": 7607.4
                },
                "restlessness": {
                    "qualifierKey": "EXCELLENT",
                    "optimalStart": 0.0,
                    "optimalEnd": 5.0
                },
                "lightPercentage": {
                    "value": 59,
                    "qualifierKey": "EXCELLENT",
                    "optimalStart": 30.0,
                    "optimalEnd": 64.0,
                    "idealStartInSeconds": 7362.0,
                    "idealEndInSeconds": 15705.6
                },
                "deepPercentage": {
                    "value": 28,
                    "qualifierKey": "EXCELLENT",
                    "optimalStart": 16.0,
                    "optimalEnd": 33.0,
                    "idealStartInSeconds": 3926.4,
                    "idealEndInSeconds": 8098.2
                }
            },
            "sleepVersion": 2
        },
        "sleepMovement": [
            {
                "startGMT": "2023-10-06T16:06:00.0",
                "endGMT": "2023-10-06T16:07:00.0",
                "activityLevel": 5.677653939613456
            },
            ...
        ],
        "remSleepData": true,
        "sleepLevels": [
            {
                "startGMT": "2023-10-06T17:06:00.0",
                "endGMT": "2023-10-06T17:26:00.0",
                "activityLevel": 1.0
            },
            ...
        ],
        "sleepRestlessMoments": [
            {
                "value": 1,
                "startGMT": 1696612320000
            },
            ...
        ],
        "restlessMomentsCount": 16,
        "wellnessSpO2SleepSummaryDTO": {
            "userProfilePk": 000000000,
            "deviceId": 1111111111,
            "sleepMeasurementStartGMT": "2023-10-06T17:07:00.0",
            "sleepMeasurementEndGMT": "2023-10-06T23:55:00.0",
            "alertThresholdValue": null,
            "numberOfEventsBelowThreshold": null,
            "durationOfEventsBelowThreshold": null,
            "averageSPO2": 96.0,
            "averageSpO2HR": 62.0,
            "lowestSPO2": 91
        },
        "wellnessEpochSPO2DataDTOList": [
            {
                "userProfilePK": 116807974,
                "epochTimestamp": "2023-10-06T17:06:00.0",
                "deviceId": 1111111111,
                "calendarDate": "2023-10-07T00:00:00.0",
                "epochDuration": 60,
                "spo2Reading": 97,
                "readingConfidence": 2
            },
            ...
        ],
        "wellnessEpochRespirationDataDTOList": [
            {
                "startTimeGMT": 1696611960000,
                "respirationValue": 15.0
            },
            ...
        ],
        "sleepHeartRate": [
            {
                "value": 78,
                "startGMT": 1696611960000
            },
            ...
        ],
        "bodyBatteryChange": 67,
        "restingHeartRate": 67
    }
    '''
    try:
        sleep = garth_client.connectapi(
            f"/wellness-service/wellness/dailySleepData/{garth.client.username}",
            params={"date": datetime.date.today().isoformat(),
                    "nonSleepBufferMinutes": 60},
        )
        return sleep
    except Exception as e:
        print(e)


def stress_data(garth_client):
    '''
    {
        "userProfilePK": 000000000,
        "calendarDate": "2023-10-07",
        "startTimestampGMT": "2023-10-06T16:00:00.0",
        "endTimestampGMT": "2023-10-07T08:53:00.0",
        "startTimestampLocal": "2023-10-07T00:00:00.0",
        "endTimestampLocal": "2023-10-07T16:53:00.0",
        "maxStressLevel": 95,
        "avgStressLevel": 43,
        "stressChartValueOffset": 1,
        "stressChartYAxisOrigin": -1,
        "stressValueDescriptorsDTOList": [
            {
                "key": "timestamp",
                "index": 0
            },
            {
                "key": "stressLevel",
                "index": 1
            }
        ],
        "stressValuesArray": [
            [
                1696608000000,
                63
            ],
            ...
        ],
        "bodyBatteryValueDescriptorsDTOList": 
            {
                "bodyBatteryValueDescriptorIndex": 0, 
                "bodyBatteryValueDescriptorKey": "timestamp"
            }, 
            {
                "bodyBatteryValueDescriptorIndex": 1, 
                "bodyBatteryValueDescriptorKey": "bodyBatteryStatus"
            }, 
            {
                "bodyBatteryValueDescriptorIndex": 2, 
                "bodyBatteryValueDescriptorKey": "bodyBatteryLevel"
            }, 
            {
                "bodyBatteryValueDescriptorIndex": 3, 
                "bodyBatteryValueDescriptorKey": "bodyBatteryVersion"
            }
        ],
        "bodyBatteryValuesArray": [
            [
                1696608000000,
                "MEASURED",
                6,
                2.0
            ],
            ...
        ]
    '''
    try:
        stress = garth_client.connectapi(
            f"/wellness-service/wellness/dailyStress/{datetime.date.today().isoformat()}")
        return stress
    except Exception as e:
        print(e)


def lambda_handler(event, context):

    garmin_user = get_secret_value(GARMIN_USERNAME_SECRET)
    garmin_pass = get_secret_value(GARMIN_PASSWORD_SECRET)

    garth.login(garmin_user, garmin_pass)

    try:
        sleep_json_data = sleep_data(garth_client=garth)
        s3_client.put_object(
            Bucket=S3_BUCKET,
            Key=f'sleep/{datetime.date.today().isoformat()}/{uuid.uuid4()}.json',
            Body=json.dumps(sleep_json_data)
        )

        stress_json_data = stress_data(garth_client=garth)
        s3_client.put_object(
            Bucket=S3_BUCKET,
            Key=f'stress/{datetime.date.today().isoformat()}/{uuid.uuid4()}.json',
            Body=json.dumps(stress_json_data)
        )
    except Exception as e:
        print(e)
