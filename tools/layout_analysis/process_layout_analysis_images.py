from pathlib import Path
from tools.image_processing import ImageProcessing
from tools.config import bdrc_archive_s3_client, layout_analysis_s3_client, bdrc_archive_bucket, layout_analysis_bucket, BDRC_ARCHIVE_BUCKET, LAYOUT_ANALYSIS_BUCKET


_config = {
    "source_s3_client": bdrc_archive_s3_client,
    "source_s3_bucket": bdrc_archive_bucket,
    "source_bucket_name": BDRC_ARCHIVE_BUCKET,
    "target_s3_client": layout_analysis_s3_client,
    "target_s3_bucket": layout_analysis_bucket,
    "target_bucket_name": LAYOUT_ANALYSIS_BUCKET,
    "csv_name": "layout_analysis"
}

input_s3_prefixs = (Path(f"./data/layout_analysis/sample_images.txt").read_text(encoding='utf-8')).splitlines()


if __name__ == "__main__":
    processor = ImageProcessing(config=_config)
    for input_s3_prefix in input_s3_prefixs[220:]:
        processor.processed_and_upload_image_to_s3(input_s3_prefix)