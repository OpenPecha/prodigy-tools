from pathlib import Path
import boto3
import os
import io
import botocore
from tools.layout_analysis.sampling_images_for_layout_analysis import get_image_keys


expected_s3_keys = [
    'Works/56/W26071/images/W26071-4032/40320003.tif',
    'Works/56/W26071/images/W26071-4032/40320004.tif',
    'Works/56/W26071/images/W26071-4032/40320005.tif',
    'Works/56/W26071/images/W26071-4032/40320006.tif']


def test_sampling_images_for_layout_analysis():
    s3_keys = list((get_image_keys("OCRtest", "W26071", "005")).splitlines())
    assert expected_s3_keys == s3_keys

if __name__ == "__main__":
    test_sampling_images_for_layout_analysis()