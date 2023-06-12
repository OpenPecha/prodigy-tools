import logging
import prodigy
import sqlite3
import json

# log config
logging.basicConfig(
    filename="/usr/local/prodigy/logs/stt_ab_review.log",
    format="%(levelname)s: %(message)s",
    level=logging.INFO,
)

# Prodigy has a logger named "prodigy" according to
# https://support.prodi.gy/t/how-to-write-log-data-to-file/1427/10
prodigy_logger = logging.getLogger("prodigy")
prodigy_logger.setLevel(logging.INFO)


@prodigy.recipe("stt-ab-review-recipe")
def stt_ab_recipe(dataset, database):
    logging.info(f"dataset:{dataset}")
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
            "html_template": "<button style='margin: 5px;' onclick='window.wavesurfer.setPlaybackRate(0.5)'>0.5x speed</button><button style='margin: 5px;' onclick='window.wavesurfer.setPlaybackRate(0.7)'>0.7x speed</button><button style='margin: 5px;' onclick='window.wavesurfer.setPlaybackRate(1)'>1x speed</button><button style='margin: 5px;' onclick='window.wavesurfer.setPlaybackRate(1.3)'>1.3x speed</button><button style='margin: 5px;' onclick='window.wavesurfer.setPlaybackRate(1.5)'>1.5x speed</button>",
        },
    ]
    return {
        "dataset": str(dataset)+'_review',
        "stream": stream_from_sqlite(dataset, database),
        "view_id": "blocks",
        "config": {"blocks": blocks, "editable": True},
    }


def stream_from_sqlite(dataset, database):
    # Connect to SQLite database
    connection = sqlite3.connect(f"{database}")
    cursor = connection.cursor()

    # Fetch the content from the database
    cursor.execute(
        f"""
SELECT COUNT(*) 
FROM example 
JOIN link ON example.rowid = link.example_id 
JOIN dataset ON link.dataset_id = dataset.id 
WHERE dataset.name='{dataset}'
AND json_extract(example.content, '$.id') NOT IN (
    SELECT json_extract(example.content, '$.id') 
    FROM example 
    JOIN link ON example.rowid = link.example_id 
    JOIN dataset ON link.dataset_id = dataset.id 
    WHERE dataset.name='{dataset}_review'
)
    """
    )
    rows = cursor.fetchall()

    # Loop through each row
    for row in rows:
        # Load the JSON
        json_content = json.loads(row[1])
        audio_id = json_content["id"]
        audio_url = json_content["audio"]
        transcript = json_content["user_input"] 
        yield {"id": audio_id, "audio": audio_url, "transcript": transcript}
