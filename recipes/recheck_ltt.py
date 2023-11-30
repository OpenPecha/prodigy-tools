
import logging
import prodigy
from tools.config import MONLAM_AI_OCR_BUCKET, monlam_ocr_s3_client
import jsonlines
from prodigy import set_hashes


s3_client = monlam_ocr_s3_client
bucket_name = MONLAM_AI_OCR_BUCKET

# log config 
logging.basicConfig(
    filename="/usr/local/prodigy/logs/recheck_ltt.log",
    format="%(levelname)s: %(message)s",
    level=logging.INFO,
    )

# Prodigy has a logger named "prodigy" according to 
# https://support.prodi.gy/t/how-to-write-log-data-to-file/1427/10
prodigy_logger = logging.getLogger('prodigy')
prodigy_logger.setLevel(logging.INFO)

@prodigy.recipe("recheck-ltt-recipe")
def recheck_ltt_recipe(dataset, jsonl_file):
    logging.info(f"dataset:{dataset}, jsonl_file_path:{jsonl_file}")
    blocks = [
        {"view_id": "choice"},
        {"view_id": "text_input"}
        
    ]
    options = [
                {"id": 2,"text": "དབུ་ཅན།"},
                {"id": 1, "text": "དབུ་མེད།"},
                { "id": 0, "text": "others" }
    ]

    def get_obj_key(image_url):
        parts = image_url.split("/")
        obj_key = "/".join(parts[4:7]).split("?")[0]
        return obj_key


    def stream_from_jsonl(jsonl_file):
        with jsonlines.open(jsonl_file) as reader:
            for line in reader:
                if line["answer"] != "accept":
                    continue
                image_id = line["id"]
                image_url = line["image"]
                obj_key = get_obj_key(image_url)
                text = line["user_input"]
                image_url = get_new_url(obj_key)
                eg = {"id": image_id, "image": image_url, "user_input": text, "options": options}
                yield set_hashes(eg, input_keys=("id"))


    def get_new_url(image_url):
        new_image_url = s3_client.generate_presigned_url(
            ClientMethod="get_object",
            Params={"Bucket": bucket_name, "Key": image_url},
            ExpiresIn=31536000
        )
        return new_image_url

    return {
        "dataset": dataset,
        "stream": stream_from_jsonl(jsonl_file),
        "view_id": "blocks",
        "config": {
            "blocks": blocks,
            "editable": True,
            
        }
    }