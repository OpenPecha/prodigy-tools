import boto3
from PIL import Image

def get_image_list(bucketname='image-processing.bdrc.io'):
    ''' From this method we will get the list of all the images from the bucket name'''
    session = boto3.Session(profile_name='jampa')
    s3 = session.resource('s3', region_name='us-east-1')

    # myBucket = s3.Bucket(bucketname)

    # for myBucketObject in myBucket.objects.all():
    #     print(myBucketObject)

    image = s3.Object(bucketname,'/NLM1/W2KG208132/archive/W2KG208132-I2KG208184/I2KG2081840003.tif')

def read_image_s3(bucketname, key):
    '''Load and show image file from s3

    Parameter
    --------

    bucketname :string      bucket name 
    key :       string      Path in s3

    '''
    session = boto3.Session(profile_name='jampa')
    s3 = session.resource('s3')

    bucket = s3.Bucket(bucketname)
    object  = bucket.Object(key)
    responese = object.get()
    file = responese['Body']
    im = Image.open(file)


if __name__ == "__main__":
    # get_image_list()
    read_image_s3('image-processing.bdrc.io','/NLM1/W2KG208132/archive/W2KG208132-I2KG208184/I2KG2081840003.tif')

    # print(dir(s3.Bucket.all))

    # for bucket in s3.buckets.all():
    #     print(bucket.name)



# # session = boto3.Session(profile_name='jampa')
# # s3 = session.resource('s3')
# response = s3.list_buckets()
# #Print out bucket name 
# for bucket in response['Buckets']:
# 	print(bucket['Name'])

# # paginator = s3.get_paginator('list_objects')
# # page_iterator = paginator.paginate(Bucket='image-processing.bdrc.io')

# # Create a reusable Paginator
# paginator = s3.get_paginator('list_objects')

# # Create a PageIterator from the Paginator
# page_iterator = paginator.paginate(Bucket='image-processing.bdrc.io')

# for page in page_iterator:
#     print(page['Contents'])