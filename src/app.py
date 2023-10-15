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


def sleep_data(garth_client: Client) -> dict:
    """
    Retrieves the daily sleep data for the user associated with the provided Garmin client.

    Args:
        garth_client (Client): The Garmin Connect API client.

    Returns:
        dict: The daily sleep data for the user.
    """
    try:
        return garth_client.connectapi(
            f"/wellness-service/wellness/dailySleepData/{garth_client.username}",
            params={"date": datetime.date.today().isoformat(),
                    "nonSleepBufferMinutes": 60},
        )
    except Exception as e:
        print(e)


def stress_data(garth_client: Client) -> dict:
    """
    Retrieves the daily stress data from the Garmin Connect API for the current date.

    Args:
        garth_client (Client): The Garmin Connect API client.

    Returns:
        dict: The daily stress data for the current date for the user.
    """
    try:
        return garth_client.connectapi(
            f"/wellness-service/wellness/dailyStress/{datetime.date.today().isoformat()}")
    except Exception as e:
        print(e)


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

        sleep_json_data = sleep_data(garth_client=garth_client)
        client.put_object(
            Bucket=garmin_s3_bucket,
            Key=f'sleep/{datetime.date.today().isoformat()}/{uuid.uuid4()}.json',
            Body=json.dumps(sleep_json_data)
        )

        stress_json_data = stress_data(garth_client=garth_client)
        client.put_object(
            Bucket=garmin_s3_bucket,
            Key=f'stress/{datetime.date.today().isoformat()}/{uuid.uuid4()}.json',
            Body=json.dumps(stress_json_data)
        )
    except Exception as e:
        print(e)
