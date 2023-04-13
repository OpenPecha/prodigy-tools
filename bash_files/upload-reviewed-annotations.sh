sudo -u prodigy PRODIGY_CONFIG="/usr/local/prodigy/prodigy-tools/configuration/review_layout_annotation.json" /usr/bin/python3.9 -m prodigy db-out reviewed_annotations > ./reviewed_layout_annotations.jsonl

# Create a zip archive of the exported files
backup_filename=$(date +%Y-%m-%d).zip
zip -r $backup_filename reviewed_layout_annotations.jsonl

# Upload the zip archive to S3 using the AWS CLI
aws s3 cp $backup_filename s3://image-processing.openpecha/backup/reviewed-layout/$backup_filename --profile image_processing_openpecha
