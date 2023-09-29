import logging
import prodigy
from tools.config import MONLAM_AI_OCR_BUCKET, monlam_ocr_s3_client
import jsonlines
from prodigy import set_hashes


s3_client = monlam_ocr_s3_client
bucket_name = MONLAM_AI_OCR_BUCKET

# log config 
logging.basicConfig(
    filename="/usr/local/prodigy/logs/Corr1-20230809.log",
    format="%(levelname)s: %(message)s",
    level=logging.INFO,
    )

# Prodigy has a logger named "prodigy" according to 
# https://support.prodi.gy/t/how-to-write-log-data-to-file/1427/10
prodigy_logger = logging.getLogger('prodigy')
prodigy_logger.setLevel(logging.INFO)


@prodigy.recipe("Corr1-20230809-recipe")
def Corr1_20230809_recipe(dataset, jsonl_file):
    logging.info(f"dataset:{dataset}, jsonl_file_path:{jsonl_file}")
    blocks = [ 
        {"view_id": "image"},
        {"view_id": "text_input"}
    ]
    return {
        "dataset": dataset,
        "stream": stream_from_jsonl(jsonl_file),
        "view_id": "blocks",
        "config": {
            "blocks": blocks,
            "editable": True
        }
    }


def stream_from_jsonl(jsonl_file):
    with jsonlines.open(jsonl_file) as reader:
        for line in reader:
            image_id = line["id"]
            obj_key = line["image_url"]
            text = line["user_input"]
            image_url = get_new_url(obj_key)
            eg = {"id": image_id, "image": image_url, "user_input": text}
            yield set_hashes(eg, input_keys=("id"))


def get_new_url(image_url):
    new_image_url = s3_client.generate_presigned_url(
        ClientMethod="get_object",
        Params={"Bucket": bucket_name, "Key": image_url},
        ExpiresIn=31536000
    )
    return new_image_url