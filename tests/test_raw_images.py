from pathlib import Path
from tools.image_processing import ImageProcessing
from PIL import Image
from raw_pillow_opener import register_raw_opener
import gzip

def process_gz_images(s3_image_paths):
    for s3_image_path in s3_image_paths:
        processor = ImageProcessing()
        processor.origfilename = s3_image_path.split("/")[-1][:-3]
        processor.get_new_filename(False)
        filebits = processor.get_s3_bits(s3_image_path)
        with gzip.open(filebits, 'rb') as f:
            decompressed_data = f.read()
        image = Image.open(decompressed_data)
        resized_image = processor.resize_the_image(image)
        new_image = processor.compress_and_encode_image(resized_image)
        new_image.save(processor.new_filename)
        
        

def process_image_from_raw_image(s3_image_paths):
    for s3_image_path in s3_image_paths:
        processor = ImageProcessing()
        processor.origfilename = s3_image_path.split("/")[-1]
        processor.get_new_filename(False)
        filebits = processor.get_s3_bits(s3_image_path)
        register_raw_opener()
        image = Image.open(filebits)
        resized_image = processor.resize_the_image(image)
        new_image = processor.compress_and_encode_image(resized_image)
        new_image.save(processor.new_filename)
        

    

if __name__ == "__main__":
    raw_images = list(Path(f"./raw_image_list.txt").read_text(encoding='utf-8').splitlines())
    # process_gz_images(raw_images[1:3])
    process_image_from_raw_image(raw_images[6:8])