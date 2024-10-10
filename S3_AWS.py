import boto3
import argparse
import os
import re
from botocore.exceptions import NoCredentialsError, ClientError
from config import AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY

# Initialize the S3 client using environment variables
s3_client = boto3.client(
    's3',
    aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
    aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY'),
    region_name=os.getenv('AWS_REGION', 'eu-central-1')  # Default to eu-central-1 if not set
)

# Prefix (directory) we are limited to
PREFIX = 'x-wing/'

# Function to list all files in the "x-wing" directory of the S3 bucket
def list_files(bucket_name):
    try:
        response = s3_client.list_objects_v2(Bucket=bucket_name, Prefix=PREFIX)
        if 'Contents' in response:
            print(f"Files in {bucket_name}/{PREFIX}:")
            for obj in response['Contents']:
                print(obj['Key'])
        else:
            print(f"No files found in bucket {bucket_name}/{PREFIX}.")
    except NoCredentialsError:
        print("Credentials not available.")
    except ClientError as e:
        print(f"Error: {e}")