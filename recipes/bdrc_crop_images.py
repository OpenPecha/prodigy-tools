import csv
import logging

import prodigy

from tools.config import PAGE_CROPPING_BUCKET, page_cropping_s3_client

# s3 cofig
s3_client = page_cropping_s3_client
bucket_name = PAGE_CROPPING_BUCKET


# log config 
logging.basicConfig(
    filename="/usr/local/prodigy/logs/bdrc_crop_images.log",
    format="%(levelname)s: %(message)s",
    level=logging.INFO,
    )

# Prodigy has a logger named "prodigy" according to 
# https://support.prodi.gy/t/how-to-write-log-data-to-file/1427/10
prodigy_logger = logging.getLogger('prodigy')
prodigy_logger.setLevel(logging.INFO)

@prodigy.recipe("bdrc-crop-images-recipe")
def bdrc_crop_images_recipe(dataset, csv_file):
    logging.info(f"dataset:{dataset}, csv_file_path:{csv_file}")
    obj_keys = []
    with open(csv_file) as _file:
        for csv_line in list(csv.reader(_file, delimiter=",")):
            s3_key = csv_line[0]
            # TODO: filter non-image files
            obj_keys.append(s3_key)
    return {
        "dataset": dataset,
        "stream": stream_from_s3(obj_keys),
        "view_id": "image_manual",
        "config": {
            "labels": ["PAGE"]
        }
    }


def stream_from_s3(obj_keys):
    for obj_key in obj_keys:
        image_url = s3_client.generate_presigned_url(
            ClientMethod="get_object",
            Params={"Bucket": bucket_name, "Key": obj_key},
            ExpiresIn=31536000
        )
        image_id = (obj_key.split("/"))[-1]
        yield {"id": image_id, "image": image_url}