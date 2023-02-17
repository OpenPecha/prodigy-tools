import re
import random
from pathlib import Path
from tools.utils import list_obj_keys
from tools.config import s3_client1, PAGE_CROPPPING_BUCKET


def get_five_random_images(work_id):
    obj_keys = []
    s3_keys = []
    keys = ""
    prefix = f"NLM1/{work_id}"
    obj_keys = list_obj_keys(prefix=prefix, s3_client=s3_client1, bucket_name=PAGE_CROPPPING_BUCKET)
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


def create_sample_images_txt(work_ids):
    all_keys = ''
    for work_id in work_ids:
        images_key = get_five_random_images(work_id)
        if images_key:
            for key in images_key:
                all_keys += key+"\n"
    Path(f"./data/page_cropping/sample_images_batch1.txt").write_text(all_keys, encoding='utf-8')


if __name__ == "__main__":
    work_ids = (Path(f"./data/page_cropping/mongolia_folders.txt").read_text(encoding="utf-8")).splitlines()
    create_sample_images_txt(work_ids)