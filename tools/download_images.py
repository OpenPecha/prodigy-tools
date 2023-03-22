from pathlib import Path

from tools.config import (PAGE_CROPPING_BUCKET, page_cropping_bucket,
                          page_cropping_s3_client)
from tools.image_processing import ImageProcessing
from tools.utils import list_obj_keys, get_s3_bits
from PIL import Image

# config = {
#     "source_s3_client": page_cropping_s3_client,
#     "source_s3_bucket": page_cropping_bucket,
#     "source_bucket_name": PAGE_CROPPING_BUCKET,
#     "target_s3_client": page_cropping_s3_client,
#     "target_s3_bucket": page_cropping_bucket,
#     "target_bucket_name": PAGE_CROPPING_BUCKET,
#     "csv_name": "page_cropping"
# }

def download_images(key):
    file, error = get_s3_bits(key, page_cropping_bucket)
    name = key.split("/")[-1]
    if file:
        image = Image.open(file)
        image.save(f"./W3CN14289/{name}")


if __name__ == "__main__":
    prefix = "NLM1/W3CN14289/sources/"
    obj_keys = list_obj_keys(prefix=prefix, s3_client=page_cropping_s3_client, bucket_name=PAGE_CROPPING_BUCKET)
    for obj_key in obj_keys:
        name = obj_key.split("/")[-1]
        if obj_key.split("/")[2] != "sources":
            continue
        if name in ["Thumbs.db", "Picasa.ini", ".DS_Store", "7-14.psd"]:
            continue
        elif name[-4:] == ".psd":
            continue
        image_path = Path(f"./W3CN14289/{name}")
        if image_path.is_file():
            continue
        download_images(obj_key)
