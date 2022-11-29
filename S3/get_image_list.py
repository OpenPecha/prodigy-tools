import boto3
import botocore
import io
import logging
from PIL import Image

logging.basicConfig(level=logging.INFO)

SESSSION = boto3.Session(profile_name='imageprocessing')
S3 = SESSSION.client('s3')
BUCKET_NAME = "image-processing.bdrc.io"

def get_s3_keys(prefix=""):
    l = S3.list_objects_v2(Bucket=BUCKET_NAME, Prefix=prefix)
    keys = [o["Key"] for o in l["Contents"]]
    return sorted(keys)

def gets3blob(s3Key):
    f = io.BytesIO()
    try:
        S3.download_fileobj(BUCKET_NAME, s3Key, f)
        return f
    except botocore.exceptions.ClientError as e:
        if e.response['Error']['Code'] == '404':
            logging.info("cannot find s3 key %s", s3Key)
            return None
        else:
            raise

def read_image_s3(s3Key):
    bbuf = gets3blob(s3Key)
    if bbuf is None:
        return None
    return Image.open(bbuf)


if __name__ == "__main__":
    #print(get_s3_keys())
    print(read_image_s3('NLM1/W2KG208132/archive/W2KG208132-I2KG208184/I2KG2081840003.tif'))
