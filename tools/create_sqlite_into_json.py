import json
import sqlite3


def update_db(db_path):
    final_dict = []
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("SELECT id, content FROM example")
    rows = cursor.fetchall()

    for row in rows:
        id = row[0]
        content = row[1]
        content_dict = json.loads(content)
        final_dict.append(content_dict)
        content_dict = {}
    json_string = json.dumps(final_dict)
    with open('layout_analysis.json', 'w') as f:
        f.write(json_string)

if __name__ == "__main__":
    db_path = "./layout_analysis.sqlite"
    update_db(db_path)