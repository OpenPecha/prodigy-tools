import boto3
import os


# s3 cofig
os.environ["AWS_SHARED_CREDENTIALS_FILE"] = "~/.aws/credentials"
s3 = boto3.resource("s3")
s3_client = boto3.client("s3")


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
        continuation_token = None
        while True:
            if continuation_token:
                response = s3_client.list_objects_v2(Bucket=BUCKET_NAME, Prefix=prefix, ContinuationToken=continuation_token)
            else:
                response = s3_client.list_objects_v2(Bucket=BUCKET_NAME, Prefix=prefix)
            if response['Contents']:
                for obj in response['Contents']:
                    obj_key = obj['Key']
                    self.obj_keys.append(obj_key)
                    keys += obj_key+"\n"
            continuation_token = response.get("NextContinuationToken")
            if not continuation_token:
                break


    def get_s3_keys(self):
        curr = {}
        base_directories = self.get_base_directories()
        for base_dir in base_directories:
            prefix = (base_dir.get('Prefix'))[:-1]
            self.list_obj_keys(prefix)
            curr[prefix] = {
                "s3_keys": self.obj_keys
            }
            self.final_dict.update(curr)
            curr = {}
        return self.final_dict


if __name__ == "__main__":
    BUCKET_NAME = "image-processing.bdrc.io"
    content_getter = GetAllContentOfBucket(bucket_name=BUCKET_NAME)
    s3_dict = content_getter.get_s3_keys()
    

        