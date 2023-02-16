import math
import io
import gzip
import csv
from pathlib import Path
from PIL import Image
import logging
from tools.utils import upload_to_s3, create_output_s3_prefix, is_archived, get_s3_bits, update_catalog
from raw_pillow_opener import register_raw_opener


log_file = 'processing.log'
logger = logging.getLogger(__name__)
logger.setLevel(logging.ERROR)
formatter = logging.Formatter("%(asctime)s, %(levelname)s: %(message)s")
file_handler = logging.FileHandler(filename=log_file)
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)


class ImageProcessing():
    def __init__(self, image_options={}):
        self.max_height = image_options['max_height'] if 'max_height' in image_options else 700
        self.max_width = image_options['max_width'] if 'max_width' in image_options else 2000
        self.quality = image_options['quality'] if 'quality' in image_options else 75
        self.greyscale = image_options['greyscale'] if 'greyscale' in image_options else False
        self.progressive = image_options['progressive'] if 'progressive' in image_options else True
        self.degree = self.get_degree()
        self.origfilename = None
        self.new_filename = None
        self.output_s3_prefix = ""
        
        
    def get_degree(self):
        angle = math.atan2(self.max_height, self.max_width)
        degree = math.degrees(angle)
        return int(degree)
        
        
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
        upload_to_s3(image_data, s3_key)
        return s3_key
        

    def get_new_filename(self, binary):
        if binary:
            self.new_filename = self.origfilename + "_" + str(self.degree) + ".png"
        else:
            self.new_filename = self.origfilename + "_" + str(self.degree) + ".jpg"


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
            if self.greyscale:
                resized_image = resized_image.convert("L")
            new_image = self.compress_and_encode_image(resized_image)
            return new_image
        return      

        
    def processs_image(self, filebits):
        # resize, compress and encode the image and return a processed image
        if filebits:
            if self.origfilename.split(".")[-1] == "CR2":
                register_raw_opener()
                image = Image.open(filebits)
            elif self.origfilename.split(".")[-1] == "gz":
                decompressed_data = gzip.decompress(filebits.getvalue())
                image_bytes = io.BytesIO(decompressed_data)
                image = Image.open(image_bytes)
                self.origfilename = self.origfilename[:-3]
            else:
                image = Image.open(filebits)
        else:
            return
            
        if image.mode == '1':
            self.get_new_filename(True)
            s3_key = f"{self.output_s3_prefix}/{self.new_filename}"
            if is_archived(s3_key):
                return
            image =  self.resize_the_image(image)
        else:
            self.get_new_filename(False)
            s3_key = f"{self.output_s3_prefix}/{self.new_filename}"
            if is_archived(s3_key):
                return
            image = self.process_non_binary_file(image)
        return image
    

    def processed_and_upload_image_to_s3(self, s3_image_key, csv_name):
        self.output_s3_prefix = create_output_s3_prefix(s3_prefix=s3_image_key)
        self.origfilename = s3_image_key.split("/")[-1]
        filebits, error = get_s3_bits(s3_image_key)
        if filebits == None:
            if error.response["Error"]["Code"] == "404":
                logger.exception(f"The object does not exist: s3__key: {s3_image_key}")
            else:
                logger.exception(f"The object didn't download due to error {error}: s3__key: {s3_image_key}")
                return
        processed_image = self.processs_image(filebits)
        if processed_image:
            s3_key = self.upload_image(processed_image)
            update_catalog(s3_key, csv_name)

    
if __name__ == "__main__":
    input_s3_prefixs = (Path(f"./data/layout_analysis/sample_images.txt").read_text(encoding='utf-8')).splitlines()
    for input_s3_prefix in input_s3_prefixs:
        processor = ImageProcessing()
        processor.processed_and_upload_image_to_s3(input_s3_prefix, "layout_analysis")