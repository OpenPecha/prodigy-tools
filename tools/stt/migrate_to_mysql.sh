#!/bin/bash

# for stats
# sudo -u prodigy PRODIGY_CONFIG="/usr/local/prodigy/prodigy-tools/configuration/stt_tt_ga.json" /usr/bin/python3.9 -m prodigy stats stt_tt_ga -l

# stt_tt_ga
sudo -u prodigy PRODIGY_CONFIG="/usr/local/prodigy/prodigy-tools/configuration/stt_tt_ga.json" /usr/bin/python3.9 -m prodigy db-out stt_tt_ga > ./stt_tt_ga.jsonl
sudo -u prodigy PRODIGY_CONFIG="/usr/local/prodigy/prodigy-tools/configuration/stt_tt_ga_review.json" /usr/bin/python3.9 -m prodigy db-out stt_tt_ga_review > ./stt_tt_ga_review.jsonl

sudo -u prodigy PRODIGY_CONFIG="./config_mysql.json" /usr/bin/python3.9 -m prodigy db-in stt_tt_ga ./stt_tt_ga.jsonl
sudo -u prodigy PRODIGY_CONFIG="./config_mysql.json" /usr/bin/python3.9 -m prodigy db-in stt_tt_ga_review ./stt_tt_ga_review.jsonl

# stt_tt_gb
sudo -u prodigy PRODIGY_CONFIG="/usr/local/prodigy/prodigy-tools/configuration/stt_tt_gb.json" /usr/bin/python3.9 -m prodigy db-out stt_tt_gb > ./stt_tt_gb.jsonl
sudo -u prodigy PRODIGY_CONFIG="/usr/local/prodigy/prodigy-tools/configuration/stt_tt_gb_review.json" /usr/bin/python3.9 -m prodigy db-out stt_tt_gb_review > ./stt_tt_gb_review.jsonl

sudo -u prodigy PRODIGY_CONFIG="./config_mysql.json" /usr/bin/python3.9 -m prodigy db-in stt_tt_gb ./stt_tt_gb.jsonl
sudo -u prodigy PRODIGY_CONFIG="./config_mysql.json" /usr/bin/python3.9 -m prodigy db-in stt_tt_gb_review ./stt_tt_gb_review.jsonl

# stt_tt_gc
sudo -u prodigy PRODIGY_CONFIG="/usr/local/prodigy/prodigy-tools/configuration/stt_tt_gc.json" /usr/bin/python3.9 -m prodigy db-out stt_tt_gc > ./stt_tt_gc.jsonl
sudo -u prodigy PRODIGY_CONFIG="/usr/local/prodigy/prodigy-tools/configuration/stt_tt_gc_review.json" /usr/bin/python3.9 -m prodigy db-out stt_tt_gc_review > ./stt_tt_gc_review.jsonl

sudo -u prodigy PRODIGY_CONFIG="./config_mysql.json" /usr/bin/python3.9 -m prodigy db-in stt_tt_gc ./stt_tt_gc.jsonl
sudo -u prodigy PRODIGY_CONFIG="./config_mysql.json" /usr/bin/python3.9 -m prodigy db-in stt_tt_gc_review ./stt_tt_gc_review.jsonl