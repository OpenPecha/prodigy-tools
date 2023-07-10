import logging
import jsonlines

import prodigy

from tools.config import LAYOUT_ANALYSIS_BUCKET, layout_analysis_s3_client

#s3 config
s3_client = layout_analysis_s3_client
bucket_name = LAYOUT_ANALYSIS_BUCKET

# log config 
logging.basicConfig(
    filename="/usr/local/prodigy/logs/line_segmentation_review.log",
    format="%(levelname)s: %(message)s",
    level=logging.INFO,
    )

# Prodigy has a logger named "prodigy" according to 
# https://support.prodi.gy/t/how-to-write-log-data-to-file/1427/10
prodigy_logger = logging.getLogger('prodigy')
prodigy_logger.setLevel(logging.INFO)

@prodigy.recipe("line-segmentation-review-recipe")
def line_segmentation_review_recipe(dataset, jsonl_file):
    logging.info(f"dataset:{dataset}, jsonl_file_path:{jsonl_file}")
    return {
        "dataset": dataset,
        "stream": stream_from_jsonl(jsonl_file),
        "view_id": "image_manual",
        "config": {
            "labels": ["Line"]
        }
    }

def get_obj_key(image_url):
    parts = image_url.split("/")
    obj_key = "/".join(parts[4:10]).split("?")[0]
    return obj_key

def get_new_url(image_url):
    new_image_url = s3_client.generate_presigned_url(
        ClientMethod="get_object",
        Params={"Bucket": bucket_name, "Key": image_url},
        ExpiresIn=31536000
    )
    return new_image_url

def stream_from_jsonl(jsonl_file):
    with jsonlines.open(jsonl_file) as reader:
        for line in reader:
            image_id = line["id"]
            image_url = line["image"]
            obj_key = get_obj_key(image_url)
            spans = line["spans"]
            image_url = get_new_url(obj_key)
            yield {"id": image_id, "image": image_url, "spans": spans}

