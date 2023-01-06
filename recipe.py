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
    }
def stream_from_s3(prefix):
    # Get all loaded images.
    os.environ["AWS_SHARED_CREDENTIALS_FILE"] = "/home/ta4tsering/.aws/credentials"
    s3 = boto3.client('s3')
    s3_bucket = s3.Bucket("image-processing.bdrc.io")
    
    # Build a paginator for when there are a lot of objects.
    paginator = s3.get_paginator('list_objects')
    paginate_params = {
        'Bucket': s3_bucket
    }

    # Check if only certain images from S3 should be loaded.
    if prefix is not None:
        paginate_params['Prefix'] = prefix

    page_iterator = paginator.paginate(**paginate_params)

    # Iterate through the pages.
    for page in page_iterator:
        # Iterate through items on the page.
        for obj in page['Contents']:
            img_key = obj['Key']

            # Read the image.
            img = s3.get_object(Bucket=s3_bucket, Key=img_key).get('Body').read()

            # Provide response that Prodigy expects.
            yield json.dumps({'image': img_to_b64_uri(img, 'image/jpg')})
            
