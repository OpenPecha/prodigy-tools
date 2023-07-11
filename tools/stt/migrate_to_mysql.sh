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

# stt_tt_gd
sudo -u prodigy PRODIGY_CONFIG="/usr/local/prodigy/prodigy-tools/configuration/stt_tt_gd.json" /usr/bin/python3.9 -m prodigy db-out stt_tt_gd > ./stt_tt_gd.jsonl
sudo -u prodigy PRODIGY_CONFIG="/usr/local/prodigy/prodigy-tools/configuration/stt_tt_gd_review.json" /usr/bin/python3.9 -m prodigy db-out stt_tt_gd_review > ./stt_tt_gd_review.jsonl

sudo -u prodigy PRODIGY_CONFIG="./config_mysql.json" /usr/bin/python3.9 -m prodigy db-in stt_tt_gd ./stt_tt_gd.jsonl
sudo -u prodigy PRODIGY_CONFIG="./config_mysql.json" /usr/bin/python3.9 -m prodigy db-in stt_tt_gd_review ./stt_tt_gd_review.jsonl

# stt_tt_ge
sudo -u prodigy PRODIGY_CONFIG="/usr/local/prodigy/prodigy-tools/configuration/stt_tt_ge.json" /usr/bin/python3.9 -m prodigy db-out stt_tt_ge > ./stt_tt_ge.jsonl
sudo -u prodigy PRODIGY_CONFIG="/usr/local/prodigy/prodigy-tools/configuration/stt_tt_ge_review.json" /usr/bin/python3.9 -m prodigy db-out stt_tt_ge_review > ./stt_tt_ge_review.jsonl

sudo -u prodigy PRODIGY_CONFIG="./config_mysql.json" /usr/bin/python3.9 -m prodigy db-in stt_tt_ge ./stt_tt_ge.jsonl
sudo -u prodigy PRODIGY_CONFIG="./config_mysql.json" /usr/bin/python3.9 -m prodigy db-in stt_tt_ge_review ./stt_tt_ge_review.jsonl

# stt_tt_gf
sudo -u prodigy PRODIGY_CONFIG="/usr/local/prodigy/prodigy-tools/configuration/stt_tt_gf.json" /usr/bin/python3.9 -m prodigy db-out stt_tt_gf > ./stt_tt_gf.jsonl
sudo -u prodigy PRODIGY_CONFIG="/usr/local/prodigy/prodigy-tools/configuration/stt_tt_gf_review.json" /usr/bin/python3.9 -m prodigy db-out stt_tt_gf_review > ./stt_tt_gf_review.jsonl

sudo -u prodigy PRODIGY_CONFIG="./config_mysql.json" /usr/bin/python3.9 -m prodigy db-in stt_tt_gf ./stt_tt_gf.jsonl
sudo -u prodigy PRODIGY_CONFIG="./config_mysql.json" /usr/bin/python3.9 -m prodigy db-in stt_tt_gf_review ./stt_tt_gf_review.jsonl

# stt_tt_gg
sudo -u prodigy PRODIGY_CONFIG="./stt_tt_gg.json" /usr/bin/python3.9 -m prodigy db-out stt_tt_gg > ./stt_tt_gg.jsonl
sudo -u prodigy PRODIGY_CONFIG="./stt_tt_gg.json" /usr/bin/python3.9 -m prodigy db-out stt_tt_gg_review > ./stt_tt_gg_review.jsonl

sudo -u prodigy PRODIGY_CONFIG="./config_mysql.json" /usr/bin/python3.9 -m prodigy db-in stt_tt_gg ./stt_tt_gg.jsonl
sudo -u prodigy PRODIGY_CONFIG="./config_mysql.json" /usr/bin/python3.9 -m prodigy db-in stt_tt_gg_review ./stt_tt_gg_review.jsonl

# stt_tt_gh
sudo -u prodigy PRODIGY_CONFIG="./stt_tt_gh.json" /usr/bin/python3.9 -m prodigy db-out stt_tt_gh > ./stt_tt_gh.jsonl
sudo -u prodigy PRODIGY_CONFIG="./stt_tt_gh.json" /usr/bin/python3.9 -m prodigy db-out stt_tt_gh_review > ./stt_tt_gh_review.jsonl

sudo -u prodigy PRODIGY_CONFIG="./config_mysql.json" /usr/bin/python3.9 -m prodigy db-in stt_tt_gh ./stt_tt_gh.jsonl
sudo -u prodigy PRODIGY_CONFIG="./config_mysql.json" /usr/bin/python3.9 -m prodigy db-in stt_tt_gh_review ./stt_tt_gh_review.jsonl

# stt_ns_ga
sudo -u prodigy PRODIGY_CONFIG="./stt_ns_ga.json" /usr/bin/python3.9 -m prodigy db-out stt_ns_ga > ./stt_ns_ga.jsonl
sudo -u prodigy PRODIGY_CONFIG="./stt_ns_ga.json" /usr/bin/python3.9 -m prodigy db-out stt_ns_ga_review > ./stt_ns_ga_review.jsonl

sudo -u prodigy PRODIGY_CONFIG="./config_mysql.json" /usr/bin/python3.9 -m prodigy db-in stt_ns_ga ./stt_ns_ga.jsonl
sudo -u prodigy PRODIGY_CONFIG="./config_mysql.json" /usr/bin/python3.9 -m prodigy db-in stt_ns_ga_review ./stt_ns_ga_review.jsonl

