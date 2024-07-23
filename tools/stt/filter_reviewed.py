import pandas as pd

def filter_and_save_jsonl(review_jsonl, transcript_jsonl, filtered_jsonl):
    review_pd = pd.read_json(path_or_buf=review_jsonl, lines=True)
    transcript_pd = pd.read_json(path_or_buf=transcript_jsonl, lines=True)
    
    review_df = review_pd.drop_duplicates(subset=['text'])
    transcript_df = transcript_pd.drop_duplicates(subset=['text'])
    
    transcript_df = transcript_df.dropna()

    transcript_df = transcript_df[~transcript_df['text'].isin(review_df['text'])]
    
    with open(filtered_jsonl, 'w+', encoding='utf-8') as the_file:
        for i in range(len(transcript_df)):
            transcript = transcript_df.iloc[i]['transcript']
            the_file.write(f"""{{"audio":"{transcript_df.iloc[i]['audio']}","text":"{transcript_df.iloc[i]['text']}","path":"{transcript_df.iloc[i]['audio']}","_input_hash":{transcript_df.iloc[i]['_input_hash']},"_task_hash":{transcript_df.iloc[i]['_task_hash']},"_view_id":"{transcript_df.iloc[i]['_view_id']}","transcript":"{transcript.encode('unicode-escape').decode('ascii')}","answer":"{transcript_df.iloc[i]['answer']}","_timestamp":{transcript_df.iloc[i]['_timestamp']},"_annotator_id":"{transcript_df.iloc[i]['_annotator_id']}","_session_id":"{transcript_df.iloc[i]['_session_id']}"}}\n""")

def filter_and_save_jsonl_ab(review_jsonl, transcript_jsonl, filtered_jsonl):
    review_pd = pd.read_json(path_or_buf=review_jsonl, lines=True)
    transcript_pd = pd.read_json(path_or_buf=transcript_jsonl, lines=True)
    
    review_df = review_pd.drop_duplicates(subset=['id'])
    transcript_df = transcript_pd.drop_duplicates(subset=['id'])
    
    transcript_df = transcript_df.dropna()

    transcript_df = transcript_df[~transcript_df['id'].isin(review_df['id'])]
    
    with open(filtered_jsonl, 'w+', encoding='utf-8') as the_file:
        for i in range(len(transcript_df)):
            transcript = transcript_df.iloc[i]['transcript']
            the_file.write(f"""{{"audio":"{transcript_df.iloc[i]['audio']}","url":"{transcript_df.iloc[i]['audio']}","text":"{transcript_df.iloc[i]['id']}","path":"{transcript_df.iloc[i]['audio']}","_input_hash":{transcript_df.iloc[i]['_input_hash']},"_task_hash":{transcript_df.iloc[i]['_task_hash']},"_view_id":"{transcript_df.iloc[i]['_view_id']}","transcript":"{transcript.encode('unicode-escape').decode('ascii')}","answer":"{transcript_df.iloc[i]['answer']}","_timestamp":{transcript_df.iloc[i]['_timestamp']},"_annotator_id":"{transcript_df.iloc[i]['_annotator_id']}","_session_id":"{transcript_df.iloc[i]['_session_id']}"}}\n""")


