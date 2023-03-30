from pathlib import Path

from tools.config import (PAGE_CROPPING_BUCKET, page_cropping_bucket,
                          page_cropping_s3_client)
from tools.image_processing import ImageProcessing
from tools.utils import list_obj_keys, get_s3_bits
from PIL import Image

NML1_config = {
    "source_s3_client": page_cropping_s3_client,
    "source_s3_bucket": page_cropping_bucket,
    "source_bucket_name": PAGE_CROPPING_BUCKET,
    "target_s3_client": page_cropping_s3_client,
    "target_s3_bucket": page_cropping_bucket,
    "target_bucket_name": PAGE_CROPPING_BUCKET,
    "csv_name": "page_cropping"
}

def download_images(key):
    file, error = get_s3_bits(key, page_cropping_bucket)
    name = key.split("/")[-1]
    if file:
        image = Image.open(file)
        image.save(f"./PD02/{name}")


if __name__ == "__main__":
    prefix = "NLM1/W3CN14289/sources/"
    obj_keys = (Path(f"./page_cropping.txt").read_text(encoding='utf-8')).splitlines()
    for obj_key in obj_keys:
        download_images(obj_key)
