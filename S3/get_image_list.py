import boto3
import botocore
import io
import os
import logging
from PIL import Image

logging.basicConfig(level=logging.INFO)

SESSSION = boto3.Session(profile_name='imageprocessing')
S3 = SESSSION.client('s3')
BUCKET_NAME = "image-processing.bdrc.io"
list_compressed_img = []


def get_s3_keys(prefix=""):
    '''Get the keys of all the object in the bucket'''
    l = S3.list_objects_v2(Bucket=BUCKET_NAME, Prefix=prefix)
    keys = [o["Key"] for o in l["Contents"]]
    return sorted(keys)



def gets3blob(s3Key):
    '''Get the blob image object by giving the key'''
    f = io.BytesIO()
    try:
        S3.download_fileobj(BUCKET_NAME, s3Key, f)
        return f
    except botocore.exceptions.ClientError as e:  # type: ignore
        if e.response['Error']['Code'] == '404':
            logging.info("cannot find s3 key %s", s3Key)
            return None
        else:
            raise



def read_image_s3(s3Key):
    '''Read the image in PIL Image class'''
    bbuf = gets3blob(s3Key)
    if bbuf is None:
        return None
    return Image.open(bbuf)



def compress_image(im):
    '''Compress the image'''
    compressed = im.reduce(2)
    list_compressed_img.append(compressed)
    return compressed


def get_filename(key):
    '''Keeping the same file name '''
    title = key.split("/")
    return title[-1]

def remove_extension_dot(filename):
    filename =filename.replace(".", "_")
    return filename

def rename_file(key):
    '''Rename the file with the extension .jpg'''
    name = get_filename(key)
    name=remove_extension_dot(name)
    print(name)
    name = name + "_2.jpg"
    return name



def evaluate_path(key):
    '''Check whether we are '''
    path_name = ["W2KG208132", "archive-web","W2KG208132-I2KG208184"]
    key_name = key.split("/")
    for i in range(len(key_name) - 1):
        if not key_name in path_name:
            return False
    else:
        compressed = compress_image(key)
        name =rename_file(key)
        return (compressed, name)

def loop_key(key_list):
    '''Loop through the key list'''
    for i in range(len(key_list)):
        evaluate_path(key_list[i])


def save_img(image,name):
    '''Save the image with the file name '''
    try: 
        img = image.save(name, format="JPEG")
        return img
    except ValueError as e:
        print(e)


def del_img(filename):
    '''Delete the file after prodigy has reading the data'''
    path = os.getcwd()+"/"+filename
    if os.path.exists(path):
        os.remove(filename)
    else:
        print("File not exist")
    

if __name__ == "__main__": 
    # key_list = get_s3_keys(prefix="NLM1")
    # print("Total Keys : ", len(key_list))
    # n=500
    # print(key_list[n])
    # print(evaluate_path(key_list[n]))
    image = read_image_s3('NLM1/W2KG208132/archive/W2KG208132-I2KG208184/I2KG2081840003.tif')
    filename =rename_file('NLM1/W2KG208132/archive/W2KG208132-I2KG208184/I2KG2081840003.tif')
    image =compress_image(image)
    image = save_img(image,filename)
    del_img(filename)

    # get_size_format(img)
