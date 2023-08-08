
import logging
import prodigy
import jsonlines
from tools.diff import Diff
import base64
from prodigy import set_hashes
# log config 
logging.basicConfig(
    filename="/usr/local/prodigy/logs/color_diff.log",
    format="%(levelname)s: %(message)s",
    level=logging.INFO,
    )

# Prodigy has a logger named "prodigy" according to 
# https://support.prodi.gy/t/how-to-write-log-data-to-file/1427/10
prodigy_logger = logging.getLogger('prodigy')
prodigy_logger.setLevel(logging.INFO)

@prodigy.recipe("stt-review-recipe")
def color_diff_recipe(dataset, jsonl_file):
    blocks =[
        {"view_id": "audio"},
        {
            "view_id": "text_input",
            "field_label": "Transcript",
            "field_id": "transcript",
            "field_autofocus": True,
        },
        {
            "view_id": "html",
            "html_template" : "<button style='margin: 5px;' onclick='window.wavesurfer.setPlaybackRate(0.5)'>0.5x speed</button><button style='margin: 5px;' onclick='window.wavesurfer.setPlaybackRate(0.7)'>0.7x speed</button><button style='margin: 5px;' onclick='window.wavesurfer.setPlaybackRate(1)'>1x speed</button><button style='margin: 5px;' onclick='window.wavesurfer.setPlaybackRate(1.3)'>1.3x speed</button><button style='margin: 5px;' onclick='window.wavesurfer.setPlaybackRate(1.5)'>1.5x speed</button>"
        }
    ]
    return {
        "dataset": dataset,
        "stream": stream_from_jsonl(jsonl_file),
        "view_id": "blocks",
        "config": {
            "blocks": blocks,
            "editable": True,
        }
    }

def stream_from_jsonl(jsonl_file):
    with jsonlines.open(jsonl_file) as reader:
        for line in reader:
            audio_id = line["text"]
            audio_path = line["audio"]
            transcript = line["transcript"]
            audio_file = open(audio_path, 'rb')
            audio_64 = base64.b64encode(audio_file.read())
            yield set_hashes({"audio": f"data:audio/*;base64,{audio_64.decode('utf-8')}", "text": audio_id, "path": audio_path, "transcript": transcript}, input_keys=("text"))
