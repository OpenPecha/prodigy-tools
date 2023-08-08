import logging
import jsonlines
import prodigy
import urllib.parse
from tools.config import MONLAM_AI_OCR_BUCKET, monlam_ocr_s3_client
from prodigy import set_hashes


s3_client = monlam_ocr_s3_client
bucket_name = MONLAM_AI_OCR_BUCKET


@prodigy.recipe("glyph-annotation-review-recipe")
def glyph_annotation_review_recipe(dataset, jsonl_file):
    logging.info(f"dataset:{dataset}, jsonl_file_path:{jsonl_file}")
    blocks = [
        {
            "view_id": "image_manual",
            "labels": ["Base Line", "Glyph"]
        },
        {"view_id": "html"},
    ]
    return {
        "dataset": dataset,
        "stream": stream_from_jsonl(jsonl_file),
        "view_id": "blocks",
        "config": {
            "blocks": blocks
        }
    }


def get_obj_key(image_url):
    parts = image_url.split("/")
    obj_key = "/".join(parts[4:8]).split("?")[0]
    decoded_key = urllib.parse.unquote(obj_key)
    return decoded_key


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
            eg = {}
            if "spans" not in line:
                continue
            if "answer" in line:
                if line["answer"] == "ignore":
                    continue
            image_id = line["id"]
            text = image_id.split("_")[0]
            obj_key = get_obj_key(line["image"])
            image_url = get_new_url(obj_key)
            spans = line["spans"]
            html = f"<p style='font-size: 10em;'>{text}</p>"
            eg = {"id": image_id, "image": image_url, "spans": spans, "html":html}
            yield set_hashes(eg, input_keys=("id"))