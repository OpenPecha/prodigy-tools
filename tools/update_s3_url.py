import argparse
import json
import sqlite3


def update_db(db_path):
    conn = sqlite3.connect(db_path)
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

def update_url(prev_url, s3_client):
    if "iiif" in prev_url:
        return prev_url
    url_contents = (prev_url.split("?")[0]).split("/")
    bucket_name = url_contents[3]
    obj_key = '/'.join(url_contents[4:])

    new_url = s3_client.generate_presigned_url(
            ClientMethod="get_object",
            Params={"Bucket": bucket_name, "Key": obj_key},
            ExpiresIn=604800
        )
    return new_url

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("db_path", help="Path to the SQLite database")
    args = parser.parse_args()
    update_db(args.db_path)