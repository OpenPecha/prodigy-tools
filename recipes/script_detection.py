import os
import csv
import boto3
import prodigy
import logging

# s3 cofig
os.environ["AWS_SHARED_CREDENTIALS_FILE"] = "/home/ta4tsering/.aws/credentials"
s3 = boto3.resource("s3")
s3_client = boto3.client("s3")
BUCKET_NAME = "image-processing.bdrc.io"

# log config 
logging.basicConfig(
    filename="/usr/local/prodigy/logs/script_detection.log",
    format="%(levelname)s: %(message)s",
    level=logging.INFO,
    )

# Prodigy has a logger named "prodigy" according to 
# https://support.prodi.gy/t/how-to-write-log-data-to-file/1427/10
prodigy_logger = logging.getLogger('prodigy')
prodigy_logger.setLevel(logging.INFO)

@prodigy.recipe("script-detection-recipe")
def script_detection_recipe(dataset, csv_file):
    logging.info(f"dataset:{dataset}, csv_file_path:{csv_file}")
    with open(csv_file) as _file:
        obj_keys = []
        for csv_line in list(csv.reader(_file, delimiter=",")):
            s3_key = csv_line[0]
            # TODO: filter non-image files
            obj_keys.append(s3_key)
    return {
        "dataset": dataset,
        "stream": stream_from_s3(obj_keys),
        "view_id": "blocks",
        "config": {
            "blocks": [
                {"view_id": "choice", "text": None}
                ]
            } 
        }

def stream_from_s3(obj_keys):
    options = [
        {"id": 2, "text": "Uchen"},
        {"id": 1, "text": "Ume"},
        {"id": 0, "text": "etc"}
    ]
    for obj_key in obj_keys:
        image_url = s3_client.generate_presigned_url(
            ClientMethod="get_object",
            Params={"Bucket": BUCKET_NAME, "Key": obj_key},
            ExpiresIn=31536000
        )
        image_id = (obj_key.split("/"))[-1]
        yield {"id": image_id, "image": image_url, "options": options}
