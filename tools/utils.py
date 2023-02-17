import os
import io
import csv
import boto3
import botocore


def upload_to_s3(data, s3_key, s3_bucket):
    s3_bucket.put_object(Key=s3_key, Body=data)


def get_base_directories(s3_client, bucket_name):
    response = s3_client.list_objects_v2(Bucket=bucket_name, Prefix='', Delimiter='/')
    for content in response.get('CommonPrefixes', []):
        yield content


def list_obj_keys(prefix, s3_client, bucket_name):
    obj_keys = []
    continuation_token = None
    while True:
        if continuation_token:
            response = s3_client.list_objects_v2(Bucket=bucket_name, Prefix=prefix, ContinuationToken=continuation_token)
        else:
            response = s3_client.list_objects_v2(Bucket=bucket_name, Prefix=prefix)
        if response['Contents']:
            for obj in response['Contents']:
                obj_key = obj['Key']
                obj_keys.append(obj_key)
        continuation_token = response.get("NextContinuationToken")
        if not continuation_token:
            break
    return obj_keys


def create_output_s3_prefix(s3_prefix):
    prefix = list(s3_prefix.split("/"))
    dir_name = prefix[0]
    work_id = prefix[1]
    _type  = prefix[2]
    remaining = "/".join(prefix[3:-1])
    output_s3_path = f"{dir_name}/{work_id}/{_type}-web/{remaining}"
    return output_s3_path


def is_archived(key, config):
    if len(config) != 0:
        s3_client = config['target_s3_client']
        bucket_name = config['target_bucket_name']
        try:
            s3_client.head_object(Bucket=bucket_name, Key=key)
        except botocore.errorfactory.ClientError:
            return False
        return True
    return False
    


def get_s3_bits(s3_key, s3_bucket):
    filebits = io.BytesIO()
    try:
        s3_bucket.download_fileobj(s3_key, filebits)
        return filebits, None
    except botocore.exceptions.ClientError as error:
        return None, error


def update_catalog(s3_key, csv_name):
    with open(f"./data/{csv_name}.csv",'a') as f:
        writer = csv.writer(f)
        writer.writerow([s3_key])