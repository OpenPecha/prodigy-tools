import boto3
import prodigy
import json
from prodigy.util import img_to_b64_uri
from typing import List, Optional
import os



@prodigy.recipe("custom-recipe")
def custom_recipe(dataset, s3_prefix):
    return {
        "dataset": dataset,
        "stream": stream_from_s3(s3_prefix),
        "view_id": "image"
        "label": "PAGE"
    }

def stream_from_s3(s3_prefix):
    # Get all loaded images.
    os.environ["AWS_SHARED_CREDENTIALS_FILE"] = "/home/ta4tsering/.aws/credentials"
    s3 = boto3.resource("s3")
    s3_client = boto3.client("s3")
    IMAGE_PROCESSING_BUCKET = "image-processing.bdrc.io"
    
    response = s3_client.list_objects_v2(Bucket=IMAGE_PROCESSING_BUCKET, Prefix=s3_prefix)
    if response:
        for info in response['Contents']:
            img_key = info['Key']
            # Read the image.
            obj = s3.Object(IMAGE_PROCESSING_BUCKET, img_key)
            img = obj.get()['Body'].read()

            # Provide response that Prodigy expects.
            yield json.dumps({'image': img_to_b64_uri(img, 'image/jpg')})
            
