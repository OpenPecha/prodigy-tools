from pathlib import Path
import jsonlines



def read_jsonl(jsonl_path):
    with jsonlines.open(jsonl_path) as reader:
        for line in reader:
            yield line

def create_jsonl_for_prodigy(jsonl_path):
    final_jsonl = []
    for line in read_jsonl(jsonl_path):
        image_name = line["image"]
        for span in line['spans']:
            if span['label'] == 'LINETEXT':
                text = span['text']
                line_image_id = span["id"]
                image_id = f"{(image_name.split('.'))[0]}_{line_image_id}"
                image_url = f"line_images/{image_id}.jpg"
                final_jsonl.append({"id":image_id, "image_url": image_url, "user_input": text})
    return final_jsonl

def write_jsonl(final_jsonl, jsonl_path):
    with jsonlines.open(jsonl_path, mode="w") as writer:
        writer.write_all(final_jsonl)


if __name__ == "__main__":
    jsonl_path = Path("./data/line_to_text/LhasaKanjur_batch1_3999.jsonl")
    final_jsonl = create_jsonl_for_prodigy(jsonl_path)
    write_jsonl(final_jsonl, f"./data/line_to_text/final_jsonl.jsonl")