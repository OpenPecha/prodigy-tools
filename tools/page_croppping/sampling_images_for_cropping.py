import boto3
import os
from tools.utils import list_obj_keys, get_base_directories
from tools.config import s3_client1, PAGE_CROPPPING_BUCKET


def get_all_s3_keys_from_bucket():
    curr = {}
    obj_keys = []
    final_dict = {}
    base_directories = get_base_directories(s3_client=s3_client1, bucket_name=PAGE_CROPPPING_BUCKET)
    for base_dir in base_directories:
        prefix = (base_dir.get('Prefix'))[:-1]
        obj_keys = list_obj_keys(prefix, s3_client=s3_client1, bucket_name=PAGE_CROPPPING_BUCKET)
        curr[prefix] = {
            "s3_keys": obj_keys
        }
        final_dict.update(curr)
        curr = {}
    return final_dict


if __name__ == "__main__":
    s3_dict = get_all_s3_keys_from_bucket()
    

        