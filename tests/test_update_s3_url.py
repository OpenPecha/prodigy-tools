import sqlite3
import requests
import boto3
import json
from pathlib import Path

s3_client = boto3.client("s3")

def test_update_db():
    conn = sqlite3.connect('./tests/data/bdrc_crop_images.sqlite')
    cursor = conn.cursor()
    cursor.execute("SELECT id, content FROM example")
    rows = cursor.fetchall()

    for row in rows:
        id = row[0]
        content = row[1]
        content_dict = json.loads(content)
        new_url = update_url(content_dict['image'])
        content_dict['image'] = new_url
        updated_content = json.dumps(content_dict)
        cursor.execute("UPDATE example SET content = ? WHERE id = ?", (updated_content, id))

    conn.commit()
    conn.close()

def update_url(prev_url):
    url_contents = (prev_url.split("?")[0]).split("/")
    bucket_name = url_contents[3]
    obj_key = '/'.join(url_contents[4:])

    new_url = s3_client.generate_presigned_url(
            ClientMethod="get_object",
            Params={"Bucket": bucket_name, "Key": obj_key},
            ExpiresIn=604800
        )
    response = requests.get(new_url)
    assert response.status_code == "200"
    return new_url