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

# Main function to parse arguments and call appropriate functions
def main():
    parser = argparse.ArgumentParser(description="S3 Bucket Management CLI")
    
    subparsers = parser.add_subparsers(dest='command', help='Sub-command help')

    # Sub-command to list all files in the "x-wing" directory
    parser_list = subparsers.add_parser('list', help='List all files in the "x-wing" directory')
    parser_list.add_argument('bucket', type=str, help='Name of the S3 bucket')

    # Sub-command to upload a file to the "x-wing" directory
    parser_upload = subparsers.add_parser('upload', help='Upload a file to the "x-wing" directory in the bucket')
    parser_upload.add_argument('bucket', type=str, help='Name of the S3 bucket')
    parser_upload.add_argument('file_path', type=str, help='Path of the local file to upload')
    parser_upload.add_argument('s3_key', type=str, help='S3 object key (file name in the "x-wing" directory)')

    # Sub-command to list files matching a regex in the "x-wing" directory
    parser_list_regex = subparsers.add_parser('list_regex', help='List files matching a regex in the "x-wing" directory')
    parser_list_regex.add_argument('bucket', type=str, help='Name of the S3 bucket')
    parser_list_regex.add_argument('pattern', type=str, help='Regex pattern to filter files')

    # Sub-command to delete files matching a regex in the "x-wing" directory
    parser_delete_regex = subparsers.add_parser('delete_regex', help='Delete files matching a regex in the "x-wing" directory')
    parser_delete_regex.add_argument('bucket', type=str, help='Name of the S3 bucket')
    parser_delete_regex.add_argument('pattern', type=str, help='Regex pattern to match files for deletion')

    args = parser.parse_args()

    # Determine which command to execute
    if args.command == 'list':
        list_files(args.bucket)
    elif args.command == 'upload':
        upload_file(args.bucket, args.file_path, args.s3_key)
    elif args.command == 'list_regex':
        list_files_with_regex(args.bucket, args.pattern)
    elif args.command == 'delete_regex':
        delete_files_with_regex(args.bucket, args.pattern)
    else:
        parser.print_help()

if __name__ == '__main__':
    main()