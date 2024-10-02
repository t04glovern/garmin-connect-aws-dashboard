import datetime
import json
import logging
import os
import uuid

import boto3
from garth.http import Client

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def get_secret_value(secret_arn: str):
    """
    Retrieves the secret value from AWS Secrets Manager using the provided secret ARN.

    Args:
        secret_arn (str): The ARN of the secret to retrieve.

    Returns:
        str: The secret value as a string.
    """
    client = boto3.client('secretsmanager')
    response = client.get_secret_value(SecretId=secret_arn)
    return response.get('SecretString')


def get_processing_date():
    """
    Gets the processing date from the DATE_TO_PROCESS environment variable.
    If the variable is not set, defaults to the previous day's date.

    Returns:
        str: The processing date as a string in ISO format.
    """
    if 'DATE_TO_PROCESS' in os.environ:
        return os.environ['DATE_TO_PROCESS']
    else:
        yesterday = datetime.date.today() - datetime.timedelta(days=1)
        return yesterday.isoformat()


def sleep_data(garth_client: Client, process_date: str) -> dict:
    """
    Retrieves the daily sleep data for the specified date.

    Args:
        garth_client (Client): The Garmin Connect API client.
        process_date (str): The date to process.

    Returns:
        dict: The daily sleep data for the user.
    """
    try:
        return garth_client.connectapi(
            f"/wellness-service/wellness/dailySleepData/{garth_client.username}",
            params={"date": process_date, "nonSleepBufferMinutes": 60},
        )
    except Exception as e:
        logger.error(e)


def stress_data(garth_client: Client, process_date: str) -> dict:
    """
    Retrieves the daily stress data for the specified date.

    Args:
        garth_client (Client): The Garmin Connect API client.
        process_date (str): The date to process.

    Returns:
        dict: The daily stress data for the user.
    """
    try:
        return garth_client.connectapi(
            f"/wellness-service/wellness/dailyStress/{process_date}")
    except Exception as e:
        logger.error(e)


def lambda_handler(event, context):
    """
    Lambda function that logs into a Garmin account, retrieves sleep and stress data, and uploads it to an S3 bucket.

    :param event: AWS Lambda uses this parameter to pass in event data to the handler.
    :param context: AWS Lambda uses this parameter to provide your handler the runtime information of the Lambda function that is executing.
    :return: None
    """
    garmin_s3_bucket = os.environ['GARMIN_S3_BUCKET']

    garmin_user = get_secret_value(os.environ['GARMIN_USERNAME'])
    garmin_pass = get_secret_value(os.environ['GARMIN_PASSWORD'])

    garth_client = Client()
    garth_client.login(garmin_user, garmin_pass)

    try:
        client = boto3.client('s3')

        process_date = get_processing_date()

        date_obj = datetime.datetime.strptime(process_date, "%Y-%m-%d")
        year = date_obj.strftime("%Y")
        month = date_obj.strftime("%m")
        day = date_obj.strftime("%d")

        sleep_json_data = sleep_data(garth_client=garth_client, process_date=process_date)
        client.put_object(
            Bucket=garmin_s3_bucket,
            Key=f'sleep/year={year}/month={month}/day={day}/{uuid.uuid4()}.json',
            Body=json.dumps(sleep_json_data)
        )

        stress_json_data = stress_data(garth_client=garth_client, process_date=process_date)
        client.put_object(
            Bucket=garmin_s3_bucket,
            Key=f'stress/year={year}/month={month}/day={day}/{uuid.uuid4()}.json',
            Body=json.dumps(stress_json_data)
        )
    except Exception as e:
        logger.error(e)
