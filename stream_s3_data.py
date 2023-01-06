import boto3
import prodigy
import json
from typing import List, Optional
import os



def stream_from_s3(s3_prefix):
    # Get all loaded images.
    os.environ["AWS_SHARED_CREDENTIALS_FILE"] = "~/.aws/credentials"
    s3 = boto3.resource("s3")
    s3_client = boto3.client("s3")
    IMAGE_PROCESSING_BUCKET = "image-processing.bdrc.io"
    
    # Build a paginator for when there are a lot of objects.
    response = s3_client.list_objects_v2(Bucket=IMAGE_PROCESSING_BUCKET, Prefix=s3_prefix)
    if response:
        for info in response['Contents']:
            img_key = info['Key']
            # Read the image.
            obj = s3.Object(IMAGE_PROCESSING_BUCKET, img_key)
            img = obj.get()['Body'].read()
            # Provide response that Prodigy expects.
            # yield json.dumps({'image': img_to_b64_uri(img, 'image/jpg')})
            print(img)
            
if __name__ == "__main__":
    stream_from_s3("NLM1/W2KG208129/sources-web/W2KG208129-I2KG208175")