import csv
import shutil
import hashlib
from git import Repo
from pathlib import Path
from tools.utils import list_obj_keys
from tools.config import bdrc_archive_s3_client, BDRC_ARCHIVE_BUCKET


s3_client = bdrc_archive_s3_client

def clean_dir(dir):
    if dir.is_dir():
        shutil.rmtree(str(dir))


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


def get_list_of_unique_images(repo_path, work_id, number_of_images):
    images_list = []
    unique_images_path = Path(f"{repo_path}/{work_id}-{number_of_images}")
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
        for csv_line in repos[6:]:
            work_id = csv_line[0]
            repo_name = csv_line[1]
            number_of_images = csv_line[2]
            yield repo_name, work_id, number_of_images


def sample_images_for_layout_analysis(csv_file):
    for repo_name, work_id, number_of_images in parse_csv(csv_file):
        images_s3_keys = get_image_keys(repo_name, work_id, number_of_images)
        write_unique_images_s3_keys(images_s3_keys)


if __name__ == "__main__":
    csv_file = "./data/layout_analysis/layout_analysis.csv"
    sample_images_for_layout_analysis(csv_file)