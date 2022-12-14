import prodigy
from prodigy.components.loaders import Images
from prodigy.util import split_string
from typing import List, Optional
from json.decoder import JSONDecodeError
from prodigy.components.loaders import JSONL
# Load the data from a jsonl

# Recipe decorator with argument annotations: (description, argument type,
# shortcut, type / converter function called on value before it's passed to
# the function). Descriptions are also shown when typing --help.
@prodigy.recipe(
    "image.manual",
    dataset=("The dataset to use", "positional", None, str),
    source=("Path to a directory of images", "positional", None, str),
    label=("One or more comma-separated labels", "option", "l", split_string),
    exclude=("Names of datasets to exclude", "option", "e", split_string),
    darken=("Darken image to make boxes stand out more", "flag", "D", bool),
)

def image_manual(
    dataset: str,
    source: str,
    label: Optional[List[str]] = None,
    exclude: Optional[List[str]] = None,
    darken: bool = False,
):
    """
    Manually annotate images by drawing rectangular bounding boxes or polygon
    shapes on the image.
    """
    # Load a stream of images from a directory and return a generator that
    # yields a dictionary for each example in the data. All images are
    # converted to base64-encoded data URIs.
    try:
        stream = JSONL(source)
    except JSONDecodeError as error:
        print(error)
    return {
        "view_id": "image_manual",  # Annotation interface to use
        "dataset": dataset,  # Name of dataset to save annotations
        "stream": stream,  # Incoming stream of examples
        "exclude": exclude,  # List of dataset names to exclude
        "config": {  # Additional config settings, mostly for app UI
            "label": ", ".join(label) if label is not None else "all",
            "labels": label,  # Selectable label options,
            "darken_image": 0.3 if darken else 0,
        },
    }
