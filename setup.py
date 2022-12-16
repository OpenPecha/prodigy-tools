from setuptools import find_packages, setup

setup(
    name="img2opf",
    version="0.0.1",
    packages=find_packages(),
    install_requires=[
        "boto3>=1.24.50, <2.0",
        "mozjpeg-lossless-optimization>=1.0, <1.1.2",
        "Pillow>=8.4.0, <9.0",
    ],
)
