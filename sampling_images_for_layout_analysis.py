import os
import boto3
import hashlib
import requests
from pathlib import Path
from PIL import Image
import logging
import rdflib
from rdflib import URIRef, Graph
from rdflib.namespace import Namespace, NamespaceManager
from openpecha.buda.api import image_group_to_folder_name

# s3 config
os.environ["AWS_SHARED_CREDENTIALS_FILE"] = "~/.aws/credentials"
s3 = boto3.resource("s3")
s3_client = boto3.client("s3")
BUCKET_NAME = "archive.tbrc.org"
s3_bucket = s3.Bucket(BUCKET_NAME)


BDR = Namespace("http://purl.bdrc.io/resource/")
BDO = Namespace("http://purl.bdrc.io/ontology/core/")
NSM = NamespaceManager(rdflib.Graph())


def get_number_of_intro_images(imagegroup):

    ttl_response = requests.get(f"http://purl.bdrc.io/resource/{imagegroup}.ttl")
    ttl_content = ttl_response.text
    g = Graph()
    try:
        g.parse(data=ttl_content, format="ttl")
        number = int((g.value(BDR[imagegroup], BDO["volumePagesTbrcIntro"])).split("/")[-1])
        return number
    except:
        return None

def get_sample_images_s3_key(imagegroup, s3_prefix):

    sample_images_s3_keys = []
    images_list = []
    number_of_intro = get_number_of_intro_images(imagegroup)
    response = requests.get(
        f"https://iiifpres.bdrc.io/il/v:bdr:{imagegroup}"
    )
    file_json = response.json()

    if number_of_intro:
        start = number_of_intro
    else:
        start = 0

    for info in file_json[start:start+10]:
        images_list.append(info['filename'])
    for info in file_json[-10:]:
        images_list.append(info['filename'])

    for image_name in images_list:
        s3_key = f"{s3_prefix}/{image_name}"
        sample_images_s3_keys.append(s3_key)

    return sample_images_s3_keys
    

def get_s3_prefix( work_local_id, imagegroup):

    md5 = hashlib.md5(str.encode(work_local_id))
    two = md5.hexdigest()[:2]

    vol_folder = image_group_to_folder_name(work_id, imagegroup)
    base_dir = f"Works/{two}/{work_local_id}"
    return f"{base_dir}/images/{vol_folder}"

def get_value(json_node):
    if json_node["type"] == "literal":
        return json_node["value"]
    else:
        return NSM.qname(URIRef(json_node["value"]))


def get_volume_infos(work_prefix_url):
    response = requests.get(
        f"http://purl.bdrc.io/query/table/volumesForWork?R_RES={work_prefix_url}&format=json&pageSize=500"
    )
    if response.status_code != 200:
        logger.error(
            f"Volume Info Error: No info found for Work {work_prefix_url}: status code: {response.status_code}"
        )
        return
    res = response.json()
    for b in res["results"]["bindings"]:
        volume_prefix_url = NSM.qname(URIRef(b["volid"]["value"]))
        yield {
            "vol_num": get_value(b["volnum"]),
            "volume_prefix_url": volume_prefix_url,
            "imagegroup": volume_prefix_url[4:],
        }

def get_sample_images_dict(work_id):
    curr ={}
    final_sample_dict = {}
    for _, vol_info in enumerate(get_volume_infos(f"bdr:{work_id}")):
        imagegroup = vol_info['imagegroup']
        s3_prefix = get_s3_prefix(work_id, imagegroup)
        sample_images_s3_key = get_sample_images_s3_key(imagegroup, s3_prefix)
        curr[imagegroup]=sample_images_s3_key
        final_sample_dict.update(curr)
        curr = {}
    return final_sample_dict

if __name__ == "__main__":
    work_id = "W00EGS1016255"
    finale_sample_dict = get_sample_images_dict(work_id)
    print(finale_sample_dict)