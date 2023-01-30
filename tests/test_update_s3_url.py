import sqlite3
import requests
import boto3
import json
from pathlib import Path
from tools.update_s3_url import update_url

s3_client = boto3.client("s3")

db_path = f"./tests/data/bdrc_crop_images.sqlite"

def test_update_url():
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("SELECT content FROM example")
    rows = cursor.fetchall()

    for row in rows:
        content = row[0]
        content_dict = json.loads(content)
        prev_url = content_dict['image']
        new_url = update_url(prev_url)
        response = requests.get(new_url)
        assert response.status_code == 200


if __name__ == "__main__":
    test_update_url()