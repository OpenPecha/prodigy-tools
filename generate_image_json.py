import boto3
import botocore
import io
import os
import logging
from PIL import Image
import json
from prodigy.util import img_to_b64_uri
from botocore.exceptions import ClientError

class S3_Bucket:
    def __init__(self, bucket, prefix=None):
        # self.session = boto3.Session('imageprocessing')
        self.s3 = boto3.client('s3')
        self.bucket = bucket
        self.prefix = prefix
        self.key_list = self._get_key_list()
    
    def _get_key_list(self):
        '''This function will get all the key from s3 bucket'''
        if self.prefix is not None:
            l = self.s3.list_objects_v2(Bucket=self.bucket, Prefix=self.prefix)
        else:
            l = self.s3.list_objects_v2(Bucket=self.bucket)
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
    
    def _update_json_file(self, key):
        try:
            with open("images.jsonl", 'a') as file:
                json.dump({"image" : self.s3.generate_presigned_url(ClientMethod="get_object", ExpiresIn=2592000, Params= { "Bucket" : self.bucket, "Key" : key}),'type':'image/jpg'}, file)
        except FileNotFoundError as error:
            print(error)

    def _save_to_bucket(self, image, prefix,filename):
        object_name =  f"{prefix}{filename}"        
        try:
            response = self.s3.upload_file(filename,self.bucket,object_name)
            self._update_json_file(object_name)
        except ClientError as error:
            print(error)
            return False
        except FileNotFoundError as error:
            print(error)
            return False
        except ValueError as error:
            print(error)
            return False
        return True

    def delete_from_s3(self, key):
        s3 = boto3.client("s3")
        try:
            response = s3.delete_object(Bucket=self.bucket,Key=key)
        except ClientError as error:
            print(error)
            return False
        except FileNotFoundError as error:
            print(error)
            return False
        except ValueError as error:
            print(error)
            return False
        return True
    
    def loop_through_key(self):
        '''By using the key looping through each Image object'''
        size = len(self.key_list)
        for i in range(0,2,1):
            image = self.read_image_s3(self.key_list[i])
            modify = modify_image(image,self.key_list[i])
            modify.compress_image()
            filename =modify.save_image()
            self._save_to_bucket(modify.image, "NLM1/W2KG208132/archive-web/W2KG208132-I2KG208184/",filename)
            modify.delete_image()


class modify_image:
    '''Different operation onto an individual image'''
    def __init__(self, im, key, degree=2):
        self.image = im
        self.key = key
        self.degree = degree
    
    def compress_image(self):
        self.image.resize((self.image.size[0]//self.degree, self.image.size[1]//self.degree))
    
    def _get_title(self):
        title = self.key.split('/')
        return title[-1]
    
    def _remove_extension_dot(self,title):
        return title.replace(".", "_")
    
    def _rename_file(self):
        '''Rename the file to with the extension .jpg'''
        name = self._get_title()
        name = self._remove_extension_dot(name)
        name = f"{name}_{self.degree}.jpg"
        return name
    
    def save_image(self):
        '''Save the image with changed fileName'''
        try:
            filename = self._rename_file()
            img = self.image.save(filename)
            return filename
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
        
    
    


    

if __name__ == "__main__":
    object = S3_Bucket("image-processing.bdrc.io", "NLM1/W2KG208132/archive/W2KG208132-I2KG208184/")
    object.loop_through_key()

    
