import datetime
import json
import logging
import os
import uuid

import boto3
from garth.http import Client as GarthClient

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

garmin_s3_bucket = os.environ['GARMIN_S3_BUCKET']

garmin_user = get_secret_value(os.environ['GARMIN_USERNAME'])
garmin_pass = get_secret_value(os.environ['GARMIN_PASSWORD'])

garth_client = GarthClient()
garth_client.login(garmin_user, garmin_pass)

s3_client = boto3.client('s3')


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


def sleep_data(client: GarthClient) -> dict:
    """
    Retrieves the daily sleep data for the user associated with the provided Garmin client.

    Args:
        client (GarthClient): The Garmin Connect API client.

    Returns:
        dict: The daily sleep data for the user.
    """
    return client.connectapi(
        f"/wellness-service/wellness/dailySleepData/{garth_client.username}",
        params={"date": datetime.date.today().isoformat(),
                "nonSleepBufferMinutes": 60},
    )


def stress_data(client: GarthClient) -> dict:
    """
    Retrieves the daily stress data from the Garmin Connect API for the current date.

    Args:
        client (GarthClient): The Garmin Connect API client.

    Returns:
        dict: The daily stress data for the current date for the user.
    """
    return client.connectapi(
        f"/wellness-service/wellness/dailyStress/{datetime.date.today().isoformat()}")


def lambda_handler(_event, _context) -> None:
    """
    Lambda function that logs into a Garmin account, retrieves sleep and stress data, and uploads it to an S3 bucket.

    :param event: AWS Lambda uses this parameter to pass in event data to the handler.
    :param context: AWS Lambda uses this parameter to provide your handler the runtime information of the Lambda function that is executing.
    :return: None
    """

    sleep_json_data = sleep_data(garth_client)
    stress_json_data = stress_data(garth_client)

    s3_client.put_object(
        Bucket=garmin_s3_bucket,
        Key=f'sleep/{datetime.date.today().isoformat()}/{uuid.uuid4()}.json',
        Body=json.dumps(sleep_json_data)
    )
    s3_client.put_object(
        Bucket=garmin_s3_bucket,
        Key=f'stress/{datetime.date.today().isoformat()}/{uuid.uuid4()}.json',
        Body=json.dumps(stress_json_data)
    )
