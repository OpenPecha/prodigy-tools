import os
import json
import io
import boto3
import botocore
import logging
from PIL import Image
from pathlib import Path
from PIL import Image as PillowImage
from wand.image import Image as WandImage



os.environ["AWS_SHARED_CREDENTIALS_FILE"] = "~/.aws/credentials"
IMAGES_BUCKET = "image-processing.bdrc.io"
S3 = boto3.resource("s3")
S3_client = boto3.client("s3")

IMAGES = 'images'

DATA_PATH = Path("./archive")
IMAGES_BASE_DIR = DATA_PATH / IMAGES


# logging config
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
formatter = logging.Formatter("%(asctime)s, %(levelname)s: %(message)s")
file_handler = logging.FileHandler("image_processing.log")
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)


class ImageProcessing():
    
    def __init__(self, s3_prefix, degree=None):
        self.s3_prefix = s3_prefix,
        self.degree = degree if degree != None else 2
        self.s3_images_paths = []
        self.origfilename = None
        self.new_filename = None


    def reformat_and_save_image(self, bits, origfilename, imagegroup_output_dir, binarize=False):
    
        imagegroup_output_dir.mkdir(exist_ok=True, parents=True)
        output_fn = imagegroup_output_dir / self.origfilename
        if Path(origfilename).suffix in [".tif", ".tiff", ".TIF"]:
            output_fn = imagegroup_output_dir / self.new_filename
        if output_fn.is_file():
            return
        try:
            img = PillowImage.open(bits)
        except Exception as e:
            logger.exception(f"Empty image: {output_fn}")
            return
        try:
            img.resize(img.size[0]//self.degree, img.size[1]//self.degree)
            img.save(str(output_fn))
        except:
            del img
            logger.exception(f"image couldn't saved: {output_fn}")
            return

    def get_s3_image_paths(self):
        
        response = S3_client.list_objects_v2(Bucket=IMAGES_BUCKET, Prefix=self.s3_prefix)
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


    def image_exists_locally(self, imagegroup_output_dir):
        output_fn = imagegroup_output_dir / self.new_filename
        if output_fn.is_file():
            return True
        

    def get_new_filename(self):
        self.new_filename = f"{self.origfilename.split('.')[0]}"+ "_" + self.degree + ".jpg"


    def save_reformated_images_for_vol(self):
        prefix = list(self.s3_prefix.split("/"))
        work_local_id = prefix[1]
        vol_folder = prefix[3]
        
        for s3_image_path in self.s3_image_paths:
            self.origfilename = s3_image_path.split("/")[-1]
            self.get_new_filename()
            imagegroup_output_dir = IMAGES_BASE_DIR / work_local_id / vol_folder
            if self.image_exists_locally(imagegroup_output_dir):
                continue
            filebits = self.get_s3_bits(s3_image_path, IMAGES_BUCKET)
            self.reformat_and_save_image(filebits, imagegroup_output_dir)


    def reformat_image_group(self):
        self.get_s3_image_paths()
        self.save_reformated_images_for_vol()
    
    
    
    
if __name__ == "__main__":
    s3_prefix = "NLM1/W2KG208132/archive/W2KG208132-I2KG208184/"
    processor = ImageProcessing(s3_prefix)
    processor.reformat_image_group()
    