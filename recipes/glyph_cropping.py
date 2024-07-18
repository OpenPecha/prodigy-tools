import logging
import prodigy
from tools.config import MONLAM_AI_OCR_BUCKET, monlam_ocr_s3_client
import jsonlines
from prodigy import set_hashes


s3_client = monlam_ocr_s3_client
bucket_name = MONLAM_AI_OCR_BUCKET

# log config 
logging.basicConfig(
    filename="/usr/local/prodigy/logs/Corr1-review.log",
    format="%(levelname)s: %(message)s",
    level=logging.INFO,
    )

# Prodigy has a logger named "prodigy" according to 
# https://support.prodi.gy/t/how-to-write-log-data-to-file/1427/10
prodigy_logger = logging.getLogger('prodigy')
prodigy_logger.setLevel(logging.INFO)

@prodigy.recipe("glyph-cropping-recipe")
def glyph_cropping_recipe(dataset, jsonl_file):
    logging.info(f"dataset:{dataset}, jsonl_file_path:{jsonl_file}")
    blocks = [
        {
            "view_id": "image_manual",
            "labels": ["Ch-1", "Ch-2", "Ch-3", "Ch-4"]
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


def stream_from_jsonl(jsonl_file):
    with jsonlines.open(jsonl_file) as reader:
        for line in reader:
            image_id = line["id"]
            image = line["image"]
            text = line["text"]
            line_info = line['line_info']
            image_url = f"https://s3.amazonaws.com/monlam.ai.ocr/{image}"
            html = f"<p style='font-size: 3em;'>{text}</p> <p style='font-size: 1em;'> Refer Lines {line_info}</p>"
            eg = {"id": image_id, "image": image_url, 'html':html }
            yield set_hashes(eg, input_keys=("id"))