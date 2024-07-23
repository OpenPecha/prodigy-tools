import pandas as pd
import json

def filter_line_and_save_jsonl(review_jsonl, transcript_jsonl, filtered_jsonl):
    review_pf = pd.read_json(path_or_buf=review_jsonl, lines=True)
    review_set = set(review_pf['text'])
    with open(transcript_jsonl) as f, open(filtered_jsonl, 'w+', encoding='utf-8') as op:
        for line in f:
            di = json.loads(line)
            if di['text'] not in review_set:
                op.write(line)

def filter_line_and_save_jsonl_ab(review_jsonl, transcript_jsonl, filtered_jsonl):
    review_pf = pd.read_json(path_or_buf=review_jsonl, lines=True)
    review_set = set(review_pf['id'])
    with open(transcript_jsonl) as f, open(filtered_jsonl, 'w+', encoding='utf-8') as op:
        for line in f:
            di = json.loads(line)
            if di['id'] not in review_set:
                op.write(line)

filter_line_and_save_jsonl("/home/spsither/staging/stt_cs_gb_review.jsonl", "/home/spsither/staging/stt_cs_gb.jsonl", "/home/spsither/staging/stt_cs_gb_filtered.jsonl")
filter_line_and_save_jsonl("/home/spsither/staging/stt_tt_gb_review.jsonl", "/home/spsither/staging/stt_tt_gb.jsonl", "/home/spsither/staging/stt_tt_gb_filtered.jsonl")


filter_line_and_save_jsonl("/home/spsither/staging/stt_tt_ga_review.jsonl", "/home/spsither/staging/stt_tt_ga.jsonl", "/home/spsither/staging/stt_tt_ga_filtered.jsonl")
filter_line_and_save_jsonl("/home/spsither/staging/stt_tt_gb_review.jsonl", "/home/spsither/staging/stt_tt_gb.jsonl", "/home/spsither/staging/stt_tt_gb_filtered.jsonl")
filter_line_and_save_jsonl("/home/spsither/staging/stt_tt_gc_review.jsonl", "/home/spsither/staging/stt_tt_gc.jsonl", "/home/spsither/staging/stt_tt_gc_filtered.jsonl")
filter_line_and_save_jsonl("/home/spsither/staging/stt_tt_gd_review.jsonl", "/home/spsither/staging/stt_tt_gd.jsonl", "/home/spsither/staging/stt_tt_gd_filtered.jsonl")
filter_line_and_save_jsonl("/home/spsither/staging/stt_tt_ge_review.jsonl", "/home/spsither/staging/stt_tt_ge.jsonl", "/home/spsither/staging/stt_tt_ge_filtered.jsonl")
filter_line_and_save_jsonl("/home/spsither/staging/stt_tt_gf_review.jsonl", "/home/spsither/staging/stt_tt_gf.jsonl", "/home/spsither/staging/stt_tt_gf_filtered.jsonl")
filter_line_and_save_jsonl("/home/spsither/staging/stt_tt_gg_review.jsonl", "/home/spsither/staging/stt_tt_gg.jsonl", "/home/spsither/staging/stt_tt_gg_filtered.jsonl")
filter_line_and_save_jsonl("/home/spsither/staging/stt_tt_gh_review.jsonl", "/home/spsither/staging/stt_tt_gh.jsonl", "/home/spsither/staging/stt_tt_gh_filtered.jsonl")

filter_line_and_save_jsonl("/home/spsither/staging/stt_ns_ga_review.jsonl", "/home/spsither/staging/stt_ns_ga.jsonl", "/home/spsither/staging/stt_ns_ga_filtered.jsonl")
filter_line_and_save_jsonl("/home/spsither/staging/stt_ns_gb_review.jsonl", "/home/spsither/staging/stt_ns_gb.jsonl", "/home/spsither/staging/stt_ns_gb_filtered.jsonl")
filter_line_and_save_jsonl("/home/spsither/staging/stt_ns_gc_review.jsonl", "/home/spsither/staging/stt_ns_gc.jsonl", "/home/spsither/staging/stt_ns_gc_filtered.jsonl")
#filter_line_and_save_jsonl("/home/spsither/staging/stt_ns_gd_review.jsonl", "/home/spsither/staging/stt_ns_gd.jsonl", "/home/spsither/staging/stt_ns_gd_filtered.jsonl")

filter_line_and_save_jsonl("/home/spsither/staging/stt_cs_ga_review.jsonl", "/home/spsither/staging/stt_cs_ga.jsonl", "/home/spsither/staging/stt_cs_ga_filtered.jsonl")
filter_line_and_save_jsonl("/home/spsither/staging/stt_cs_gb_review.jsonl", "/home/spsither/staging/stt_cs_gb.jsonl", "/home/spsither/staging/stt_cs_gb_filtered.jsonl")
filter_line_and_save_jsonl("/home/spsither/staging/stt_cs_gc_review.jsonl", "/home/spsither/staging/stt_cs_gc.jsonl", "/home/spsither/staging/stt_cs_gc_filtered.jsonl")
filter_line_and_save_jsonl("/home/spsither/staging/stt_cs_gd_review.jsonl", "/home/spsither/staging/stt_cs_gd.jsonl", "/home/spsither/staging/stt_cs_gd_filtered.jsonl")
filter_line_and_save_jsonl("/home/spsither/staging/stt_cs_ge_review.jsonl", "/home/spsither/staging/stt_cs_ge.jsonl", "/home/spsither/staging/stt_cs_ge_filtered.jsonl")
filter_line_and_save_jsonl("/home/spsither/staging/stt_cs_gf_review.jsonl", "/home/spsither/staging/stt_cs_gf.jsonl", "/home/spsither/staging/stt_cs_gf_filtered.jsonl")

filter_line_and_save_jsonl_ab("/home/spsither/staging/stt_ab_ga_review.jsonl", "/home/spsither/staging/stt_ab_ga.jsonl", "/home/spsither/staging/stt_ab_ga_filtered.jsonl")
filter_line_and_save_jsonl_ab("/home/spsither/staging/stt_ab_gb_review.jsonl", "/home/spsither/staging/stt_ab_gb.jsonl", "/home/spsither/staging/stt_ab_gb_filtered.jsonl")