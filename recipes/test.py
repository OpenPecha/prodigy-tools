import logging
import prodigy
import jsonlines

# log config 
logging.basicConfig(
    filename="/usr/local/prodigy/logs/stt_ab.log",
    format="%(levelname)s: %(message)s",
    level=logging.INFO,
    )

# Prodigy has a logger named "prodigy" according to 
# https://support.prodi.gy/t/how-to-write-log-data-to-file/1427/10
prodigy_logger = logging.getLogger('prodigy')
prodigy_logger.setLevel(logging.INFO)

with open('/usr/local/prodigy/prodigy-tools/recipes/js/index.js', 'r') as index_js:
    with open('/usr/local/prodigy/prodigy-tools/recipes/js/tribute.js', 'r') as tribute_js:
             with open('/usr/local/prodigy/prodigy-tools/recipes/js/time_stretcher.js', 'r') as time_stretcher:
                index_js_text = index_js.read()
                tribute_js_text = tribute_js.read()
                time_stretcher= time_stretcher.read()
                js_code = time_stretcher+' '+ tribute_js_text+' '+index_js_text 


with open('/usr/local/prodigy/prodigy-tools/recipes/css/style.css', 'r') as file:
    css_code = file.read()


@prodigy.recipe("test-recipe")
def test_recipe(dataset, jsonl_file):
    logging.info(f"dataset:{dataset}, jsonl_file_path:{jsonl_file}")
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
            "html_template" : "<label for='speed'><img width='20' height='20' src='https://img.icons8.com/ios/50/speed--v1.png' alt='speed'/></label><input id='speed' type='range' onchange='setplaybackrate(this.value)' min='0.5' max='1.5' step='0.1' value='1'/><span class='range-value' id='rangeValue'>1x</span>"
        }
    ]
    return {
        "dataset": dataset,
        "stream": stream_from_jsonl(jsonl_file),
        "view_id": "blocks",
        "config": {
            "blocks": blocks,
            "editable": True,
             "javascript":js_code,
             "global_css":css_code,
        }
    }

def stream_from_jsonl(jsonl_file):
    # Connect to the SQLite database (replace 'my_database.db' with your database name)

    with jsonlines.open(jsonl_file) as reader:
        for line in reader:
            audio_id = line["id"]
            audio_url = line["audio_url"]
            transcript = line["transcript"]
            # If the ID is not in the dataset, yield this line
            yield {"id": audio_id, "audio": audio_url, "url": audio_url, "transcript": transcript}

    # Don't forget to close the connection when you're done