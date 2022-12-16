import os
import math
import io
import boto3
import botocore
import logging
from PIL import Image
from pathlib import Path
import mozjpeg_lossless_optimization
from PIL.JpegImagePlugin import JpegImageFile



os.environ["AWS_SHARED_CREDENTIALS_FILE"] = "~/.aws/credentials"
s3 = boto3.resource("s3")
s3_client = boto3.client("s3")
IMAGE_PROCESSING_BUCKET = "image-processing.bdrc.io"
s3_bucket = s3.Bucket(IMAGE_PROCESSING_BUCKET)


# logging config
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
formatter = logging.Formatter("%(asctime)s, %(levelname)s: %(message)s")
file_handler = logging.FileHandler("image_processing.log")
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)


class ImageProcessing():
    
    def __init__(self, input_s3_prefix=None, image_options={}):
        
        self.max_height = image_options['max_height'] if 'max_height' in image_options else 700
        self.max_width = image_options['max_width'] if 'max_width' in image_options else 1000
        self.quality = image_options['quality'] if 'quality' in image_options else 75
        self.greyscale = image_options['greyscale'] if 'greyscale' in image_options else False
        self.degree = self.get_degree()
        self.s3_image_paths = []
        self.origfilename = None
        self.new_filename = None
        self.input_s3_prefix = input_s3_prefix
        self.output_s3_prefix = []
        
        
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
        self.get_new_filename()
        s3_key = self.output_s3_path / self.new_filename
        s3_bucket.put_object(Key=s3_key, Body=image)
    

    def get_s3_image_paths(self):
        
        response = s3_client.list_objects_v2(Bucket=IMAGE_PROCESSING_BUCKET, Prefix=self.input_s3_prefix)
        if response:
            for info in response['Contents']:
                s3_image_path = info['Key']
                self.s3_image_paths.append(s3_image_path)


    def get_s3_bits(self,s3path,):
        f = io.BytesIO()
        try:
            s3_bucket.download_fileobj(s3path, f)
            return f
        except botocore.exceptions.ClientError as e:
            if e.response["Error"]["Code"] == "404":
                print(f"The object does not exist, {s3path}")
            else:
                raise
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

    
    def process_non_binary_file(self, image):
        
        #resize the image
        resized_image = self.resize_the_image(image)
        # running configurable compression on image
        if self.greyscale:
            resized_image = resized_image.convert("L")
        image_data = resized_image.tobytes()
        image_bytes = io.BytesIO(image_data)
        compressed_image = JpegImageFile.convert(image_bytes, quality=self.quality)
        # encoding the jpeg file
        output_jpeg_bytes = mozjpeg_lossless_optimization.optimize(compressed_image)
        return output_jpeg_bytes       
        
    def upload_reformated_images_for_vol(self):
        
        for s3_image_path in self.s3_image_paths:
            self.origfilename = s3_image_path.split("/")[-1]
            
            s3_key = f"{self.output_s3_prefix}/{self.new_filename}"
            
            if self.is_archived(s3_key):
                continue
            filebits = self.get_s3_bits(s3_image_path)
            image = Image.open(filebits)
            
            if image.mode == '1':
                self.get_new_filename(True)
                image =  self.resize_the_image(image)
            else:
                self.get_new_filename(False)
                image = self.process_non_binary_file(image)
            image.save(self.new_filename)
            # self.upload_image(image)


    def reformat_image_group_and_upload_to_s3(self, input_s3_prefix):
        if self.input_s3_prefix == None:
            self.input_s3_prefix = input_s3_prefix
        self.output_s3_prefix = self.create_output_s3_prefix()
        self.get_s3_image_paths()
        self.upload_reformated_images_for_vol()
    
    
if __name__ == "__main__":
    image_options = {}
    input_s3_prefix = "NLM1/W2KG208132/archive/W2KG208132-I2KG208184/"
    processor = ImageProcessing()
    processor.reformat_image_group_and_upload_to_s3(input_s3_prefix)
    