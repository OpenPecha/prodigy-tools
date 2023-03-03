from tools.config import PAGE_CROPPING_BUCKET, page_cropping_s3_client
from tools.utils import get_base_directories, list_obj_keys

s3_client = page_cropping_s3_client

def get_all_s3_keys_from_bucket():
    curr = {}
    obj_keys = []
    final_dict = {}
    base_directories = get_base_directories(s3_client=s3_client, bucket_name=PAGE_CROPPING_BUCKET)
    for base_dir in base_directories:
        prefix = (base_dir.get('Prefix'))[:-1]
        obj_keys = list_obj_keys(prefix, s3_client=s3_client, bucket_name=PAGE_CROPPING_BUCKET)
        curr[prefix] = {
            "s3_keys": obj_keys
        }
        final_dict.update(curr)
        curr = {}
    return final_dict


if __name__ == "__main__":
    s3_dict = get_all_s3_keys_from_bucket()
    

        