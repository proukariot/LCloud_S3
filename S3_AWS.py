import boto3
import argparse
import os
import re
from botocore.exceptions import NoCredentialsError, ClientError

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


# Function to upload a file to the "x-wing" directory of the bucket
def upload_file(bucket_name, file_path, s3_key):
    try:
        # Ensure the s3_key has the PREFIX
        full_s3_key = PREFIX + s3_key
        s3_client.upload_file(file_path, bucket_name, full_s3_key)
        print(f"File '{file_path}' uploaded to '{full_s3_key}' in bucket '{bucket_name}'.")
    except FileNotFoundError:
        print(f"File '{file_path}' not found.")
    except NoCredentialsError:
        print("Credentials not available.")
    except ClientError as e:
        print(f"Error: {e}")

#Function to delete files in the "x-wing" directory that match a regex
def delete_files_with_regex(bucket_name, pattern):
    try:
        response = s3_client.list_objects_v2(Bucket=bucket_name, Prefix=PREFIX)
        if 'Contents' in response:
            regex = re.compile(pattern)
            files_to_delete = [obj['Key'] for obj in response['Contents'] if regex.match(obj['Key'])]
            
            if files_to_delete:
                print(f"Deleting files from {bucket_name}/{PREFIX} matching pattern '{pattern}':")
                for file_key in files_to_delete:
                    print(f"Deleting {file_key}...")
                    s3_client.delete_object(Bucket=bucket_name, Key=file_key)
                print(f"Deleted {len(files_to_delete)} files.")
            else:
                print(f"No files matched pattern '{pattern}'.")
        else:
            print(f"No files found in bucket {bucket_name}/{PREFIX}.")
    except NoCredentialsError:
        print("Credentials not available.")
    except ClientError as e:
        print(f"Error: {e}")