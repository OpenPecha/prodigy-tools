import random
import re
from pathlib import Path

from tools.config import PAGE_CROPPING_BUCKET, page_cropping_s3_client
from tools.utils import list_obj_keys

s3_client = page_cropping_s3_client

def get_images_keys():
    obj_keys = []
    prefix = f"NLM1/"
    obj_keys = list_obj_keys(prefix=prefix, s3_client=s3_client, bucket_name=PAGE_CROPPING_BUCKET)
    return obj_keys


def create_NLM1_images_txt():
    all_keys = ''
    images_key = get_images_keys()
    for key in images_key:
        all_keys += key+"\n"
    Path(f"./NLM1_images.txt").write_text(all_keys, encoding='utf-8')

def seperate_keys(keys):
    not_images = ""
    raw_images = ""
    images = ""
    preprocessed = ""
    extentions = []
    for key in keys:
        extention = (key.split("/")[-1]).split(".")[-1]
        if extention in ["db", "DS_Store","info", "txt", "pdf", "xmp", "ini", "bmp" "doc", "gz"]:
            not_images += key+"\n"
        elif extention == "CR2":
            raw_images += key+"\n"
        elif extention in ["jpg", "png"]:
            if (key.split("/")[-1]).split(".")[-2][-3:] == "_19":
                preprocessed += key+"\n"
            else:
                images += key+"\n"
        if extention not in extentions:
            extentions.append(extention)
            extentions = list(set(extentions))
    print(extentions)
    Path("./NLM1/preprocessed_NLM1.txt").write_text(preprocessed,encoding='utf-8')
    Path("./NLM1/raw_images.txt").write_text(raw_images,encoding='utf-8')
    Path("./NLM1/not_images.txt").write_text(not_images,encoding='utf-8')
    Path("./NLM1/images.txt").write_text(images,encoding='utf-8')

if __name__ == "__main__":
    keys = (Path(f"./NLM1/NLM1_images.txt").read_text(encoding='utf-8')).splitlines()
    seperate_keys(keys)