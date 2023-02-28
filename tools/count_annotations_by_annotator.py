import csv
import json
import sqlite3


def count_annotator_id(db_path):
    count_dict = {}
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("SELECT id, content FROM example")
    rows = cursor.fetchall()

    for row in rows:
        content = row[1]
        content_dict = json.loads(content)
        annotator_id = content_dict['_annotator_id']
        if annotator_id in count_dict.keys():
            count = count_dict[annotator_id] + 1
            count_dict[annotator_id] = count
        else:
            count_dict[annotator_id] = 1

    return count_dict
    

def count_annotations_and_write_csv(db_path, csv_path):
    count_dict = count_annotator_id(db_path)

    for annotator_id, number_of_annotations in count_dict.items():
        line = [annotator_id, number_of_annotations]
        with open(csv_path,'a') as f:
            writer = csv.writer(f)
            writer.writerow(line)


if __name__ == "__main__":
    db_path = "./tests/data/inputs/bdrc_crop_images.sqlite"
    csv_path  = "./data/page_annnotations_count.csv"
    count_annotations_and_write_csv(db_path, csv_path)