import os
import boto3
import hashlib
from pathlib import Path
from git import Repo


# s3 config
os.environ["AWS_SHARED_CREDENTIALS_FILE"] = "~/.aws/credentials"
s3 = boto3.resource("s3")
s3_client = boto3.client("s3")
BUCKET_NAME = "archive.tbrc.org"
s3_bucket = s3.Bucket(BUCKET_NAME)


def get_s3_keys_of_unique_images(unique_images, s3_images_list):
    unique_images_s3_keys = []
    for s3_image in s3_images_list:
        image_name = ((s3_image.split("/"))[-1]).split(".")[0]
        if image_name in unique_images:
            unique_images_s3_keys.append(s3_image)
    return unique_images_s3_keys


def get_s3_images_list_of_work(work_id):
    obj_keys = []
    md5 = hashlib.md5(str.encode(work_id))
    two = md5.hexdigest()[:2]
    prefix = f"Works/{two}/{work_id}/images"
    continuation_token = None
    while True:
        if continuation_token:
            response = s3_client.list_objects_v2(Bucket=BUCKET_NAME, Prefix=prefix, ContinuationToken=continuation_token)
        else:
            response = s3_client.list_objects_v2(Bucket=BUCKET_NAME, Prefix=prefix)
        if response['Contents']:
            for obj in response['Contents']:
                obj_key = obj['Key']
                obj_keys.append(obj_key)
        continuation_token = response.get("NextContinuationToken")
        if not continuation_token:
            break
    return obj_keys


def get_list_of_unique_images(repo_path):
    images_list = []
    unique_images_path = Path(f"{repo_path}/unique_images")
    images_path_list = list(unique_images_path.iterdir())
    for images_path in images_path_list:
        images_list.append(images_path.stem)
    return images_list

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


def get_unique_images_keys(repo_name, work_id):
    repo_path = download_repo(repo_name, "./")
    unique_images = get_list_of_unique_images(repo_path)
    s3_images_list = get_s3_images_list_of_work(work_id)
    unique_images_s3_keys = get_s3_keys_of_unique_images(unique_images, s3_images_list)
    
    return unique_images_s3_keys


if __name__ == "__main__":
    repo_name = "OCRtest"
    work_id = "W26071"
    unique_images_s3_keys = get_unique_images_keys(repo_name, work_id)
    print(unique_images_s3_keys)