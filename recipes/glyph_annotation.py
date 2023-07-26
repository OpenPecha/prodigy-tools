import logging
import jsonlines

import prodigy
from tools.config import MONLAM_AI_OCR_BUCKET, monlam_ocr_s3_client
import jsonlines
from prodigy import set_hashes


s3_client = monlam_ocr_s3_client
bucket_name = MONLAM_AI_OCR_BUCKET



@prodigy.recipe("glyph-recipe")
def glyph_recipe(dataset, jsonl_file):
    logging.info(f"dataset:{dataset}, jsonl_file_path:{jsonl_file}")
    blocks = [
        {
            "view_id": "image_manual",
            "labels": ["Base Line", "Glyph"],
        },
        {
            "view_id": "text"
        },
    ]
    return {
        "dataset": dataset,
        "stream": stream_from_jsonl(jsonl_file),
        "view_id": "blocks",
        "config": {
            "blocks": blocks
        }
    }

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
            obj_key = line["image_url"]
            text = line["text"]
            image_url = get_new_url(obj_key)
            eg = {"id": image_id, "image": image_url, "text": text}
            yield set_hashes(eg, input_keys=("id"))

