import os
import boto3
import configparser

PAGE_CROPPPING_BUCKET = "image-processing.bdrc.io"
BDRC_ARCHIVE_BUCKET = "archive.tbrc.org"
LAYOUT_ANALYSIS_BUCKET = "image-processing.openpecha"


aws_credentials_file = os.path.expanduser("~/.aws/credentials")
config = configparser.ConfigParser()
config.read(aws_credentials_file)


session1 = boto3.Session(
    aws_access_key_id= config.get("image_processing_bdrc_io", "aws_access_key_id"),
    aws_secret_access_key= config.get("image_processing_bdrc_io", "aws_secret_access_key")
)
s3_client1 = session1.client('s3')
s3_resource1 = session1.resource('s3')
page_cropping_bucket = s3_resource1.Bucket(PAGE_CROPPPING_BUCKET)


session2 = boto3.Session(
    aws_access_key_id= config.get("archive_tbrc_org", "aws_access_key_id"),
    aws_secret_access_key= config.get("archive_tbrc_org", "aws_secret_access_key")
)
s3_client2 = session2.client('s3')
s3_resource2 = session2.resource('s3')
bdrc_archive_bucket = s3_resource2.Bucket(BDRC_ARCHIVE_BUCKET)


session3 = boto3.Session(
    aws_access_key_id= config.get("image_processing_openpecha", "aws_access_key_id"),
    aws_secret_access_key= config.get("image_processing_openpecha", "aws_secret_access_key")
)
s3_client3 = session3.client('s3')
s3_resource3 = session3.resource('s3')
layout_analysis_bucket = s3_resource3.Bucket(LAYOUT_ANALYSIS_BUCKET)
