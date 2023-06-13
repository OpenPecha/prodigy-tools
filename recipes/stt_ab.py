import logging
import prodigy
import jsonlines
# log config 
# logging.basicConfig(
#     filename="/usr/local/prodigy/logs/stt_ab.log",
#     format="%(levelname)s: %(message)s",
#     level=logging.INFO,
#     )

# Prodigy has a logger named "prodigy" according to 
# https://support.prodi.gy/t/how-to-write-log-data-to-file/1427/10
# prodigy_logger = logging.getLogger('prodigy')
# prodigy_logger.setLevel(logging.INFO)

with open('recipes/js/auto.js') as txt:
    script_text = txt.read()

@prodigy.recipe("stt-ab-recipe")
def stt_ab_recipe(dataset, jsonl_file):
    # logging.info(f"dataset:{dataset}, jsonl_file_path:{jsonl_file}")
    blocks = [
        {"view_id": "audio"},
        {
            "view_id": "text_input",
            "field_rows": 6,
            "field_label": "Transcript",
            "field_id": "transcript",
            "field_autofocus": True,
        }, 
        {
            "view_id": "html",
            "html_template" : "<button style='margin: 5px;' onclick='window.wavesurfer.setPlaybackRate(0.5)'>0.5x speed</button><button style='margin: 5px;' onclick='window.wavesurfer.setPlaybackRate(0.7)'>0.7x speed</button><button style='margin: 5px;' onclick='window.wavesurfer.setPlaybackRate(1)'>1x speed</button><button style='margin: 5px;' onclick='window.wavesurfer.setPlaybackRate(1.3)'>1.3x speed</button><button style='margin: 5px;' onclick='window.wavesurfer.setPlaybackRate(1.5)'>1.5x speed</button>"
        }
    ]
    
  
    stream=stream_from_jsonl(jsonl_file)
    return {
        "dataset": dataset,
        "stream": stream,
        "view_id": "blocks",
        "config": {
            "title":"Pecha Tools",
            "blocks": blocks,
            "editable": True,
            "javascript":script_text,
        }
    }

def stream_from_jsonl(jsonl_file, dataset):
    # Connect to the SQLite database (replace 'my_database.db' with your database name)
    conn = sqlite3.connect('my_database.db')
    cursor = conn.cursor()

    with jsonlines.open(jsonl_file) as reader:
        for line in reader:
            audio_id = line["id"]
            audio_url = line["audio_url"]
            transcript = line["transcript"]
            
            # Check if the ID already exists in the given dataset in the database
            cursor.execute(
                f"""
                SELECT COUNT(*)
                FROM example
                JOIN link ON example.rowid = link.example_id
                JOIN dataset ON link.dataset_id = dataset.id
                WHERE dataset.name = '{dataset}' AND json_extract(example.content, '$.id') = '{line["id"]}'
                """, 
                (dataset, audio_id)
            )
            count = cursor.fetchone()[0]

            if count == 0:
                # If the ID is not in the dataset, yield this line
                yield {"id": audio_id, "audio": audio_url, "transcript": transcript}

    # Don't forget to close the connection when you're done
    conn.close()
