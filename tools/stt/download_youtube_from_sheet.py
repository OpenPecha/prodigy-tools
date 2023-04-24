import pandas as pd
from pathlib import Path
import os

def read_spreadsheet():
    SHEET_ID = "1UOhU5Jcge89URmfagDf7Imm_QP74opOx6QsS2LaOSd0"
    url = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/gviz/tq?tqx=out:csv"
    df = pd.read_csv(url)
    return df

def create_folder(id):
    Path(id).mkdir(parents=True, exist_ok=True)
    
def download_audio(id, yt_url):
    os.system(
        f"""yt-dlp --extract-audio --audio-quality 0 --audio-format mp3 --postprocessor-args "-ar 16000 -ac 1" {yt_url} -o './{id}/{id}.%(ext)s'"""
    )
        
if __name__ == "__main__":
    spreadsheet = read_spreadsheet()
    for index, row in spreadsheet.iterrows():
        if not isinstance(row['Source URL'], str) or not isinstance(row['ID/Repo Name'], str):
            break
        print(row['ID/Repo Name'], row['Source URL'])
        id = row['ID/Repo Name']
        yt_url = row['Source URL']
        create_folder(id)
        download_audio(id, yt_url)