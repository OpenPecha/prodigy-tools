import boto3
import prodigy
import json
from prodigy.util import img_to_b64_uri
from typing import List, Optional
import os
import logging

# s3 cofig
os.environ["AWS_SHARED_CREDENTIALS_FILE"] = "/home/ta4tsering/.aws/credentials"
s3 = boto3.resource("s3")
s3_client = boto3.client("s3")
IMAGE_PROCESSING_BUCKET = "image-processing.bdrc.io"

# log config 
logging.basicConfig(
    filename="bdrc_crop_images.log",
    format="%(levelname)s: %(message)s",
    level=logging.INFO,
    )

def stream_from_s3(s3_prefix):
    # Get all loaded images.
    response = s3_client.list_objects_v2(Bucket=IMAGE_PROCESSING_BUCKET, Prefix=s3_prefix)
    if response:
        for info in response['Contents']:
            img_key = info['Key']
            # Read the image.
            obj = s3.Object(IMAGE_PROCESSING_BUCKET, img_key)
            img = obj.get()['Body'].read()
            logging.info(f"s3_image_key: {img_key}")
            logging.info(f"image: {img_to_b64_uri(img, 'image/jpg')}")

            # Provide response that Prodigy expects.
            yield {'image': img_to_b64_uri(img, 'image/jpg')}
        
if __name__ == "__main__":
    stream_from_s3("")