import boto3
import botocore
import io
import os
import logging
from PIL import Image
import json
from botocore.exceptions import ClientError
from image_processing import modify_image

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
        '''Update the processed file into the image.json for the prodigy '''
        try:
            with open("images.jsonl", 'a') as file:
                json.dump({"image" : self.s3.generate_presigned_url(ClientMethod="get_object", ExpiresIn=2592000, Params= { "Bucket" : self.bucket, "Key" : key}),'type':'image/jpg'}, file, indent = 2)
        except FileNotFoundError as error:
            print(error)

    def _save_to_bucket(self, image, prefix,filename):
        '''Save the image into the bucket'''
        object_name =  f"{prefix}{filename}"        
        try:
            objects = self.s3.list_objects_v2(Bucket=self.bucket, Prefix=prefix)
            destination_keys = [o["Key"] for o in objects["Contents"]]
            if object_name in destination_keys:
                print(f"{filename} is already in the bucket")
                return False
            else:
                response = self.s3.upload_fileobj(image,self.bucket,object_name)
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
        except KeyError as error: # this is require when no file is been uploaded to the key
            response = self.s3.upload_fileobj(image,self.bucket,object_name)
            self._update_json_file(object_name)
        return True

    def delete_from_s3(self,prefix, key):
        '''Delete the image from s3 bucket using the key'''
        s3 = boto3.client("s3")
        try:
            objects = self.s3.list_objects_v2(Bucket=self.bucket, Prefix=prefix)
            destination_keys = [o["Key"] for o in objects["Contents"]]
            if key not in destination_keys:
                print("Specified image not in the bucket")
                return False
            else:
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
        except Keyerror as error:
            print("No such key is exist")
        return True
    
    def loop_through_key(self):
        '''By using the key looping through each Image object'''
        size = len(self.key_list)
        for i in range(0,3,1):
            image = self.read_image_s3(self.key_list[i])
            modify = modify_image(image,self.key_list[i])
            modify.compress_image()
            bytes_arr =modify.save_image()
            filename = modify._rename_file()
            self._save_to_bucket(bytes_arr, "NLM1/W2KG208132/archive-web/W2KG208132-I2KG208184/",filename)
            modify.delete_image()

if __name__ == "__main__":
    object = S3_Bucket("image-processing.bdrc.io", "NLM1/W2KG208132/archive/W2KG208132-I2KG208184/")
    object.loop_through_key()

    
