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

def compress_image(im):
    compressed = im.reduce(2)
    compressed.save("Compressed_img.jpg")


if __name__ == "__main__":
    key_list = get_s3_keys()
    # print(key_list)
    # print(read_image_s3('NLM1/W2KG208132/archive/W2KG208132-I2KG208184/I2KG2081840003.tif'))
    img =read_image_s3('NLM1/W2KG208132/archive/W2KG208132-I2KG208184/I2KG2081840003.tif')
    compress_image(img)

    # get_size_format(img)
