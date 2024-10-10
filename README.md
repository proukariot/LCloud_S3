# LCloud_S3
# S3 CLI Tool

This is a Python Command Line Interface (CLI) tool for interacting with an AWS S3 bucket named **"developer-task"**. The tool allows users to perform the following operations limited to the **"x-wing/"** prefix in the bucket:

- List all files in the `x-wing/` prefix
- Upload a local file to the `x-wing/` prefix
- List files in the `x-wing/` prefix that match a specified regex pattern
- Delete files from the `x-wing/` prefix that match a specified regex pattern

## Prerequisites

Before running the CLI, ensure you have the following:

- Python 3.1x installed
- AWS account with access to the S3 service
- `boto3` library installed. You can install it using pip:

```bash
pip install boto3
```
## Configuration
You need to configure your AWS credentials. This can be done by setting the following environment variables in your terminal:

```bash
export AWS_ACCESS_KEY_ID=YOUR_ACCESS_KEY_ID
export AWS_SECRET_ACCESS_KEY=YOUR_SECRET_ACCESS_KEY
export AWS_REGION=YOUR_AWS_REGION  
```
Replace YOUR_ACCESS_KEY_ID and YOUR_SECRET_ACCESS_KEY with your actual AWS credentials. The AWS_REGION can be set based on the region your S3 bucket is located in.

## Usage
1. List All Files in the x-wing/ Prefix
To list all files under the x-wing/ prefix in the "developer-task" bucket, run:

```bash
python S3_AWS.py list developer-task
```
2. Upload a File to the x-wing/ Prefix
To upload a local file to the x-wing/ prefix, use the following command:

```bash
python S3_AWS.py upload developer-task /path/to/local/file.txt filename_in_s3.txt
```
Replace /path/to/local/file.txt with the path to your local file and filename_in_s3.txt with the desired name in S3.

3. List Files Matching a Regex in the x-wing/ Prefix
To list files that match a regex pattern (e.g., all .txt files), run:

```bash
python S3_AWS.py list_regex developer-task '.*\.txt$'
```
4. Delete Files Matching a Regex in the x-wing/ Prefix
To delete files that match a regex pattern (e.g., all .log files), use the command:

```bash
python S3_AWS.py delete_regex developer-task '.*\.log$'
```
