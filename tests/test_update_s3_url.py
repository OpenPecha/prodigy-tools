import json
import sqlite3
from pathlib import Path

import boto3
import requests

from tools.config import page_cropping_s3_client
from tools.update_s3_url import update_url

db_path = f"./tests/data/inputs/bdrc_crop_images.sqlite"

def test_update_url():
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("SELECT content FROM example")
    rows = cursor.fetchall()

    for row in rows[:4]:
        content = row[0]
        content_dict = json.loads(content)
        prev_url = content_dict['image']
        new_url = update_url(prev_url, page_cropping_s3_client)
        response = requests.get(new_url)
        assert response.status_code == 200

if __name__ == "__main__":
    test_update_url()