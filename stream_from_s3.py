import boto3
import os
import datetime
import logging

# s3 cofig
os.environ["AWS_SHARED_CREDENTIALS_FILE"] = "~/.aws/credentials"
s3 = boto3.resource("s3")
s3_client = boto3.client("s3")
IMAGE_PROCESSING_BUCKET = "image-processing.bdrc.io"

# log config 
logging.basicConfig(
    filename="bdrc_crop_images.log",
    format="%(levelname)s: %(message)s",
    level=logging.INFO,
    )

def stream_from_s3(obj_keys):
    # using generate_presigned_url
    for obj_key in obj_keys:
        image_url = s3_client.generate_presigned_url(
            ClientMethod="get_object",
            Params={"Bucket": IMAGE_PROCESSING_BUCKET, "Key": obj_key},
            ExpiresIn=3600
        )
        print(f"image: {image_url}")

def bdrc_crop_images_recipe(dataset, s3_prefix):
    logging.info(f"dataset:{dataset}, s3_prefix:{s3_prefix}")
    obj_list = s3_client.list_objects_v2(Bucket=IMAGE_PROCESSING_BUCKET, Prefix=s3_prefix)
    if not obj_list:
        logging.error("no object in s3 prefix")
        raise "no object in s3 prefix"
    obj_keys = []
    for obj in obj_list['Contents']:
        obj_key = obj['Key']
        # TODO: filter non-image files
        obj_keys.append(obj_key)
    stream_from_s3(obj_keys)
    return {
        "dataset": dataset,
        "stream": stream_from_s3(obj_keys),
        "view_id": "image_manual",
        "config": {
            "labels": ["PAGE"]
        }
    }

        
if __name__ == "__main__":
   bdrc_crop_images_recipe("crop_images", 'NLM1/W2KG208129/sources-web/W2KG208129-I2KG208175')