import os
import math
import io
import boto3
import botocore
from pathlib import Path
from PIL import Image
import logging
from raw_pillow_opener import register_raw_opener

# s3 config
os.environ["AWS_SHARED_CREDENTIALS_FILE"] = "~/.aws/credentials"
s3 = boto3.resource("s3")
s3_client = boto3.client("s3")
IMAGE_PROCESSING_BUCKET = "image-processing.bdrc.io"
s3_bucket = s3.Bucket(IMAGE_PROCESSING_BUCKET)


# logging config
# log_file = "/usr/local/prodigy/logs/processing.log"
log_file = 'processing.log'
logger = logging.getLogger(__name__)
logger.setLevel(logging.ERROR)
formatter = logging.Formatter("%(asctime)s, %(levelname)s: %(message)s")
file_handler = logging.FileHandler(filename=log_file)
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)

class ImageProcessing():
    
    def __init__(self, input_s3_prefix=None, image_options={}):
        
        self.max_height = image_options['max_height'] if 'max_height' in image_options else 700
        self.max_width = image_options['max_width'] if 'max_width' in image_options else 2000
        self.quality = image_options['quality'] if 'quality' in image_options else 75
        self.greyscale = image_options['greyscale'] if 'greyscale' in image_options else False
        self.progressive = image_options['progressive'] if 'progressive' in image_options else True
        self.degree = self.get_degree()
        self.s3_image_paths = []
        self.origfilename = None
        self.new_filename = None
        self.input_s3_prefix = input_s3_prefix
        self.output_s3_prefix = []
        self.s3_upload_paths = []
        
        
    def get_degree(self):
        angle = math.atan2(self.max_height, self.max_width)
        degree = math.degrees(angle)
        return int(degree)

    
    def create_output_s3_prefix(self):
        prefix = list(self.input_s3_prefix.split("/"))
        work_id = prefix[1]
        vol_folder = prefix[3]
        
        output_s3_path = f"NLM1/{work_id}/archive-web/{vol_folder}"
        return output_s3_path
        
        
    def upload_image(self, image):
        s3_key = f"{self.output_s3_prefix}/{self.new_filename}"
        image_bytes = io.BytesIO()
        if self.new_filename.split(".")[-1] == "png":
            extention = "png"
        else:
            extention = "jpeg"
        image.save(image_bytes, extention)
        image_bytes.seek(0)
        image_data = image_bytes.read()
        s3_bucket.put_object(Key=s3_key, Body=image_data)
        self.s3_upload_paths.append(s3_key)
    

    def get_s3_image_paths(self):
        
        response = s3_client.list_objects_v2(Bucket=IMAGE_PROCESSING_BUCKET, Prefix=self.input_s3_prefix)
        if response:
            for info in response['Contents']:
                s3_image_path = info['Key']
                self.s3_image_paths.append(s3_image_path)


    def get_s3_bits(self, s3path):
        f = io.BytesIO()
        try:
            s3_bucket.download_fileobj(s3path, f)
            return f
        except botocore.exceptions.ClientError as e:
            if e.response["Error"]["Code"] == "404":
                logger.exception(f"The object does not exist: s3_path: {s3path}")
            else:
                logger.exception(f"The object didn't download due to error {e}: s3_path: {s3path}")
        return
        

    def get_new_filename(self, binary):
        if binary:
            self.new_filename = f"{self.origfilename.split('.')[0]}"+ "_" + str(self.degree) + ".png"
        else:
            self.new_filename = f"{self.origfilename.split('.')[0]}"+ "_" + str(self.degree) + ".jpg"


    def is_archived(self, key):
        try:
            s3_client.head_object(Bucket=IMAGE_PROCESSING_BUCKET, Key=key)
        except botocore.errorfactory.ClientError:
            return False
        return True

    def resize_the_image(self, image):
        try:
            width, height = image.size
            aspect_ratio = width / height

            if aspect_ratio > 1:
                # Image is wider than the maximum dimensions
                new_width = self.max_width
                new_height = int(self.max_width / aspect_ratio)
            else:
                # Image is taller than the maximum dimensions
                new_height = self.max_height
                new_width = int(self.max_height * aspect_ratio)

            resized_img = image.resize((new_width, new_height))
            return resized_img
        except Exception as e:
            logger.exception(
                f"Image corrupted can't resize, error {e}: original filename: {self.origfilename}"
            )
            return


    def compress_and_encode_image(self, resized_image):
        
        # do cofigurable compression with input quality if given else 75 and do progressive encoding
        compressed_image_bytes = io.BytesIO()
        resized_image.save(compressed_image_bytes, format='JPEG', quality=self.quality, progressive=self.progressive)

        compressed_image = Image.open(compressed_image_bytes, formats=['JPEG'])
        
        # create new image to not include the metadata of compressed image
        new_image = Image.new(mode=compressed_image.mode, size=resized_image.size)
        new_image.putdata(list(compressed_image.getdata()))
        return compressed_image
    
    
    def process_non_binary_file(self, image):
        #resize the image
        resized_image = self.resize_the_image(image)
        
        if resized_image:
            # check if greyscal option is True
            if self.greyscale:
                resized_image = resized_image.convert("L")
                
            new_image = self.compress_and_encode_image(resized_image)
            return new_image
        return      
        
        
    def upload_reformated_images_for_vol(self):
        
        for s3_image_path in self.s3_image_paths:
            self.origfilename = s3_image_path.split("/")[-1]
            # download the image file
            filebits = self.get_s3_bits(s3_image_path)
            
            if filebits:
                # to check if the image is a raw image or not and use register_raw_opener if it is a raw image
                if self.origfilename.split(".")[-1] == "CR2":
                    register_raw_opener()
                    image = Image.open(filebits)
                elif self.origfilename.split(".")[-1] == "gz":
                    continue
                else:
                    image = Image.open(filebits, formats=['JEPG'])
            else:
                continue
            
            if image.mode == '1':
                self.get_new_filename(True)
                s3_key = f"{self.output_s3_prefix}/{self.new_filename}"
                if self.is_archived(s3_key):
                    continue
                image =  self.resize_the_image(image)
            else:
                self.get_new_filename(False)
                s3_key = f"{self.output_s3_prefix}/{self.new_filename}"
                if self.is_archived(s3_key):
                    continue
                image = self.process_non_binary_file(image)

            if image:
                self.upload_image(image)

    def reformat_image_group_and_upload_to_s3(self, input_s3_prefix):
        
        if self.input_s3_prefix == None:
            self.input_s3_prefix = input_s3_prefix
        self.output_s3_prefix = self.create_output_s3_prefix()
        self.get_s3_image_paths()
        self.upload_reformated_images_for_vol()
    
    
if __name__ == "__main__":
    image_options = {}
    # input_s3_prefix = "NLM1/W2KG208132/archive/W2KG208132-I2KG208184/"
    input_s3_prefix = 'NLM1/W2KG208129/sources/W2KG208129-I2KG208175/'
    processor = ImageProcessing()
    processor.reformat_image_group_and_upload_to_s3(input_s3_prefix)