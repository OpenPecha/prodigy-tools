import os
import math
import json
import hashlib
import io
import boto3
import botocore
import logging
from PIL import Image
from pathlib import Path
from PIL import Image as PillowImage
from wand.image import Image as WandImage



os.environ["AWS_SHARED_CREDENTIALS_FILE"] = "~/.aws/credentials"
S3 = boto3.resource("s3")
S3_client = boto3.client("s3")
IMAGE_PROCESSING_BUCKET = "image-processing.bdrc.io"
s3_bucket = S3.Bucket(IMAGE_PROCESSING_BUCKET)


# logging config
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
formatter = logging.Formatter("%(asctime)s, %(levelname)s: %(message)s")
file_handler = logging.FileHandler("image_processing.log")
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)


class ImageProcessing():
    
    def __init__(self, vol_s3_prefix, max_height=None, max_width=None):
        self.vol_s3_prefix = vol_s3_prefix,
        self.max_height = max_height if max_height != None else 700
        self.max_width = max_width if max_width != None else 1000
        self.degree = self.get_degree()
        self.s3_image_paths = []
        self.origfilename = None
        self.new_filename = None
        self.output_s3_path = self.create_output_s3_path()
        
        
    def get_degree(self):
        angle = math.atan2(self.max_height, self.max_width)
        degree = math.degrees(angle)
        return degree

    
    def create_output_s3_path(self):
        prefix = list(self.vol_s3_prefix.split("/"))
        work_id = prefix[1]
        vol_folder = prefix[3]
        
        # md5 = hashlib.md5(str.encode(work_id))
        # two = md5.hexdigest()[:2]
        
        output_s3_path = "NLM1" / work_id / "archive-web" / vol_folder
        return output_s3_path
        
        
    def upload_image(self, image):
        self.get_new_filename()
        s3_key = self.output_s3_path / self.new_filename
        s3_bucket.put_object(Key=s3_key, Body=image)
    

    def get_s3_image_paths(self):
        
        response = S3_client.list_objects_v2(Bucket=IMAGE_PROCESSING_BUCKET, Prefix=self.vol_s3_prefix)
        if response:
            for info in response['content']:
                s3_image_path = info['key']
                self.s3_image_paths.append(s3_image_path)


    def get_s3_bits(s3path, bucket):
        f = io.BytesIO()
        try:
            bucket.download_fileobj(s3path, f)
            return f
        except botocore.exceptions.ClientError as e:
            if e.response["Error"]["Code"] == "404":
                print(f"The object does not exist, {s3path}")
            else:
                raise
        return
        

    def get_new_filename(self):
        self.new_filename = f"{self.origfilename.split('.')[0]}"+ "_" + self.degree + ".jpg"


    def is_archived(self, key):
        try:
            S3_client.head_object(Bucket=IMAGE_PROCESSING_BUCKET, Key=key)
        except botocore.errorfactory.ClientError:
            return False
        return True


    def process_binary_files(self, filebits):
        pass
    
    
    def process_image(self, filebits):
        if Path(self.origfilename).suffix == "jpeg":
            pass
        else:
            pass
        
        
    def upload_reformated_images_for_vol(self):
        
        for s3_image_path in self.s3_image_paths:
            
            self.origfilename = s3_image_path.split("/")[-1]
            self.get_new_filename()
            s3_key = self.output_s3_path / self.new_filename
            if self.is_archived(s3_key):
                continue
            
            filebits = self.get_s3_bits(s3_image_path)
            if Path(self.origfilename).suffix in [".tif", ".tiff", ".TIF"]:
                image = self.process_binary_files(filebits)
            else:
                image = self.process_image(filebits)
            self.upload_image(image)


    def reformat_image_group_and_upload_to_s3(self):
        self.get_s3_image_paths()
        self.upload_reformated_images_for_vol()
    
    
if __name__ == "__main__":
    s3_prefix = "NLM1/W2KG208132/archive/W2KG208132-I2KG208184/"
    processor = ImageProcessing(s3_prefix)
    processor.reformat_image_group_and_upload_to_s3()
    