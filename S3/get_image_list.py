import boto3

def get_image_list(bucketname='image-processing.bdrc.io'):
    ''' From this method we will get the list of all the images from the bucket name'''
    session = boto3.Session(profile_name='jampa')
    s3 = session.resource('s3', region_name='us-east-1')

    myBucket = s3.Bucket(bucketname)

    for myBucketObject in myBucket.objects.all():
        print(myBucketObject)
    


if __name__ == "__main__":
    get_image_list()

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