# stt_ns_gb
sudo -u prodigy PRODIGY_CONFIG="./stt_ns.json" /usr/bin/python3.9 -m prodigy db-out stt_ns_gb > ./stt_ns_gb.jsonl
sudo -u prodigy PRODIGY_CONFIG="./stt_ns.json" /usr/bin/python3.9 -m prodigy db-out stt_ns_gb_review > ./stt_ns_gb_review.jsonl

sudo -u prodigy PRODIGY_CONFIG="./config_mysql.json" /usr/bin/python3.9 -m prodigy db-in stt_ns_gb ./stt_ns_gb.jsonl
sudo -u prodigy PRODIGY_CONFIG="./config_mysql.json" /usr/bin/python3.9 -m prodigy db-in stt_ns_gb_review ./stt_ns_gb_review.jsonl

# stt_ns_gc
sudo -u prodigy PRODIGY_CONFIG="./stt_ns.json" /usr/bin/python3.9 -m prodigy db-out stt_ns_gc > ./stt_ns_gc.jsonl
sudo -u prodigy PRODIGY_CONFIG="./stt_ns.json" /usr/bin/python3.9 -m prodigy db-out stt_ns_gc_review > ./stt_ns_gc_review.jsonl

sudo -u prodigy PRODIGY_CONFIG="./config_mysql.json" /usr/bin/python3.9 -m prodigy db-in stt_ns_gc ./stt_ns_gc.jsonl
sudo -u prodigy PRODIGY_CONFIG="./config_mysql.json" /usr/bin/python3.9 -m prodigy db-in stt_ns_gc_review ./stt_ns_gc_review.jsonl

# stt_ns_gd
sudo -u prodigy PRODIGY_CONFIG="./stt_ns.json" /usr/bin/python3.9 -m prodigy db-out stt_ns_gd > ./stt_ns_gd.jsonl
sudo -u prodigy PRODIGY_CONFIG="./stt_ns.json" /usr/bin/python3.9 -m prodigy db-out stt_ns_gd_review > ./stt_ns_gd_review.jsonl

sudo -u prodigy PRODIGY_CONFIG="./config_mysql.json" /usr/bin/python3.9 -m prodigy db-in stt_ns_gd ./stt_ns_gd.jsonl
sudo -u prodigy PRODIGY_CONFIG="./config_mysql.json" /usr/bin/python3.9 -m prodigy db-in stt_ns_gd_review ./stt_ns_gd_review.jsonl

# stt_cs_ga
sudo -u prodigy PRODIGY_CONFIG="/usr/local/prodigy/prodigy-tools/configuration/stt_cs.json" /usr/bin/python3.9 -m prodigy db-out stt_cs > ./stt_cs_ga.jsonl
sudo -u prodigy PRODIGY_CONFIG="/usr/local/prodigy/prodigy-tools/configuration/stt_cs_review.json" /usr/bin/python3.9 -m prodigy db-out stt_cs_review > ./stt_cs_ga_review.jsonl

sudo -u prodigy PRODIGY_CONFIG="./config_mysql.json" /usr/bin/python3.9 -m prodigy db-in stt_cs ./stt_cs_ga.jsonl
sudo -u prodigy PRODIGY_CONFIG="./config_mysql.json" /usr/bin/python3.9 -m prodigy db-in stt_cs_review ./stt_cs_ga_review.jsonl

# stt_cs_gb
sudo -u prodigy PRODIGY_CONFIG="/usr/local/prodigy/prodigy-tools/configuration/stt_cs_gb.json" /usr/bin/python3.9 -m prodigy db-out stt_cs_gb > ./stt_cs_gb.jsonl
sudo -u prodigy PRODIGY_CONFIG="/usr/local/prodigy/prodigy-tools/configuration/stt_cs_gb_review.json" /usr/bin/python3.9 -m prodigy db-out stt_cs_gb_review > ./stt_cs_gb_review.jsonl

sudo -u prodigy PRODIGY_CONFIG="./config_mysql.json" /usr/bin/python3.9 -m prodigy db-in stt_cs_gb ./stt_cs_gb.jsonl
sudo -u prodigy PRODIGY_CONFIG="./config_mysql.json" /usr/bin/python3.9 -m prodigy db-in stt_cs_gb_review ./stt_cs_gb_review.jsonl

# stt_cs_gc
sudo -u prodigy PRODIGY_CONFIG="/usr/local/prodigy/prodigy-tools/configuration/stt_cs_gc.json" /usr/bin/python3.9 -m prodigy db-out stt_cs_gc > ./stt_cs_gc.jsonl
sudo -u prodigy PRODIGY_CONFIG="/usr/local/prodigy/prodigy-tools/configuration/stt_cs_gc_review.json" /usr/bin/python3.9 -m prodigy db-out stt_cs_gc_review > ./stt_cs_gc_review.jsonl

sudo -u prodigy PRODIGY_CONFIG="./config_mysql.json" /usr/bin/python3.9 -m prodigy db-in stt_cs_gc ./stt_cs_gc.jsonl
sudo -u prodigy PRODIGY_CONFIG="./config_mysql.json" /usr/bin/python3.9 -m prodigy db-in stt_cs_gc_review ./stt_cs_gc_review.jsonl