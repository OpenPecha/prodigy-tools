#!/bin/bash

# Stop the Prodigy service
sudo systemctl stop prodigy_bdrc_crop_images.service

# Run the Python script
/usr/bin/python3.9 -m update_s3_url.py /usr/local/prodigy/layout_analysis_01.sqlite

# Start the Prodigy service again
sudo systemctl start prodigy_bdrc_crop_images.service
