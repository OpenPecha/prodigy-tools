import csv
import io
import shutil

import botocore
from pathlib import Path
from git import Repo

def clean_dir(dir):
    if dir.is_dir():
        shutil.rmtree(str(dir))

def upload_to_s3(data, s3_key, s3_bucket):
    s3_bucket.put_object(Key=s3_key, Body=data)


def get_base_directories(s3_client, bucket_name):
    response = s3_client.list_objects_v2(Bucket=bucket_name, Prefix='', Delimiter='/')
    for content in response.get('CommonPrefixes', []):
        yield content


def list_obj_keys(prefix, s3_client, bucket_name):
    obj_keys = []
    continuation_token = None
    while True:
        if continuation_token:
            response = s3_client.list_objects_v2(Bucket=bucket_name, Prefix=prefix, ContinuationToken=continuation_token)
        else:
            response = s3_client.list_objects_v2(Bucket=bucket_name, Prefix=prefix)
        if response['Contents']:
            for obj in response['Contents']:
                obj_key = obj['Key']
                obj_keys.append(obj_key)
        continuation_token = response.get("NextContinuationToken")
        if not continuation_token:
            break
    return obj_keys


def create_output_s3_prefix(s3_prefix):
    prefix = list(s3_prefix.split("/"))
    dir_name = prefix[0]
    if dir_name == "NLM1":
        dir_name = "/".join(prefix[:2])
        _type  = prefix[2]
        remaining = "/".join(prefix[3:-1])
        output_s3_path = f"{dir_name}/{_type}-web/{remaining}"
    else:
        dir_name = "/".join(prefix[:3])
        _type  = prefix[3]
        remaining = "/".join(prefix[4:-1])
        output_s3_path = f"{dir_name}/{_type}-web/{remaining}"
    return output_s3_path


def is_archived(key, config):
    if len(config) != 0:
        s3_client = config['target_s3_client']
        bucket_name = config['target_bucket_name']
        try:
            s3_client.head_object(Bucket=bucket_name, Key=key)
        except botocore.errorfactory.ClientError:
            return False
        return True
    return False
    


def get_s3_bits(s3_key, s3_bucket):
    filebits = io.BytesIO()
    try:
        s3_bucket.download_fileobj(s3_key, filebits)
        return filebits, None
    except botocore.exceptions.ClientError as error:
        return None, error


def update_catalog(s3_key, csv_path):
    with open(f"{csv_path}",'a') as f:
        writer = csv.writer(f)
        writer.writerow([s3_key])

def get_branch(repo, branch):
    if branch in repo.heads:
        return branch
    return "master"


def download_repo(repo_name, out_path=None, branch="master"):
    pecha_url = f"https://github.com/MonlamAI/{repo_name}.git"
    out_path = Path(out_path)
    out_path.mkdir(exist_ok=True, parents=True)
    repo_path = out_path / repo_name
    Repo.clone_from(pecha_url, str(repo_path))
    repo = Repo(str(repo_path))
    branch_to_pull = get_branch(repo, branch)
    repo.git.checkout(branch_to_pull)
    return repo_path


def get_list_of_unique_images(repo_path, work_id, number_of_images):
    images_list = []
    unique_images_path = Path(f"{repo_path}/{work_id}-{number_of_images}")
    images_path_list = list(unique_images_path.iterdir())
    for images_path in images_path_list:
        images_list.append(images_path.stem)
    return images_list