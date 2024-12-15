# Install Dependencies

```bash
pip install aws-sam-cli==1.132.0
```

## Run

```bash
sam build
sam validate
sam deploy
```

## Run Manually

```bash
cd src
pip install -r requirements.txt

export GARMIN_S3_BUCKET=garmin-connection-aws-cron-s3bucket-ucg6p4b0lajd
export AWS_DEFAULT_REGION=ap-southeast-2
export DATE_TO_PROCESS=2024-01-17

python app.py
```
