
import json
import logging

import prodigy

from tools.config import LAYOUT_ANALYSIS_BUCKET, layout_analysis_s3_client

#s3 config
s3_client = layout_analysis_s3_client
bucket_name = LAYOUT_ANALYSIS_BUCKET

# log config 
logging.basicConfig(
    filename="/usr/local/prodigy/logs/review_annotations.log",
    format="%(levelname)s: %(message)s",
    level=logging.INFO,
    )

# Prodigy has a logger named "prodigy" according to 
# https://support.prodi.gy/t/how-to-write-log-data-to-file/1427/10
prodigy_logger = logging.getLogger('prodigy')
prodigy_logger.setLevel(logging.INFO)

@prodigy.recipe("review-layout-annotation-recipe")
def review_layout_annotation_recipe(dataset, jsonl_path):
    logging.info(f"dataset: {dataset}, jsonl_path: {jsonl_path}")
    return {
        "dataset": dataset,
        "stream": get_stream_from_jsonl(jsonl_path),
        "view_id": "image_manual",
        "config": {
            "labels": ["Text-Area", "Illustration", "Caption", "Margin", "Header", "Footer", "Hole", "Table", "Other"]
        }
    }


def get_stream_from_jsonl(jsonl_path):
    with open(jsonl_path) as f:
        for line in f:
            content_dict = json.loads(line)
            id = content_dict['id']
            spans = content_dict['spans']
            new_url = get_new_url(content_dict['image'])
            yield  {"id": id,"image": new_url, "spans": spans}


def get_new_url(image_url):
    key = "/".join(image_url.split("?")[0].split("/")[4:])
    new_image_url = s3_client.generate_presigned_url(
        ClientMethod="get_object",
        Params={"Bucket": bucket_name, "Key": key},
        ExpiresIn=31536000
    )
    return new_image_url