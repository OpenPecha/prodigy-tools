from pathlib import Path

from tools.config import (PAGE_CROPPING_BUCKET, page_cropping_bucket,
                          page_cropping_s3_client)
from tools.image_processing import ImageProcessing
from tools.config import (BDRC_ARCHIVE_BUCKET,bdrc_archive_bucket,
                          bdrc_archive_s3_client)

bdrc_config = {
    "source_s3_client": bdrc_archive_s3_client,
    "source_s3_bucket": bdrc_archive_bucket,
    "source_bucket_name": BDRC_ARCHIVE_BUCKET,
    "target_s3_client": page_cropping_s3_client,
    "target_s3_bucket": page_cropping_bucket,
    "target_bucket_name": PAGE_CROPPING_BUCKET,
    "csv_path": "./data/page_cropping.csv"
}

NLM1_config = {
    "source_s3_client": page_cropping_s3_client,
    "source_s3_bucket": page_cropping_bucket,
    "source_bucket_name": PAGE_CROPPING_BUCKET,
    "target_s3_client": page_cropping_s3_client,
    "target_s3_bucket": page_cropping_bucket,
    "target_bucket_name": PAGE_CROPPING_BUCKET,
    "csv_path": "./data/NLM1/preprocess_NLM1.csv"
}

input_s3_prefixs = (Path(f"./data/NLM1/raw_images.txt").read_text(encoding='utf-8')).splitlines()


if __name__ == "__main__":
    processor = ImageProcessing(config=NLM1_config)
    for input_s3_prefix in input_s3_prefixs:
        processor.processed_and_upload_image_to_s3(input_s3_prefix)