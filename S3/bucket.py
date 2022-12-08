import boto3
import botocore
import io
import os
import logging
from PIL import Image

class S3_Bucket:
    def __init__(self, bucket, prefix):
        self.session = boto3.Session('imageprocessing')
        self.s3 = self.session.client('s3')
        self.bucket = bucket
        self.prefix = prefix
        self.key_list = self._get_key_list()
        

    
    def _get_key_list(self):
        '''This function will get all the key from s3 bucket'''
        l = self.s3.list_objects_v2(Bucket=self.bucket, Prefix=self.prefix)
        keys = [o["Key"] for o in l["Contents"]]
        return sorted(keys)
    
    def _get_blob(self, key):
        '''Get the blob image object by giving the key'''
        f = io.BytesIO()
        try:
            self.s3.download_fileobj(self.bucket, key, f)
            return f
        except botocore.exceptions.ClientError as e:  # type: ignore
            if e.response['Error']['Code'] == '404':
                logging.info("cannot find s3 key %s", s3Key)
                return None
            else:
                raise
    
    def read_image_s3(self,s3Key):
        '''Read the image in PIL Image class'''
        bbuf = self._get_blob(s3Key)
        if bbuf is None:
            return None
        return Image.open(bbuf)
    
    def loop_through_key(self):
        '''By using the key looping through each Image object'''
        for i in range(len(self.key_list)):
            image = self.read_image_s3(self.key_list[i])
            modify = modify_image(image,self.key_list[i])
            modify.compress_image()
            modify.save_image()




class modify_image:
    '''Different operation onto an individual image'''
    def __init__(self, im, key, degree=2):
        self.image = im
        self.key = key
        self.degree = degree
    
    def compress_image(self):
        self.image.reduce(self.degree)
    
    def _get_title(self):
        title = self.key.split('/')
        return title[-1]
    
    def _remove_extension_dot(title):
        return title.replace(".", "_")
    
    def _rename_file(self):
        '''Rename the file to with the extension .jpg'''
        name = self._get_title()
        name = self._remove_extension_dot(name)
        name = name,"_",self.degree,".jpg"
        return name
    
    def save_image(self):
        '''Save the image with changed fileName'''
        try:
            img = self.image.save(self._rename_file(),format="JPEG")
            return img
        except ValueError as e:
            print(e)
    
    def delete_image(self):
        '''Delete the file after prodigy has reading teh data'''
        name = self._rename_file()
        path = os.getcwd()+"/"+name

        if os.path.exists(path):
            os.remove(name)
        else:
            print("File doesnt exist")
    

