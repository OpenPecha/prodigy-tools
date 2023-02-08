
import os
import io
import re
import json
import boto3
import random
import hashlib
from pathlib import Path
from git import Repo


# s3 config
os.environ["AWS_SHARED_CREDENTIALS_FILE"] = "~/.aws/credentials"
s3 = boto3.resource("s3")
s3_client = boto3.client("s3")
BUCKET_NAME = "image-processing.bdrc.io"
s3_bucket = s3.Bucket(BUCKET_NAME)



def get_five_random_images(work_id):
    obj_keys = []
    s3_keys = []
    keys = ""
    prefix = f"NLM1/{work_id}"
    continuation_token = None
    while True:
        if continuation_token:
            response = s3_client.list_objects_v2(Bucket=BUCKET_NAME, Prefix=prefix, ContinuationToken=continuation_token)
        else:
            response = s3_client.list_objects_v2(Bucket=BUCKET_NAME, Prefix=prefix)
        if response['Contents']:
            for obj in response['Contents']:
                obj_key = obj['Key']
                obj_keys.append(obj_key)
                keys += obj_key+"\n"
        continuation_token = response.get("NextContinuationToken")
        if not continuation_token:
            break
    Path(f"./source_keys.txt").write_text(keys, encoding='utf-8')
    if len(obj_keys) < 10:
        total = len(obj_keys)
    else:
        total = int(len(obj_keys)/2)
    numbers = get_five_random_numbers(total, (len(obj_keys)-1))
    for num in numbers:
        if len(s3_keys) == 5:
            break
        key = obj_keys[num]
        if (key.split("/"))[2] == "sources": 
            if (key.split("/"))[-1] == ".DS_Store" or (key.split("/")[-1]).split(".")[-1] in ["info", "db"]:
                continue
            elif re.search(r'\d{4}', ((key.split("/")[-1]).split(".")[0][-4:])):
                if int((key.split("/")[-1]).split(".")[0][-4:]) < 4:
                    continue
                else:
                    s3_keys.append(key)
            else:
                s3_keys.append(key)
    s3_keys = list(set(s3_keys))  
    return s3_keys


def get_five_random_numbers(total, stop):
    nums = []
    for _ in range(total):
        nums.append(random.randint(0, stop))
    return nums


if __name__ == "__main__":
    all_keys = ''
    work_ids = (Path(f"./data/page_cropping/mongolia_folders.txt").read_text(encoding="utf-8")).splitlines()
    for work_id in work_ids:
        images_key = get_five_random_images(work_id)
        if images_key:
            for key in images_key:
                all_keys += key+"\n"
    Path(f"./data/page_cropping/sample_images_batch1.txt").write_text(all_keys, encoding='utf-8')