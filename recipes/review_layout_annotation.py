
import csv
import json
import logging
import sqlite3

import prodigy

from tools.config import LAYOUT_ANALYSIS_BUCKET, layout_analysis_s3_client

#s3 config
s3_client = layout_analysis_s3_client
bucket_name = LAYOUT_ANALYSIS_BUCKET

# log config 
logging.basicConfig(
    filename="/usr/local/prodigy/logs/layout_analysis.log",
    format="%(levelname)s: %(message)s",
    level=logging.INFO,
    )

# Prodigy has a logger named "prodigy" according to 
# https://support.prodi.gy/t/how-to-write-log-data-to-file/1427/10
prodigy_logger = logging.getLogger('prodigy')
prodigy_logger.setLevel(logging.INFO)

@prodigy.recipe("review-layout-annotation-recipe")
def review_layout_annotation_recipe(dataset, db_path):
    logging.info(f"dataset: {dataset}, db_path: {db_path}")
    return {
        "dataset": dataset,
        "stream": get_stream_from_sqlite(db_path),
        "view_id": "image_manual"
    }


def get_stream_from_sqlite(db_path):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("SELECT id, content FROM example")
    rows = cursor.fetchall()

    for row in rows:
        id = row[0]
        content = row[1]
        content_dict = json.loads(content)
        spans = content_dict['spans']
        new_url = get_new_url(content_dict['image'])
        yield  {"id": id,"image": new_url, "spans": spans}


def get_new_url(image_url):
    key = "/".join(image_url.split("?")[0].split("/")[4:])
    new_image_url = s3_client.generate_presigned_url(
        ClientMethod="get_object",
        Params={"Bucket": bucket_name, "Key": key},
        ExpiresIn=31536000
    )
    return new_image_url