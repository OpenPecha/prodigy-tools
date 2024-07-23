import logging
import prodigy
from tools.config import MONLAM_AI_OCR_BUCKET, monlam_ocr_s3_client
import spacy
from prodigy.components.loaders import JSONL

s3_client = monlam_ocr_s3_client
bucket_name = MONLAM_AI_OCR_BUCKET

# log config 
logging.basicConfig(
    filename="/usr/local/prodigy/logs/NER.log",
    format="%(levelname)s: %(message)s",
    level=logging.INFO,
    )

# Prodigy has a logger named "prodigy" according to 
# https://support.prodi.gy/t/how-to-write-log-data-to-file/1427/10
prodigy_logger = logging.getLogger('prodigy')
prodigy_logger.setLevel(logging.INFO)


nlp = spacy.load("en_core_web_sm")


@prodigy.recipe("NER-recipe")
def NER_recipe(dataset, jsonl_file):
    logging.info(f"dataset:{dataset}, jsonl_file_path:{jsonl_file}")
    stream = JSONL(jsonl_file)
    def add_tokens(stream):
        for example in stream:
            doc = nlp(example['text'])
            tokens = [{'text': token.text, 'start': token.idx, 'end': token.idx + len(token.text), 'id': i} for i, token in enumerate(doc)]
            example['tokens'] = tokens
            yield example
    
    return {
        'dataset': dataset,
        'view_id': 'ner_manual',  # Annotation interface
        'stream': add_tokens(stream),
        'config': {
            'lang': 'en',
            'labels': ['PERSON', 'ORG', 'GPE']  # Specify your labels
        }
    }
