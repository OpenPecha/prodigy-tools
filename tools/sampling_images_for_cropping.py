import boto3
import os
import logging


# s3 cofig
os.environ["AWS_SHARED_CREDENTIALS_FILE"] = "~/.aws/credentials"
s3 = boto3.resource("s3")
s3_client = boto3.client("s3")

def bdrc_crop_images_recipe(dataset, bucket_name):
    obj_list = s3_client.list_objects_v2(Bucket=bucket_name, Prefix=s3_prefix)
    if not obj_list:
        logging.error("no object in s3 prefix")
        raise "no object in s3 prefix"
    obj_keys = []
    for obj in obj_list['Contents']:
        obj_key = obj['Key']
        # TODO: filter non-image files
        obj_keys.append(obj_key)
    return {
        "dataset": dataset,
        "stream": stream_from_s3(obj_keys),
        "view_id": "image_manual",
        "config": {
            "labels": ["PAGE"]
        }
    }

class GetAllContentOfBucket:
    def __init__(self, bucket_name):
        self.bucket_name = bucket_name
        self.obj_keys = []
        self.final_dict = {}

    def get_base_directories(self):
        response = s3_client.list_objects_v2(Bucket=self.bucket_name, Prefix='', Delimiter='/')
        for content in response.get('CommonPrefixes', []):
            yield content

    def list_obj_keys(self, prefix):
        response = s3_client.list_objects_v2(Bucket=self.bucket_name, Prefix=prefix)
        if response['Contents']:
            self.obj_keys = []
            for obj in response['Contents']:
                obj_key = obj['Key']
                self.obj_keys.append(obj_key)
        return self.obj_keys

    def get_s3_keys(self):
        curr = {}
        base_directories = self.get_base_directories()
        for base_dir in base_directories:
            prefix = (base_dir.get('Prefix'))[:-1]
            s3_keys = self.list_obj_keys(prefix)
            curr[prefix] = {
                "s3_keys":s3_keys
            }
            self.final_dict.update(curr)
            curr = {}
        return self.final_dict

if __name__ == "__main__":
    BUCKET_NAME = "image-processing.bdrc.io"
    content_getter = GetAllContentOfBucket(bucket_name=BUCKET_NAME)
    s3_dict = content_getter.get_s3_keys()
    

        