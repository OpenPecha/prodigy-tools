#!/bin/bash

# Export data from the database into separate files
sudo -u prodigy PRODIGY_CONFIG="/usr/local/prodigy/prodigy-tools/configuration/layout_analysis_01.json" /usr/bin/python3.9 -m prodigy db-out layout_analysis_01 > ./layout_analysis_01.jsonl
sudo -u prodigy PRODIGY_CONFIG="/usr/local/prodigy/prodigy-tools/configuration/layout_analysis_02.json" /usr/bin/python3.9 -m prodigy db-out layout_analysis_02 > ./layout_analysis_02.jsonl
sudo -u prodigy PRODIGY_CONFIG="/usr/local/prodigy/prodigy-tools/configuration/layout_analysis_03.json" /usr/bin/python3.9 -m prodigy db-out layout_analysis_03 > ./layout_analysis_03.jsonl

# Create a zip archive of the exported files
backup_filename=$(date +%Y-%m-%d).zip
zip -r $backup_filename layout_analysis_01.json layout_analysis_02.json layout_analysis_03.json

# Upload the zip archive to S3 using the AWS CLI
aws s3 cp $backup_filename s3://image-processing.openpecha/backup/$backup_filename --profile image_processing_openpecha