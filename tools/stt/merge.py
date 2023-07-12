import pandas as pd
review_jsonl = "~/test/stt_tt_ga_review.jsonl"
transcript_jsonl = "~/test/stt_tt_ga.jsonl"
merged_jsonl = "/home/spsither/test/merged.jsonl"

review_pd = pd.read_json(path_or_buf=review_jsonl, lines=True)
transcript_pd = pd.read_json(path_or_buf=transcript_jsonl, lines=True)

review_df = review_pd.drop_duplicates(subset=['text'])
transcript_df = transcript_pd.drop_duplicates(subset=['text'])
merged = pd.merge(review_df, transcript_df, on='text', how='inner')

with open(merged_jsonl, 'w+', encoding='utf-8') as the_file:
    for i in range(len(merged)):
        first_annotation = merged.loc[i, 'transcript_y']
        reviewed_annotation = merged.loc[i, 'transcript_x']
        if(not isinstance(reviewed_annotation, str)):
            reviewed_annotation = ''
        if(not isinstance(first_annotation, str)):
            first_annotation = ''
        if(not reviewed_annotation == ''):
            the_file.write(f"""{{"id":"{merged.loc[i, 'text']}", "audio_url":"{merged.loc[i, 'audio_x']}", "first_annotation":"{first_annotation.encode('unicode-escape').decode('ascii')}", "reviewed_annotation":"{reviewed_annotation.encode('unicode-escape').decode('ascii')}"}}\n""")