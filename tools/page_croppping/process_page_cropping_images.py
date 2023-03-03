from pathlib import Path

from tools.config import (PAGE_CROPPING_BUCKET, page_cropping_bucket,
                          page_cropping_s3_client)
from tools.image_processing import ImageProcessing

_config = {
    "source_s3_client": page_cropping_s3_client,
    "source_s3_bucket": page_cropping_bucket,
    "source_bucket_name": PAGE_CROPPING_BUCKET,
    "target_s3_client": page_cropping_s3_client,
    "target_s3_bucket": page_cropping_bucket,
    "target_bucket_name": PAGE_CROPPING_BUCKET,
    "csv_name": "page_cropping"
}

input_s3_prefixs = (Path(f"./data/page_cropping/sample_images_batch1.txt").read_text(encoding='utf-8')).splitlines()


if __name__ == "__main__":
    processor = ImageProcessing(config=_config)
    for input_s3_prefix in input_s3_prefixs:
        processor.processed_and_upload_image_to_s3(input_s3_prefix)