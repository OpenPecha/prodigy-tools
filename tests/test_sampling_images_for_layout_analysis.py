from pathlib import Path
import boto3
import os
import io
import botocore
from tools.layout_analysis.sampling_images_for_layout_analysis import get_image_keys
from tools.image_processing import ImageProcessing


os.environ["AWS_SHARED_CREDENTIALS_FILE"] = "~/.aws/credentials"
s3 = boto3.resource("s3")
s3_client = boto3.client("s3")
IMAGE_PROCESSING_BUCKET = "archive.tbrc.org"
s3_bucket = s3.Bucket(IMAGE_PROCESSING_BUCKET)


expected_s3_keys = [
    'Works/56/W26071/images/W26071-4032/40320003.tif',
    'Works/56/W26071/images/W26071-4032/40320004.tif',
    'Works/56/W26071/images/W26071-4032/40320005.tif',
    'Works/56/W26071/images/W26071-4032/40320006.tif']


def get_s3_bits(s3_key):
    filebits = io.BytesIO()
    try:
        s3_bucket.download_fileobj(s3_key, filebits)
        return filebits, None
    except botocore.exceptions.ClientError as error:
        return None, error


def test_sampling_images_for_layout_analysis():
    s3_keys = list((get_image_keys("OCRtest", "W26071")).splitlines())
    assert expected_s3_keys == s3_keys