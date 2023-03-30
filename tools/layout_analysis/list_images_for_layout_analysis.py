import csv
import hashlib
import shutil
from pathlib import Path

from tools.config import BDRC_ARCHIVE_BUCKET, bdrc_archive_s3_client
from tools.utils import list_obj_keys, download_repo, clean_dir, get_list_of_unique_images

s3_client = bdrc_archive_s3_client

def write_unique_images_s3_keys(images_s3_keys):
    file_path = Path(f"./data/layout_analysis/sample_images.txt")
    with open(file_path, "a") as file:
        file.write(images_s3_keys)
    return file_path


def get_s3_keys_of_unique_images(unique_images, s3_images_list):
    unique_images_s3_keys = ""
    for s3_image in s3_images_list:
        image_name = ((s3_image.split("/"))[-1]).split(".")[0]
        if image_name in unique_images:
            unique_images_s3_keys += s3_image+"\n"
    return unique_images_s3_keys


def get_s3_images_list_of_work(work_id):
    obj_keys = []
    md5 = hashlib.md5(str.encode(work_id))
    two = md5.hexdigest()[:2]
    prefix = f"Works/{two}/{work_id}/images"
    obj_keys = list_obj_keys(prefix=prefix, s3_client=s3_client, bucket_name=BDRC_ARCHIVE_BUCKET)
    return obj_keys


def get_image_keys(repo_name, work_id, number_of_images):
    repo_path = download_repo(repo_name, "./")
    unique_images = get_list_of_unique_images(repo_path, work_id, number_of_images)
    s3_images_list = get_s3_images_list_of_work(work_id)
    images_s3_keys = get_s3_keys_of_unique_images(unique_images, s3_images_list)
    clean_dir(repo_path)
    return images_s3_keys


def parse_csv(csv_file):
    with open(csv_file) as _file:
        repos = list(csv.reader(_file, delimiter=","))
        for csv_line in repos:
            work_id = csv_line[0]
            repo_name = csv_line[1]
            number_of_images = csv_line[2]
            yield repo_name, work_id, number_of_images


def sample_images_for_layout_analysis(csv_file):
    for repo_name, work_id, number_of_images in parse_csv(csv_file):
        images_s3_keys = get_image_keys(repo_name, work_id, number_of_images)
        write_unique_images_s3_keys(images_s3_keys)


if __name__ == "__main__":
    csv_file = "./data/layout_analysis/repos.csv"
    sample_images_for_layout_analysis(csv_file)