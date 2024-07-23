import pandas as pd
from pathlib import Path
import os

def read_spreadsheet():
    SHEET_ID = "1zX1JEUigHX5gSwfJKqeerhs_5Xxkq8wFbpVUBjrKEnc"
    url = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/gviz/tq?tqx=out:csv"
    df = pd.read_csv(url)
    return df

def create_folder(id):
    Path(id).mkdir(parents=True, exist_ok=True)

def download_audio(id, yt_url):
    os.system(
        f"""yt-dlp --extract-audio --audio-quality 0 --audio-format wav --postprocessor-args "-ar 16000 -ac 1" {yt_url} -o './{id}/{id}.%(ext)s'"""
    )

if __name__ == "__main__":
    spreadsheet = read_spreadsheet()
    for index, row in spreadsheet.iterrows():
        if not isinstance(row['Audio link'], str) or not isinstance(row['ID'], str):
            break
        id = row['ID']
        yt_url = row['Audio link']
        sr_no = row['Sr.no']
        # print(id, yt_url)
        if sr_no <= 1:
            print(id, yt_url)
            create_folder(id)
            download_audio(id, yt_url)