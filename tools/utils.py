import os
import io
import csv
import boto3
import botocore


# s3 config
# os.environ["AWS_SHARED_CREDENTIALS_FILE"] = "/home/ta4tsering/.aws/credentials"
os.environ["AWS_SHARED_CREDENTIALS_FILE"] = "~/.aws/credentials"
s3 = boto3.resource("s3")
s3_client = boto3.client("s3")
IMAGE_PROCESSING_BUCKET = "image-processing.bdrc.io"
s3_bucket = s3.Bucket(IMAGE_PROCESSING_BUCKET)


def upload_to_s3(data, s3_key):
    s3_bucket.put_object(Key=s3_key, Body=data)


def get_s3_image_keys(s3_prefix):
    s3_image_keys = []
    response = s3_client.list_objects_v2(Bucket=IMAGE_PROCESSING_BUCKET, Prefix=s3_prefix)
    if response:
        for info in response['Contents']:
            s3_image_key = info['Key']
            s3_image_keys.append(s3_image_key)
    return s3_image_keys


def create_output_s3_prefix(s3_prefix):
    prefix = list(s3_prefix.split("/"))
    dir_name = prefix[0]
    work_id = prefix[1]
    _type  = prefix[2]
    remaining = "/".join(prefix[3:-1])
    output_s3_path = f"{dir_name}/{work_id}/{_type}-web/{remaining}"
    return output_s3_path


def is_archived(key):
    try:
        s3_client.head_object(Bucket=IMAGE_PROCESSING_BUCKET, Key=key)
    except botocore.errorfactory.ClientError:
        return False
    return True


def get_s3_bits(s3_key):
    filebits = io.BytesIO()
    try:
        s3_bucket.download_fileobj(s3_key, filebits)
        return filebits, None
    except botocore.exceptions.ClientError as error:
        return None, error

def update_catalog(s3_key):
    with open(f"./data/page_cropping.csv",'a') as f:
        writer = csv.writer(f)
        writer.writerow([s3_key])

if __name__ == "__main__":
    pass