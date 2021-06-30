import os
import uuid
import boto3
from botocore.client import Config

BUCKET_NAME = os.environ.get("BUCKET_NAME")
INPUT_PREFIX = 'input'
OUTPUT_PREFIX = 'output'

# Get the service client.
s3 = boto3.session.Session().client(
    service_name='s3',
    config=Config(signature_version='s3v4'),
    endpoint_url=os.environ.get('S3_ENDPOINT', 'https://s3.amazonaws.com'),
)


def generate_procedure(procedure, params):
    # 1. create folders name
    print(f'Bucket name: {BUCKET_NAME}')
    input_prefix = "/".join([procedure, INPUT_PREFIX])
    print(f'Input prefix: {input_prefix}')
    output_prefix = "/".join([
        procedure,
        OUTPUT_PREFIX,
        f'{params.get("lastname", "UNKNOWN")}-{params.get("name", "UNKNOWN")}-{uuid.uuid4()}'
    ])
    print(f'Output prefix: {output_prefix}')
    # 2. Get files from the input folder
    input_files = s3.list_objects_v2(
        Bucket=BUCKET_NAME,
        Prefix=input_prefix
    )

    for file in input_files.get('Contents'):
        key = file.get('Key')
        file_name = key.split("/")[-1]
        print(f'Key: {key}, File name: {file_name}')
        if file_name:
            data = s3.get_object(Bucket=BUCKET_NAME, Key=key)
            contents = data['Body'].read()
            # 3. TODO Replace values in the file
            # 4. Write the changes to the output folder
            output_key = "/".join([
                output_prefix,
                f'{params.get("lastname", "UNKNOWN")}-{params.get("name", "UNKNOWN")}-{file_name}'
            ])
            print(f'Output key: {output_key}')
            s3.put_object(Body=contents, Bucket=BUCKET_NAME, Key=output_key)