filter_and_save_jsonl("/home/spsither/staging/stt_tt_ga_review.jsonl", "/home/spsither/staging/stt_tt_ga.jsonl", "/home/spsither/staging/stt_tt_ga_filtered.jsonl")
filter_and_save_jsonl("/home/spsither/staging/stt_tt_gb_review.jsonl", "/home/spsither/staging/stt_tt_gb.jsonl", "/home/spsither/staging/stt_tt_gb_filtered.jsonl")
filter_and_save_jsonl("/home/spsither/staging/stt_tt_gc_review.jsonl", "/home/spsither/staging/stt_tt_gc.jsonl", "/home/spsither/staging/stt_tt_gc_filtered.jsonl")
filter_and_save_jsonl("/home/spsither/staging/stt_tt_gd_review.jsonl", "/home/spsither/staging/stt_tt_gd.jsonl", "/home/spsither/staging/stt_tt_gd_filtered.jsonl")
filter_and_save_jsonl("/home/spsither/staging/stt_tt_ge_review.jsonl", "/home/spsither/staging/stt_tt_ge.jsonl", "/home/spsither/staging/stt_tt_ge_filtered.jsonl")
filter_and_save_jsonl("/home/spsither/staging/stt_tt_gf_review.jsonl", "/home/spsither/staging/stt_tt_gf.jsonl", "/home/spsither/staging/stt_tt_gf_filtered.jsonl")
filter_and_save_jsonl("/home/spsither/staging/stt_tt_gg_review.jsonl", "/home/spsither/staging/stt_tt_gg.jsonl", "/home/spsither/staging/stt_tt_gg_filtered.jsonl")
filter_and_save_jsonl("/home/spsither/staging/stt_tt_gh_review.jsonl", "/home/spsither/staging/stt_tt_gh.jsonl", "/home/spsither/staging/stt_tt_gh_filtered.jsonl")

filter_and_save_jsonl("/home/spsither/staging/stt_ns_ga_review.jsonl", "/home/spsither/staging/stt_ns_ga.jsonl", "/home/spsither/staging/stt_ns_ga_filtered.jsonl")
filter_and_save_jsonl("/home/spsither/staging/stt_ns_gb_review.jsonl", "/home/spsither/staging/stt_ns_gb.jsonl", "/home/spsither/staging/stt_ns_gb_filtered.jsonl")
filter_and_save_jsonl("/home/spsither/staging/stt_ns_gc_review.jsonl", "/home/spsither/staging/stt_ns_gc.jsonl", "/home/spsither/staging/stt_ns_gc_filtered.jsonl")
#filter_and_save_jsonl("/home/spsither/staging/stt_ns_gd_review.jsonl", "/home/spsither/staging/stt_ns_gd.jsonl", "/home/spsither/staging/stt_ns_gd_filtered.jsonl")

filter_and_save_jsonl("/home/spsither/staging/stt_cs_ga_review.jsonl", "/home/spsither/staging/stt_cs_ga.jsonl", "/home/spsither/staging/stt_cs_ga_filtered.jsonl")
filter_and_save_jsonl("/home/spsither/staging/stt_cs_gb_review.jsonl", "/home/spsither/staging/stt_cs_gb.jsonl", "/home/spsither/staging/stt_cs_gb_filtered.jsonl")
filter_and_save_jsonl("/home/spsither/staging/stt_cs_gc_review.jsonl", "/home/spsither/staging/stt_cs_gc.jsonl", "/home/spsither/staging/stt_cs_gc_filtered.jsonl")
filter_and_save_jsonl("/home/spsither/staging/stt_cs_gd_review.jsonl", "/home/spsither/staging/stt_cs_gd.jsonl", "/home/spsither/staging/stt_cs_gd_filtered.jsonl")
filter_and_save_jsonl("/home/spsither/staging/stt_cs_ge_review.jsonl", "/home/spsither/staging/stt_cs_ge.jsonl", "/home/spsither/staging/stt_cs_ge_filtered.jsonl")
filter_and_save_jsonl("/home/spsither/staging/stt_cs_gf_review.jsonl", "/home/spsither/staging/stt_cs_gf.jsonl", "/home/spsither/staging/stt_cs_gf_filtered.jsonl")

filter_and_save_jsonl_ab("/home/spsither/staging/stt_ab_ga_review.jsonl", "/home/spsither/staging/stt_ab_ga.jsonl", "/home/spsither/staging/stt_ab_ga_filtered.jsonl")
filter_and_save_jsonl_ab("/home/spsither/staging/stt_ab_gb_review.jsonl", "/home/spsither/staging/stt_ab_gb.jsonl", "/home/spsither/staging/stt_ab_gb_filtered.jsonl")